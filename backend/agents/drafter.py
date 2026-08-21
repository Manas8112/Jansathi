import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from agents.state import AgentState

# We use the smarter model for complex legal drafting
llm = ChatGroq(
    model=os.getenv("MODEL_NAME", "llama-3.1-70b-versatile"),
    temperature=0.2
)

drafting_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a highly capable Indian Legal Assistant (JanSaathi). 
Your goal is to draft a legal document (like an RTI application or Consumer Complaint) based on the user's situation.
Use the provided legal context if available. 
Make sure the tone is formal, professional, and follows standard Indian legal formats.
Include placeholders like [YOUR NAME], [DATE], etc. for missing information.

Legal Context:
{context}
"""),
    ("user", "{message}")
])

def draft_document_node(state: AgentState):
    """
    Drafts a legal document based on intent and retrieved context.
    """
    messages = state.get("messages", [])
    if not messages:
        return {}
        
    latest_message = messages[-1].content
    context = "\n\n".join(state.get("retrieved_context", []))
    
    chain = drafting_prompt | llm
    response = chain.invoke({
        "message": latest_message,
        "context": context
    })
    
    # We append the AI's response to the message history
    return {
        "drafted_document": response.content,
        "messages": [AIMessage(content=response.content)]
    }

def legal_advice_node(state: AgentState):
    """
    Provides general legal advice based on retrieved context.
    """
    messages = state.get("messages", [])
    if not messages:
        return {}
        
    latest_message = messages[-1].content
    context = "\n\n".join(state.get("retrieved_context", []))
    
    advice_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a knowledgeable Indian Legal Advisor (JanSaathi).
Answer the user's question accurately using ONLY the provided legal context.
If the context does not contain the answer, politely state that you cannot provide definitive advice on that specific matter, but offer general guidance.
Ensure your response is in simple, easy-to-understand language.

Legal Context:
{context}
"""),
        ("user", "{message}")
    ])
    
    chain = advice_prompt | llm
    response = chain.invoke({
        "message": latest_message,
        "context": context
    })
    
    return {
        "messages": [AIMessage(content=response.content)]
    }

def general_chat_node(state: AgentState):
    """
    Handles general non-legal chit-chat.
    """
    messages = state.get("messages", [])
    if not messages:
        return {}
        
    latest_message = messages[-1].content
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are JanSaathi, an AI assistant for Civic and Legal Empowerment in India. Briefly and politely answer the user, and guide them back to asking legal or civic questions."),
        ("user", "{message}")
    ])
    
    chain = chat_prompt | llm
    response = chain.invoke({"message": latest_message})
    
    return {
        "messages": [AIMessage(content=response.content)]
    }
