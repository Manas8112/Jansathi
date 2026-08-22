import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState
from utils.llm_utils import strip_think
from langchain_core.messages import HumanMessage

# We use the fast versatile model for intent routing
llm = ChatGroq(
    model=os.getenv("MODEL_CHEAP", "openai/gpt-oss-20b"),
    temperature=0.0
)

# A structured prompt to enforce a specific output format
intent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Indian legal intent classifier. Read the user's message IN THE CONTEXT of the recent conversation and classify their true intent into exactly ONE of these categories: 'RTI' (Right to Information), 'Complaint' (Consumer dispute), 'Draft Document' (Drafting leases, contracts, notices, agreements), 'Legal Advice' (General law questions), 'Scheme Info' (Government schemes), or 'General' (Chitchat). Return ONLY the category string.\n\nRecent Conversation History:\n{history}"),
    ("user", "{message}")
])

chain = intent_prompt | llm

def intent_router_node(state: AgentState):
    """
    Analyzes the latest user message to determine their legal intent.
    """
    messages = state.get("messages", [])
    if not messages:
         return {"user_intent": "General", "next_action": "respond"}
         
    latest_message = messages[-1].content
    
    history_str = ""
    if len(messages) > 1:
        for m in messages[-5:-1]:
            role = "User" if isinstance(m, HumanMessage) else "JanSaathi"
            # Truncate long AI messages in history so the router doesn't get confused by massive text blocks
            content = m.content[:300] + "..." if len(m.content) > 300 else m.content
            history_str += f"{role}: {content}\n"
            
    response = chain.invoke({"message": latest_message, "history": history_str})
    raw_intent = response.content.strip()
    intent = strip_think(raw_intent)
    
    # Simple routing logic based on intent
    if intent in ["RTI", "Complaint", "Draft Document"]:
        next_action = "draft_document"
    elif intent in ["Legal Advice", "Scheme Info"]:
        next_action = "retrieve_context"
    else:
        next_action = "general_chat"
        
    return {"user_intent": intent, "next_action": next_action}
