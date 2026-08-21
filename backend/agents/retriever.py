from agents.state import AgentState
from rag.chroma_store import search_documents

def retrieve_context_node(state: AgentState):
    """
    Retrieves legal context from ChromaDB based on the latest user message.
    """
    messages = state.get("messages", [])
    if not messages:
        return {"retrieved_context": []}
        
    query = messages[-1].content
    intent = state.get("user_intent", "General")
    
    # Optional: Filter by intent/type if we have categorized our ChromaDB collections/metadata
    # For now, we do a semantic search on the query
    results = search_documents("jansaathi_legal_kb", query, n_results=3)
    
    context_list = []
    if results and "documents" in results and results["documents"]:
        # ChromaDB returns a list of lists for documents
        for doc in results["documents"][0]:
            context_list.append(doc)
            
    return {"retrieved_context": context_list}
