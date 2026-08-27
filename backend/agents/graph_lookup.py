"""
Graph Lookup Node for LangGraph
================================
This node runs BEFORE the LLM drafting nodes. It queries:
1. The Legal Knowledge Graph — for section-specific facts and relationships
2. The Jurisdiction Engine — for deterministic forum, fee, and deadline data

Together these form a deterministic constraint layer that prevents LLM
hallucinations about courts, fees, deadlines, and legal procedures.
"""
import re
from agents.state import AgentState
from knowledge.legal_graph import get_context_for_intent
from knowledge.jurisdiction_engine import get_jurisdiction_engine
from utils.language_utils import detect_language


def extract_claim_amount(message: str) -> float:
    """Extracts claim amount in lakhs from user message."""
    crore_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:crore|cr)', message, re.IGNORECASE)
    if crore_match:
        return float(crore_match.group(1)) * 100

    lakh_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|lac|L\b)', message, re.IGNORECASE)
    if lakh_match:
        return float(lakh_match.group(1))

    rupee_match = re.search(r'(?:₹|Rs\.?|INR)\s*(\d+(?:,\d+)*(?:\.\d+)?)', message)
    if rupee_match:
        amount = float(rupee_match.group(1).replace(',', ''))
        return amount / 100000

    return 0.0


def extract_state(message: str) -> str:
    """Extracts Indian state name from user message."""
    states = [
        "Maharashtra", "Karnataka", "Delhi", "UP", "Uttar Pradesh", "Gujarat",
        "Tamil Nadu", "Telangana", "Rajasthan", "Kerala", "West Bengal",
        "Madhya Pradesh", "Bihar", "Punjab", "Haryana", "Andhra Pradesh",
        "Odisha", "Assam", "Jharkhand", "Uttarakhand", "Himachal Pradesh",
        "Chhattisgarh", "Goa"
    ]
    for state in states:
        if state.lower() in message.lower():
            return state
    return ""


def graph_lookup_node(state: AgentState) -> dict:
    """
    Queries the Legal Knowledge Graph and Jurisdiction Engine, then injects
    ground-truth facts into retrieved_context before the LLM sees the query.

    This runs after intent classification but before the LLM drafting nodes.
    """
    intent = state.get("user_intent", "General")
    messages = state.get("messages", [])

    if not messages or intent == "General":
        return {}

    latest_message = messages[-1].content
    
    try:
        lang_code = detect_language(latest_message)
        if lang_code in ("hi", "hinglish"):
            import os
            from langchain_groq import ChatGroq as _ChatGroq
            _trans_llm = _ChatGroq(model=os.getenv("MODEL_CHEAP", "openai/gpt-oss-20b"), temperature=0.0)
            _trans_resp = _trans_llm.invoke(f"Translate this to English for legal database search. Return ONLY the English translation, nothing else: {latest_message}")
            search_query = _trans_resp.content.strip()
        else:
            search_query = latest_message
    except Exception:
        search_query = latest_message

    print(f"[GraphLookup] Intent: {intent} | Search: '{search_query[:60]}'")

    claim_amount = extract_claim_amount(search_query)
    user_state = extract_state(search_query)

    # 1. Get deterministic facts from knowledge graph (section-level)
    graph_context, referenced_nodes = get_context_for_intent(intent, search_query, claim_amount)

    # 2. Get jurisdiction facts (forum, fees, deadlines)
    engine = get_jurisdiction_engine()
    jurisdiction_result = engine.resolve(intent, search_query, claim_amount, user_state)
    jurisdiction_context = jurisdiction_result.to_prompt_string() if jurisdiction_result else ""

    print(f"[GraphLookup] Graph nodes matched: {len(referenced_nodes) if referenced_nodes else 0}")
    print(f"[GraphLookup] Jurisdiction data: {'YES' if jurisdiction_context else 'none'}")

    # Prepend both to any existing RAG context
    existing_context = state.get("retrieved_context", [])
    new_context = [c for c in [jurisdiction_context, graph_context] if c] + existing_context

    return {
        "retrieved_context": new_context,
        "referenced_nodes": referenced_nodes
    }

