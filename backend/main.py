from dotenv import load_dotenv
load_dotenv()

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from auth.database import init_db
from auth.router import router as auth_router
from auth.dependencies import get_current_user
from auth.models import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create db tables
    await init_db()
    
    # Pre-load ML models (Embedding and Cross-Encoder) into memory
    print("Initializing Machine Learning Models (this may take a moment)...")
    from rag.pipeline import get_rag_pipeline
    get_rag_pipeline()
    print("ML Models loaded successfully!")
    
    yield
    # Shutdown

app = FastAPI(
    title="JanSaathi API",
    description="Backend for JanSaathi - AI for Civic & Legal Empowerment",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Auth Router
app.include_router(auth_router)

# Include Chat Router
from api.chat_router import router as chat_router
app.include_router(chat_router)

from api.documents import router as documents_router
app.include_router(documents_router)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "JanSaathi backend is running"}
