"""
Self-Correction Verifier Agent (Reflexion Technique)
======================================================
Based on the "Reflexion" paper (Shinn et al., 2023).
After the LLM generates a legal response, this agent acts as a critic:
- Checks if the response actually answers the question
- Verifies citations are real Indian law sections
- Ensures a concrete action roadmap is present
- Flags if the response is hedging / refusing to advise

If issues are found, the main LLM is asked to re-draft with specific feedback.
This loop runs MAX 1 time (to avoid latency), but catches the most common failures.
"""
import os
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from agents.state import AgentState
from utils.llm_utils import strip_think

# Use fast model for verification — it only needs to check, not generate
verifier_llm = ChatGroq(
    model=os.getenv("MODEL_CHEAP", "openai/gpt-oss-20b"),
    temperature=0.0
)

verifier_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a strict legal response quality checker for JanSaathi.

Evaluate the AI response below against these criteria. Respond with ONLY a JSON object:

{{
  "passes": true/false,
  "issues": ["list of issues found, empty if passes"],
  "score": 0-10
}}

Criteria:
1. Does it give a SPECIFIC, ACTIONABLE step-by-step roadmap? (not just general advice)
2. Does it cite at least ONE specific Indian law section (e.g., "Section 6 RTI Act")?
3. Does it mention WHERE to file / WHO to contact (specific forum/authority)?
4. Does it mention a deadline or timeframe?
5. Does it AVOID saying "I cannot provide advice" or "consult a lawyer" as the MAIN answer?
6. Is the response actually answering the user's question (not deflecting)?
7. Does the response cite only REAL Indian law sections? Valid examples include: Section 6 RTI Act, Section 35 CPA, Section 498A IPC, Section 420 IPC, Section 17 RERA, Section 19 RTI Act. Flag as issue if response cites something like 'Section 1200' or any section not commonly known.
8. Does the response avoid contradicting the user's established facts from earlier in the conversation (e.g. do NOT recommend a different court than what was already determined)?

Score 0-10 (10 = perfect, 7+ = acceptable, <7 = needs improvement)

User's Question: {question}
AI Response to evaluate: {response}

Return ONLY the JSON, nothing else."""),
    ("user", "Evaluate this response.")
])

correction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are JanSaathi — India's most trusted AI legal advisor.

Your previous response had these issues: {issues}

Rewrite your response addressing ALL these issues. Your new response MUST:
1. Give a numbered, step-by-step Action Roadmap
2. Cite specific Indian law sections
3. Name the specific forum/authority where the user should file
4. Include at least one concrete deadline or timeframe
5. Be empowering and actionable — NOT hedging
6. Do NOT cite any law section that is not a well-known, real Indian law section.

Legal Context (use this to ground your answer):
{context}

User's original question: {question}

Write the improved response now:"""),
    ("user", "Please provide an improved, complete legal response.")
])

correction_llm = ChatGroq(
    model=os.getenv("MODEL_NAME", "openai/gpt-oss-120b"),
    temperature=0.2,
    max_tokens=1024
)


def _strip_think(text: str) -> str:
    # Keep for backward compat — delegates to central utility
    return strip_think(text)


def verifier_node(state: AgentState) -> dict:
    """
    Self-correction node that runs after draft_document or legal_advice nodes.
    If the response doesn't meet quality standards, it triggers a re-draft.
    """
    messages = state.get("messages", [])
    if not messages:
        return {}

    # Skip verification if a document was successfully drafted
    # (Documents shouldn't be forced into the Action Roadmap format)
    if state.get("drafted_document"):
        print("[Verifier] Skipping verification because a document was drafted.")
        return {}
        
    # Skip verification if the user is in a general, non-actionable, or interactive flow
    # to prevent forcing deadlines/roadmaps/citations onto general informational queries.
    skip_intents = {"General_Legal_Advice", "Civic_Info", "Chitchat", "Scheme_Info", "Fill_Document", "Off-Topic"}
    if state.get("user_intent") in skip_intents:
        print(f"[Verifier] Skipping verification because intent is {state.get('user_intent')}.")
        return {}

    # Find last AI message
    ai_messages = [m for m in messages if isinstance(m, AIMessage)]
    if not ai_messages:
        return {}

    last_ai_response = ai_messages[-1].content
    last_ai_response = _strip_think(last_ai_response)

    # Skip verification if the AI successfully triggered a domain guardrail refusal
    if "I can only assist you with matters related to Indian law" in last_ai_response or "I cannot answer questions outside of the legal and civic domain" in last_ai_response:
        print("[Verifier] Skipping verification because response is a valid guardrail refusal.")
        return {}

    # Find last user message
    from langchain_core.messages import HumanMessage
    human_messages = [m for m in messages if isinstance(m, HumanMessage)]
    if not human_messages:
        return {}
    user_question = human_messages[-1].content

    # Run the verifier (up to 3 times max)
    current_response = last_ai_response
    has_modified = False

    try:
        import json
        verify_chain = verifier_prompt | verifier_llm
        correction_chain = correction_prompt | correction_llm
        context = "\n\n".join(state.get("retrieved_context", []))

        for attempt in range(1, 4):
            print(f"[Verifier] Running verification attempt {attempt}/3...")
            verify_response = _strip_think(verify_chain.invoke({
                "question": user_question,
                "response": current_response
            }).content)

            # Extract JSON from response
            json_match = re.search(r'\{.*\}', verify_response, re.DOTALL)
            if not json_match:
                print(f"[Verifier] Failed to parse JSON on attempt {attempt}, accepting current draft.")
                break

            evaluation = json.loads(json_match.group())
            score = evaluation.get("score", 10)
            passes = evaluation.get("passes", True)
            issues = evaluation.get("issues", [])

            print(f"[Verifier] Attempt {attempt} - Score: {score}/10 | Passes: {passes} | Issues: {issues}")

            if passes or score >= 7.5 or not issues:
                print(f"[Verifier] Response accepted on attempt {attempt} (score={score}/10).")
                break
            
            # If we reached the final attempt and it still fails, append a warning
            if attempt == 3:
                print("[Verifier] Max attempts (3) reached. Appending verification warning.")
                current_response += "\n\n> ⚠️ **Verification Note:** This response could not be fully verified for compliance by the reflexion layer. Please verify key details independently."
                has_modified = True
                break

            # Trigger re-draft for next attempt
            print(f"[Verifier] Score {score} < 7.5 — triggering re-draft for attempt {attempt + 1}...")
            current_response = strip_think(correction_chain.invoke({
                "issues": "; ".join(issues),
                "context": context[:3000],
                "question": user_question
            }).content)
            has_modified = True

        if has_modified:
            # Replace last AI message with the updated/corrected one
            non_ai_messages = [m for m in messages if not isinstance(m, AIMessage)]
            return {
                "messages": non_ai_messages + [AIMessage(content=current_response)]
            }

    except Exception as e:
        print(f"[Verifier] Error during verification: {e}")
        # Fail gracefully — return original response unchanged

    return {}
