import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState

# We use the cheaper model for intent routing
llm = ChatOpenAI(
    model=os.getenv("MODEL_CHEAP", "gpt-4o-mini"),
    temperature=0.0
)

# A structured prompt to enforce a specific output format
intent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Indian legal intent classifier. Read the user's message and classify their intent into exactly ONE of these categories: 'RTI' (Right to Information), 'Complaint' (Consumer dispute), 'Legal Advice' (General law questions), 'Scheme Info' (Government schemes), or 'General' (Chitchat). Return ONLY the category string."),
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
    
    response = chain.invoke({"message": latest_message})
    intent = response.content.strip()
    
    # Simple routing logic based on intent
    if intent in ["RTI", "Complaint"]:
        next_action = "draft_document"
    elif intent in ["Legal Advice", "Scheme Info"]:
        next_action = "retrieve_context"
    else:
        next_action = "general_chat"
        
    return {"user_intent": intent, "next_action": next_action}
