from dotenv import load_dotenv
load_dotenv(encoding="utf-8-sig")

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from auth.database import init_db
from auth.router import router as auth_router
from auth.dependencies import get_current_user
from auth.models import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[DEBUG] Lifespan started. Initializing DB...")
    # Startup: create db tables
    await init_db()
    
    print("[DEBUG] DB initialized. Loading ML models...")
    # Pre-load ML models (Embedding and Cross-Encoder) into memory
    from rag.pipeline import get_rag_pipeline
    get_rag_pipeline()

    import os
    import threading
    hf_model_id = os.getenv("HF_MODEL_ID")
    if hf_model_id:
        hf_model_id = hf_model_id.replace("https://huggingface.co/", "").strip("/")
        
    hf_token = os.getenv("HF_API_TOKEN")
    
    if hf_model_id and hf_token:
        print(f"[DEBUG] Hugging Face intent model configured. Sending warm-up request to {hf_model_id}...")
        def warmup_hf():
            import requests
            import time
            try:
                # Give Render's container network interface 10 seconds to fully establish DNS resolvers
                time.sleep(10)
                url = f"https://api-inference.huggingface.co/models/{hf_model_id}"
                headers = {"Authorization": f"Bearer {hf_token}"}
                # Pinging with a dummy payload just to trigger the model to load into HF's memory
                requests.post(url, headers=headers, json={"inputs": "wake up"}, timeout=5)
                print("[DEBUG] Hugging Face model warm-up request completed.")
            except Exception as e:
                print(f"[DEBUG] Hugging Face warm-up ping failed: {e}")
        
        # Run in a background thread so it doesn't block FastAPI startup
        threading.Thread(target=warmup_hf, daemon=True).start()

    print("[DEBUG] ML Models loaded successfully! Yielding to Uvicorn...")
    
    yield
    print("[DEBUG] Shutdown initiated")

app = FastAPI(
    title="JanSaathi API",
    description="Backend for JanSaathi - AI for Civic & Legal Empowerment",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

from api.user_router import router as user_router
app.include_router(user_router)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "JanSaathi backend is running"}
