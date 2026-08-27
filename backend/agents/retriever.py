from agents.state import AgentState
from rag.pipeline import get_rag_pipeline
from utils.language_utils import detect_language

def retrieve_context_node(state: AgentState):
    """
    Retrieves legal context using the Hybrid RAG Pipeline.
    """
    messages = state.get("messages", [])
    if not messages:
        return {"retrieved_context": []}
        
    latest_message = messages[-1].content
    intent = state.get("user_intent", "General")
    
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
    
    # Use the full hybrid RAG pipeline
    pipeline = get_rag_pipeline()
    results = pipeline.retrieve(search_query, top_n=3)
    
    context_list = []
    for doc in results:
        context_list.append(doc["content"])
            
    return {"retrieved_context": context_list}
