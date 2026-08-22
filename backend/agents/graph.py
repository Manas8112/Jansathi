from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.intent_router import intent_router_node
from agents.graph_lookup import graph_lookup_node
from agents.retriever import retrieve_context_node
from agents.drafter import draft_document_node, legal_advice_node, general_chat_node
from agents.verifier import verifier_node


def route_after_intent(state: AgentState):
    """
    All non-general intents go through knowledge graph + jurisdiction engine first.
    """
    next_action = state.get("next_action", "general_chat")
    if next_action == "general_chat":
        return "general_chat"
    return "knowledge_graph"


def route_after_retrieval(state: AgentState):
    intent = state.get("user_intent", "General")
    if intent in ["RTI", "Complaint"]:
        return "draft"
    else:
        return "advise"


# ── Build the pipeline ───────────────────────────────────────────────────────
#
# Flow:
#   User Message
#     → intent_router          (classify: RTI / Complaint / Legal Advice / General)
#     → knowledge_graph        (inject deterministic legal facts + jurisdiction data)
#     → retrieve_context       (hybrid RAG: BM25 + vector + reranker)
#     → draft_document         (for RTI/Complaint: full document generation)
#       OR legal_advice        (for Legal Advice/Scheme: structured advice + roadmap)
#     → verifier               (Reflexion: score output, re-draft if score < 7)
#     → END
#
# general_chat bypasses all legal processing for pure chitchat.
# ────────────────────────────────────────────────────────────────────────────

workflow = StateGraph(AgentState)

workflow.add_node("intent_router", intent_router_node)
workflow.add_node("knowledge_graph", graph_lookup_node)
workflow.add_node("retrieve_context", retrieve_context_node)
workflow.add_node("draft_document", draft_document_node)
workflow.add_node("legal_advice", legal_advice_node)
workflow.add_node("general_chat", general_chat_node)
workflow.add_node("verifier", verifier_node)          # Reflexion self-correction

workflow.set_entry_point("intent_router")

workflow.add_conditional_edges(
    "intent_router",
    route_after_intent,
    {
        "knowledge_graph": "knowledge_graph",
        "general_chat": "general_chat"
    }
)

workflow.add_edge("knowledge_graph", "retrieve_context")

workflow.add_conditional_edges(
    "retrieve_context",
    route_after_retrieval,
    {
        "draft": "draft_document",
        "advise": "legal_advice"
    }
)

# All legal responses go through verifier before reaching user
workflow.add_edge("draft_document", "verifier")
workflow.add_edge("legal_advice", "verifier")
workflow.add_edge("verifier", END)
workflow.add_edge("general_chat", END)

app = workflow.compile()
