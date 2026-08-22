import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from langchain_core.messages import HumanMessage, AIMessage
from auth.dependencies import get_current_user
from auth.models import User, SavedDocument, Conversation, Message as DBMessage
from auth.database import get_db
from agents.graph import app as agent_graph
from utils.llm_utils import strip_think

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None

class ChatResponse(BaseModel):
    reply: str
    conversation_id: str
    intent: str
    confidence: str
    confidence_score: float | None = None
    citations: list[str] | None = None

@router.get("/conversations")
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of user's conversations."""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
    )
    convs = result.scalars().all()
    return [{"id": c.id, "title": c.title, "updated_at": c.updated_at} for c in convs]

@router.get("/conversations/{conv_id}")
async def get_conversation_messages(
    conv_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all messages for a specific conversation."""
    # Verify ownership
    result = await db.execute(select(Conversation).where(Conversation.id == conv_id, Conversation.user_id == current_user.id))
    conv = result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    msg_result = await db.execute(
        select(DBMessage).where(DBMessage.conversation_id == conv_id).order_by(DBMessage.id)
    )
    messages = msg_result.scalars().all()
    return [
        {"role": ("user" if m.role == "human" else "ai"), "content": m.content}
        for m in messages
    ]

@router.delete("/conversations/{conv_id}")
async def delete_conversation(
    conv_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a specific conversation."""
    result = await db.execute(select(Conversation).where(Conversation.id == conv_id, Conversation.user_id == current_user.id))
    conv = result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    await db.delete(conv)
    await db.commit()
    return {"status": "success", "message": "Conversation deleted"}

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Sends a message to the JanSaathi AI agent.
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    conv_id = request.conversation_id
    history_messages = []
    
    if not conv_id:
        # Create new conversation
        conv_id = str(uuid.uuid4())
        title = request.message[:50] + "..." if len(request.message) > 50 else request.message
        conv = Conversation(id=conv_id, user_id=current_user.id, title=title)
        db.add(conv)
    else:
        # Verify and load existing conversation
        result = await db.execute(select(Conversation).where(Conversation.id == conv_id, Conversation.user_id == current_user.id))
        conv = result.scalar_one_or_none()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Load history
        msg_result = await db.execute(
            select(DBMessage).where(DBMessage.conversation_id == conv_id).order_by(DBMessage.id)
        )
        for m in msg_result.scalars().all():
            if m.role == "human":
                history_messages.append(HumanMessage(content=m.content))
            else:
                history_messages.append(AIMessage(content=m.content))
                
    # Save the new user message
    user_db_msg = DBMessage(conversation_id=conv_id, role="human", content=request.message)
    db.add(user_db_msg)
    await db.commit()
    
    # Append the new message to history for the LLM
    history_messages.append(HumanMessage(content=request.message))
    
    # Initialize the state for the LangGraph
    initial_state = {
        "messages": history_messages,
        "conversation_id": conv_id,
        "user_intent": "Unknown",
        "extracted_entities": {},
        "retrieved_context": [],
        "drafted_document": None,
        "next_action": "",
        "jurisdiction_data": None,
        "confidence_score": None,
        "citations": None
    }
    
    try:
        # Run the graph
        final_state = agent_graph.invoke(initial_state)
        
        # Get the AI's final message
        messages = final_state.get("messages", [])
        raw_reply = messages[-1].content if messages else "I am unable to process that right now."
        # Final safety net: strip any leaked <think> tags
        reply = strip_think(raw_reply)
        
        # Remove the <document> tags from the chat reply so the user isn't spammed with text
        import re
        reply = re.sub(r'<document>.*?</document>', '', reply, flags=re.DOTALL).strip()
        
        # Save document if one was drafted
        drafted_doc = final_state.get("drafted_document")
        if drafted_doc:
            doc_type = "legal_notice"
            intent = final_state.get("user_intent", "")
            if intent == "RTI": doc_type = "rti"
            elif intent == "Complaint": doc_type = "consumer_complaint"
            
            lines = [line.strip() for line in drafted_doc.split('\n') if line.strip()]
            title = lines[0][:100] if lines else f"Drafted {doc_type}"
            if title.startswith("#"): title = title.lstrip("#").strip()
            
            saved_doc = SavedDocument(
                id=str(uuid.uuid4()),
                user_id=current_user.id,
                doc_type=doc_type,
                title=title,
                content=drafted_doc
            )
            db.add(saved_doc)
            
            # Append a notice to the reply
            reply += f"\n\n> [!NOTE]\n> A document has been drafted and saved securely. **[Click here to open your My Documents Dashboard](/dashboard)** to download it as a PDF."
        
        # Save the AI's reply
        ai_db_msg = DBMessage(conversation_id=conv_id, role="ai", content=reply)
        db.add(ai_db_msg)
        await db.commit()
        
        score = final_state.get("confidence_score")
        confidence_label = "high" if (score is None or score >= 7) else "medium" if score >= 5 else "low"
        
        return ChatResponse(
            reply=reply,
            conversation_id=conv_id,
            intent=final_state.get("user_intent", "Unknown"),
            confidence=confidence_label,
            confidence_score=score,
            citations=final_state.get("citations")
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in chat processing: {e}")
        raise HTTPException(status_code=500, detail="Internal AI Processing Error")
