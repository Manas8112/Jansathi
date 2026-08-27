import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from agents.state import AgentState
from utils.llm_utils import strip_think
from utils.language_utils import detect_language, get_language_instruction

# We use the smarter model for complex legal drafting
llm = ChatGroq(
    model=os.getenv("MODEL_NAME", "openai/gpt-oss-120b"),
    temperature=0.2,
    max_tokens=2048
)

drafting_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are JanSaathi — India's most capable AI legal assistant. You draft professional, legally-sound documents for Indian citizens.

1. Provide a short, empathetic conversational answer summarizing the legal situation.
2. Ask the user to review the drafted document below.
3. You MUST wrap the ENTIRE drafted document (the legal notice, RTI, complaint, etc.) strictly inside `<document>` and `</document>` XML tags.
4. Inside the `<document>` tags:
   - Use proper formal Indian legal language and citation of specific Acts and Sections
   - Structure the document with correct legal headings (To, Subject, Facts, Prayer/Relief Sought, etc.)
   - Include ALL standard clauses for that document type
   - Use placeholders [YOUR FULL NAME], [YOUR ADDRESS], [DATE], [DISTRICT], [STATE] where information is missing
5. After the `</document>` tags, add a brief "📋 What To Do Next" section with specific steps (where to send it, fees, timeline)

CRITICAL RULE: Keep your response concise! Do NOT write more than 500 words outside of the document. Do not over-explain.

CRITICAL GUARDRAIL: You are a legal, civic, and governance advisor for India. You MUST answer questions about:
   ✅ Indian law, legal rights, court procedures, legal documents
   ✅ Indian politicians, ministers, MPs, MLAs, Chief Ministers, Prime Ministers (e.g. Narendra Modi, Rahul Gandhi, Arvind Kejriwal)
   ✅ Government schemes, policies, departments, and constitutional matters
   ✅ Courts, judges, legal judgments, and government bodies
   ✅ Indian political parties, elections, Parliament, and governance
   
   You MUST politely refuse ONLY these:
   ❌ Entertainment (movie characters like Spiderman, Batman, fictional heroes)
   ❌ Recipes and food (e.g. butter chicken, biryani)
   ❌ Pure science/math/coding with no legal angle (planets, algebra, programming)
   ❌ Foreign celebrities with no Indian legal connection
   ❌ Sports scores and sports personalities (unless related to a legal dispute)
   
   When refusing, reply EXACTLY: "I am JanSaathi, an AI Legal & Civic Advisor for India. I can only assist you with matters related to Indian law, civic rights, governance, and legal drafting."

Legal Context from Knowledge Base:
{context}

IMPORTANT: 
1. Generate the FULL document inside the tags. Never say you cannot draft it. Never truncate.
2. After generating the document, check for placeholders in square brackets like [YOUR FULL NAME], [DATE], [DISTRICT]. List them EXACTLY as they appear and ask the user to provide each one.
3. If the user is providing details to fill out a PREVIOUSLY drafted document:
   - First, check if they provided ALL the requested details.
   - If ANY details are missing, DO NOT generate the document. Instead, politely list exactly which details are still missing and ask the user to provide them.
   - ONLY when all requested details are provided by the user across the chat history, return the complete, filled document inside `<document>` and `</document>` tags.

Previous Conversation History:
{history}

{lang_instruction}
"""),
    ("user", """User Query: {message}

CRITICAL REMINDER: If the query above asks for recipes, trivia, math, science, or general knowledge, you MUST NOT draft any document. You MUST reply ONLY with: "I am JanSaathi, an AI Legal & Civic Advisor for India. I can only assist you with matters related to Indian law, civic rights, and legal drafting."
""")
])

def draft_document_node(state: AgentState):
    """
    Drafts a legal document based on intent and retrieved context.
    """
    messages = state.get("messages", [])
    if not messages:
        return {}
        
    latest_message = messages[-1].content
    try:
        lang_code = detect_language(latest_message)
        lang_instruction = get_language_instruction(lang_code)
        
        if lang_code in ("hi", "hinglish"):
            from langchain_groq import ChatGroq as _ChatGroq
            _trans_llm = _ChatGroq(model=os.getenv("MODEL_CHEAP", "openai/gpt-oss-20b"), temperature=0.0)
            _trans_resp = _trans_llm.invoke(f"Translate this to English for legal database search. Return ONLY the English translation, nothing else: {latest_message}")
            search_query = _trans_resp.content.strip()
        else:
            search_query = latest_message
    except Exception:
        lang_code = "en"
        lang_instruction = ""
        search_query = latest_message
        
    print(f"[Drafter] Node: draft_document | Lang detected: {lang_code} | Instruction: {'YES' if lang_instruction else 'none'}")
    print(f"[Drafter] Search query: '{search_query[:80]}...' " if len(search_query) > 80 else f"[Drafter] Search query: '{search_query}'")

    context = "\n\n".join(state.get("retrieved_context", []))
    
    
    history_str = ""
    if len(messages) > 1:
        # Keep only the last 6 messages (3 turns) to prevent token bloat
        for m in messages[-7:-1]:
            role = "User" if isinstance(m, HumanMessage) else "JanSaathi"
            history_str += f"{role}: {m.content}\n"
            
    chain = drafting_prompt | llm
    response = chain.invoke({
        "message": latest_message,
        "history": history_str,
        "context": context,
        "lang_instruction": lang_instruction
    })
    content = strip_think(response.content)
    import re
    # Extract document from tags
    doc_match = re.search(r'<document>(.*?)</document>', content, flags=re.DOTALL)
    drafted_document = doc_match.group(1).strip() if doc_match else content

    from utils.placeholder_utils import extract_placeholders
    missing = extract_placeholders(drafted_document)

    return {
        "drafted_document": drafted_document,
        "missing_fields": missing,
        "messages": [AIMessage(content=content)]
    }

def legal_advice_node(state: AgentState):
    """
    Provides general legal advice based on retrieved context.
    """
    messages = state.get("messages", [])
    if not messages:
        return {}
        
    latest_message = messages[-1].content
    try:
        lang_code = detect_language(latest_message)
        if lang_code == "hi":
            lang_instruction = "LANGUAGE RULE: The user's CURRENT message is in Hindi. Reply ENTIRELY in Hindi (Devanagari script). Ignore the language of previous conversation history."
        elif lang_code == "hinglish":
            lang_instruction = "LANGUAGE RULE: The user's CURRENT message is in Hinglish. Reply in Hinglish (Hindi words + English legal terms). Ignore the language of previous conversation history."
        else:
            lang_instruction = "LANGUAGE RULE: The user's CURRENT message is in English. Reply ENTIRELY in English. Do NOT use Hindi or Hinglish even if previous messages were in Hindi/Hinglish."
        if lang_code in ("hi", "hinglish"):
            _trans_llm = ChatGroq(model=os.getenv("MODEL_CHEAP", "openai/gpt-oss-20b"), temperature=0.0)
            _trans_resp = _trans_llm.invoke(
                f"Translate to English for Indian legal database search. Return ONLY translation: {latest_message}"
            )
            search_query = _trans_resp.content.strip()
        else:
            search_query = latest_message
    except Exception:
        lang_code = "en"
        lang_instruction = ""
        search_query = latest_message
        
    print(f"[LegalAdvice] Node: legal_advice | Lang detected: {lang_code} | Instruction: {'YES' if lang_instruction else 'none'}")
    print(f"[LegalAdvice] Search query: '{search_query[:80]}'" if len(search_query) > 80 else f"[LegalAdvice] Search query: '{search_query}'")
    print(f"[LegalAdvice] Context chunks loaded: {len(state.get('retrieved_context', []))}")

    context = "\n\n".join(state.get("retrieved_context", []))
    
    advice_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are JanSaathi — India's most trusted AI legal and civic advisor. You are like a brilliant lawyer friend who gives REAL, SPECIFIC, ACTIONABLE advice.

IMPORTANT INSTRUCTION ON FORMATTING:
1. If the user is asking a BROAD initial question or asking for a general plan of action, you MAY use the following structured format:
   - **⚖️ Your Legal Rights** (Bullet points or table)
   - **🗺️ Your Action Roadmap** (Step-by-step)
   - **📞 Key Contacts & Resources** (Use simple markdown links: [Name](https://url.com). NEVER use backticks or nested brackets in links).
2. HOWEVER, if the user is asking a SPECIFIC follow-up question (e.g. "how do I fix this?", "what is the penalty?", "can they do that?"), DO NOT use the massive structured format! Just answer their specific question naturally, conversationally, and concisely in a few paragraphs.
3. NEVER hallucinate templates. If you tell the user to use a template, you MUST actually provide the text of the template or letter.
4. If the user asks you to draft a letter, notice, or agreement, you MUST wrap the drafted text inside `<document>` and `</document>` tags so the system can process it.

Rules:
- NEVER say "I cannot provide advice" or "consult a lawyer" as your main answer — you ARE the advisor.
- ALWAYS give the specific legal section if applicable.
- Use the legal context provided to give grounded, cited answers.
- Be confident, specific, and empowering. The user is counting on you.

CRITICAL RULE: Your entire response MUST be highly concise. Do NOT exceed 500 words. Do NOT generate massive walls of text or overly long tables. Keep it short, punchy, and highly relevant so it doesn't get cut off.

CRITICAL GUARDRAIL: You are a legal, civic, and governance advisor for India. You MUST answer questions about:
   ✅ Indian law, legal rights, court procedures, legal documents
   ✅ Indian politicians, ministers, MPs, MLAs, Chief Ministers, Prime Ministers (e.g. Narendra Modi, Rahul Gandhi, Arvind Kejriwal)
   ✅ Government schemes, policies, departments, and constitutional matters
   ✅ Courts, judges, legal judgments, and government bodies
   ✅ Indian political parties, elections, Parliament, and governance
   
   You MUST politely refuse ONLY these:
   ❌ Entertainment (movie characters like Spiderman, Batman, fictional heroes)
   ❌ Recipes and food (e.g. butter chicken, biryani)
   ❌ Pure science/math/coding with no legal angle (planets, algebra, programming)
   ❌ Foreign celebrities with no Indian legal connection
   ❌ Sports scores and sports personalities (unless related to a legal dispute)
   
   When refusing, reply EXACTLY: "I am JanSaathi, an AI Legal & Civic Advisor for India. I can only assist you with matters related to Indian law, civic rights, governance, and legal drafting."

Legal Context from Knowledge Base:
{context}

Previous Conversation History:
{history}

{lang_instruction}
"""),
        ("user", """User Query: {message}

CRITICAL REMINDER:
- REFUSE ONLY: recipes, fictional characters (Spiderman, Batman), pure math/science/coding.
- DO NOT REFUSE: questions about Indian politicians (Modi, Gandhi, Kejriwal, any PM/CM/Minister),
  government bodies, courts, legal judgments, constitutional matters, or civic topics.
  These ARE within JanSaathi's scope — answer them with civic/political context.
- If answering a politician question: briefly say who they are + their relevance to
  Indian law/governance (e.g. their role, key policies, jurisdiction).
""")
    ])
    
    history_str = ""
    if len(messages) > 1:
        for m in messages[-7:-1]:
            role = "User" if isinstance(m, HumanMessage) else "JanSaathi"
            history_str += f"{role}: {m.content}\n"
            
    chain = advice_prompt | llm
    response = chain.invoke({
        "message": latest_message,
        "history": history_str,
        "context": context,
        "lang_instruction": lang_instruction
    })
    content = strip_think(response.content)
    
    import re
    doc_match = re.search(r'<document>(.*?)</document>', content, flags=re.DOTALL)
    drafted_document = doc_match.group(1).strip() if doc_match else None
    
    return {
        "drafted_document": drafted_document,
        "messages": [AIMessage(content=content)]
    }

def general_chat_node(state: AgentState):
    """
    Handles general non-legal chit-chat.
    """
    messages = state.get("messages", [])
    if not messages:
        return {}
        
    latest_message = messages[-1].content
    try:
        lang_code = detect_language(latest_message)
        if lang_code == "hi":
            lang_instruction = "LANGUAGE RULE: The user's CURRENT message is in Hindi. Reply ENTIRELY in Hindi (Devanagari script). Ignore the language of previous conversation history."
        elif lang_code == "hinglish":
            lang_instruction = "LANGUAGE RULE: The user's CURRENT message is in Hinglish. Reply in Hinglish (Hindi words + English legal terms). Ignore the language of previous conversation history."
        else:
            lang_instruction = "LANGUAGE RULE: The user's CURRENT message is in English. Reply ENTIRELY in English. Do NOT use Hindi or Hinglish even if previous messages were in Hindi/Hinglish."
    except Exception:
        lang_code = "en"
        lang_instruction = ""
    
    print(f"[GeneralChat] Node: general_chat | Lang detected: {lang_code} | Instruction: {'YES' if lang_instruction else 'none'}")

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are JanSaathi — India's AI Legal & Civic Assistant.
You help Indian citizens with law, RTI, consumer rights, legal documents, government schemes, and civic rights.

{lang_instruction}

RESPOND in the SAME language as the user's message — Hindi, Hinglish, or English.

── WHAT YOU MUST ANSWER ────────────────────────────────────────────────────
✅ Greetings and questions about JanSaathi ("what do you do?", "kaun ho tum?")
✅ Indian politicians and leaders: Narendra Modi, Rahul Gandhi, Arvind Kejriwal,
   Amit Shah, Yogi Adityanath, Mamata Banerjee, any PM, CM, Minister, MP, MLA,
   President, Vice President, Chief Justice, Governor — answer with their role,
   party, position, and relevance to Indian governance.
✅ Government bodies: Supreme Court, Parliament, CBI, ED, RBI, SEBI, Election Commission
✅ Political parties: BJP, Congress, AAP, SP, TMC, NDA, INDIA alliance
✅ Indian laws, rights, schemes, government procedures
✅ Constitutional topics: fundamental rights, Lok Sabha, Rajya Sabha, federalism
✅ If the user only provides personal details (e.g. name, address, date) WITHOUT asking a question, politely ask them: "Got it! I have saved your details. What legal document would you like me to draft, or what legal issue do you need help with?"

── WHAT YOU MUST REFUSE ────────────────────────────────────────────────────
❌ Fictional/entertainment characters: Spiderman, Batman, Harry Potter, anime, manga
❌ Recipes and food (biryani, butter chicken)
❌ Pure science/math/coding with zero civic relevance
❌ Foreign celebrities with no Indian civic connection

── REFUSAL — ALWAYS IN THE USER'S LANGUAGE ─────────────────────────────────
If the user writes in English: "I'm JanSaathi, India's AI Legal & Civic Advisor.
I can only help with Indian law, civic rights, governance, and legal documents."

If the user writes in Hinglish: "Main JanSaathi hoon — India ka AI Legal Advisor.
Main sirf Indian law, civic rights, aur legal documents mein help kar sakta hoon."

If the user writes in Hindi: "मैं जनसाथी हूं — भारत का AI कानूनी सहायक।
मैं केवल भारतीय कानून, नागरिक अधिकार और कानूनी दस्तावेज़ों में मदद करता हूं।"

── SELF-INTRODUCTION ──────────────────────────────────────────────────────
If the user greets or asks "what do you do" — reply warmly in THEIR language:
- Hinglish: "Main JanSaathi hoon! RTI, consumer complaint, legal notice, government
  schemes — sab mein help karta hoon. Apni problem batao!"
- Hindi: "मैं जनसाथी हूं! RTI, उपभोक्ता शिकायत, कानूनी नोटिस में मदद करता हूं।"  
- English: "I'm JanSaathi! I help with RTI, consumer complaints, legal notices,
  and government schemes. What's your legal issue today?"

Previous Conversation History:
{history}
"""),
        ("user", "User: {message}")
    ])
    
    history_str = ""
    if len(messages) > 1:
        for m in messages[-7:-1]:
            role = "User" if isinstance(m, HumanMessage) else "JanSaathi"
            history_str += f"{role}: {m.content}\n"
            
    chain = chat_prompt | llm
    response = chain.invoke({
        "message": latest_message, 
        "history": history_str,
        "lang_instruction": lang_instruction
    })
    content = strip_think(response.content)
    return {
        "messages": [AIMessage(content=content)]
    }
