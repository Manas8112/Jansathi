from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import get_db
from auth.dependencies import get_current_user
from auth.models import User, Conversation, Message, SavedDocument
from sqlalchemy import select, delete

router = APIRouter(prefix="/api/user", tags=["user"])

@router.delete("/me")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Delete messages
        conv_result = await db.execute(select(Conversation.id).where(Conversation.user_id == current_user.id))
        conv_ids = conv_result.scalars().all()
        if conv_ids:
            await db.execute(delete(Message).where(Message.conversation_id.in_(conv_ids)))
        
        # Delete conversations and saved documents
        await db.execute(delete(Conversation).where(Conversation.user_id == current_user.id))
        await db.execute(delete(SavedDocument).where(SavedDocument.user_id == current_user.id))
        
        # Delete user
        await db.execute(delete(User).where(User.id == current_user.id))
        
        await db.commit()
        return {"message": "Account deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete account")
