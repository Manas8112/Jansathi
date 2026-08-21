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
    # TODO: Load ML models here
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

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "JanSaathi backend is running"}

# TODO: Add other endpoints for Chat, Document Upload, PDF Generation, etc.
