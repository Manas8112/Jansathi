# JanSaathi Backend & AI Engine

The brains of JanSaathi. This backend powers the RAG pipelines, local ML intent classification, and the robust agentic orchestration.

## Tech Stack
- **API Framework:** FastAPI (Python)
- **Local Machine Learning:** HuggingFace `transformers`, `torch`, `scikit-learn`
- **Cloud LLM Fallback:** LangChain + Groq
- **Vector Database:** ChromaDB
- **Data Persistence:** SQLAlchemy (SQLite / PostgreSQL ready)

## Core Architecture
1. **Hybrid Intent Router:**
   All user queries first pass through a locally trained `InLegalBERT` model. If the confidence exceeds 0.80, it instantly triggers a specialized workflow (RTI, Complaint, etc.) completely offline. If the model is uncertain, it safely delegates to the Groq API for advanced cloud processing.
2. **Retrieval-Augmented Generation (RAG):**
   Legal drafts and civic rights answers are grounded in real Indian constitutional data injected via ChromaDB using BM25 token retrieval.
3. **Multi-Agent System:**
   - `intent_router.py`: Directs traffic intelligently.
   - `drafter.py`: Handles legal document generation based on intent.

## Setup Instructions
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Configure your API Keys:
   - Rename `.env.example` to `.env`
   - Paste your `GROQ_API_KEY`
3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

*(Note: The pre-trained local ML model is tracked via Git LFS. If you don't have it, run the scripts in `/training` to compile your own 6,000-sample model).*
