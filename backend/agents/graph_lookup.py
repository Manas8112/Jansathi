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
    claim_amount = extract_claim_amount(latest_message)
    user_state = extract_state(latest_message)

    # 1. Get deterministic facts from knowledge graph (section-level)
    graph_context = get_context_for_intent(intent, latest_message, claim_amount)

    # 2. Get jurisdiction facts (forum, fees, deadlines)
    engine = get_jurisdiction_engine()
    jurisdiction_result = engine.resolve(intent, latest_message, claim_amount, user_state)
    jurisdiction_context = jurisdiction_result.to_prompt_string() if jurisdiction_result else ""

    # Prepend both to any existing RAG context
    existing_context = state.get("retrieved_context", [])
    new_context = [c for c in [jurisdiction_context, graph_context] if c] + existing_context

    return {
        "retrieved_context": new_context
    }

