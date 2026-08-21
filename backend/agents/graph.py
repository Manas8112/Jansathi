from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.intent_router import intent_router_node
from agents.retriever import retrieve_context_node
from agents.drafter import draft_document_node, legal_advice_node, general_chat_node

def route_after_intent(state: AgentState):
    """
    Conditional routing function based on the intent router's decision.
    """
    return state.get("next_action", "general_chat")

# Initialize the state graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("intent_router", intent_router_node)
workflow.add_node("retrieve_context", retrieve_context_node)
workflow.add_node("draft_document", draft_document_node)
workflow.add_node("legal_advice", legal_advice_node)
workflow.add_node("general_chat", general_chat_node)

# Define edges
workflow.set_entry_point("intent_router")

workflow.add_conditional_edges(
    "intent_router",
    route_after_intent,
    {
        "draft_document": "retrieve_context",
        "retrieve_context": "retrieve_context",
        "general_chat": "general_chat"
    }
)

# After retrieval, we need to know if we are drafting or advising
def route_after_retrieval(state: AgentState):
    intent = state.get("user_intent", "General")
    if intent in ["RTI", "Complaint"]:
        return "draft"
    else:
        return "advise"

workflow.add_conditional_edges(
    "retrieve_context",
    route_after_retrieval,
    {
        "draft": "draft_document",
        "advise": "legal_advice"
    }
)

# End edges
workflow.add_edge("draft_document", END)
workflow.add_edge("legal_advice", END)
workflow.add_edge("general_chat", END)

# Compile the graph
app = workflow.compile()
