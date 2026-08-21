from agents.state import AgentState
from rag.pipeline import get_rag_pipeline

def retrieve_context_node(state: AgentState):
    """
    Retrieves legal context using the Hybrid RAG Pipeline.
    """
    messages = state.get("messages", [])
    if not messages:
        return {"retrieved_context": []}
        
    query = messages[-1].content
    intent = state.get("user_intent", "General")
    
    # Use the full hybrid RAG pipeline
    pipeline = get_rag_pipeline()
    results = pipeline.retrieve(query, top_n=3)
    
    context_list = []
    for doc in results:
        context_list.append(doc["content"])
            
    return {"retrieved_context": context_list}
