"""
Documents API - Save and retrieve generated legal documents
"""
import uuid
import io
import PyPDF2
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import get_current_user
from auth.models import User, SavedDocument, Conversation, Message as DBMessage
from auth.database import get_db
from agents.analyzer import analyze_document_text

router = APIRouter(prefix="/api/documents", tags=["documents"])


class SaveDocumentRequest(BaseModel):
    doc_type: str   # "rti", "legal_notice", "consumer_complaint", "rera_complaint"
    title: str
    content: str


class DocumentResponse(BaseModel):
    id: str
    doc_type: str
    title: str
    content: str
    created_at: str


@router.post("/", response_model=DocumentResponse)
async def save_document(
    request: SaveDocumentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save a generated legal document to the user's account."""
    doc = SavedDocument(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        doc_type=request.doc_type,
        title=request.title,
        content=request.content,
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    return DocumentResponse(
        id=doc.id,
        doc_type=doc.doc_type,
        title=doc.title,
        content=doc.content,
        created_at=doc.created_at.isoformat()
    )


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all saved documents for the current user."""
    result = await db.execute(
        select(SavedDocument)
        .where(SavedDocument.user_id == current_user.id)
        .order_by(SavedDocument.created_at.desc())
    )
    docs = result.scalars().all()
    return [
        DocumentResponse(
            id=d.id,
            doc_type=d.doc_type,
            title=d.title,
            content=d.content,
            created_at=d.created_at.isoformat()
        )
        for d in docs
    ]


@router.get("/{doc_id}", response_model=DocumentResponse)
async def get_document(
    doc_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific saved document."""
    result = await db.execute(
        select(SavedDocument)
        .where(SavedDocument.id == doc_id, SavedDocument.user_id == current_user.id)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentResponse(
        id=doc.id,
        doc_type=doc.doc_type,
        title=doc.title,
        content=doc.content,
        created_at=doc.created_at.isoformat()
    )


@router.delete("/{doc_id}")
async def delete_document(
    doc_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a saved document."""
    result = await db.execute(
        select(SavedDocument)
        .where(SavedDocument.id == doc_id, SavedDocument.user_id == current_user.id)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    await db.delete(doc)
    await db.commit()
    return {"status": "deleted"}


class AnalyzeResponse(BaseModel):
    analysis: str


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_document(
    file: UploadFile = File(...),
    conversation_id: str | None = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload a PDF document to analyze for illegal or predatory clauses."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        
        extracted_text = ""
        # Read up to the first 10 pages to avoid massive context
        num_pages = min(10, len(pdf_reader.pages))
        for i in range(num_pages):
            page_text = pdf_reader.pages[i].extract_text()
            if page_text:
                extracted_text += page_text + "\n\n"
                
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract any text from the PDF")
            
        # Call the LLM analyzer
        analysis = analyze_document_text(extracted_text)
        
        # Save to conversation history if applicable
        if conversation_id:
            # Check if conversation exists
            result = await db.execute(select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == current_user.id))
            conv = result.scalar_one_or_none()
            if not conv:
                conv = Conversation(id=conversation_id, user_id=current_user.id, title=f"Analyzed {file.filename}")
                db.add(conv)
            
            # Save the human context message
            db.add(DBMessage(conversation_id=conversation_id, role="human", content=f"📎 Uploaded document for analysis: **{file.filename}**\n\nExtracted Text:\n{extracted_text[:1000]}..."))
            
            # Save the AI response
            db.add(DBMessage(conversation_id=conversation_id, role="ai", content=analysis))
            await db.commit()
        
        return AnalyzeResponse(analysis=analysis)
        
    except Exception as e:
        print(f"Error analyzing document: {e}")
        raise HTTPException(status_code=500, detail="Failed to process and analyze the document")
