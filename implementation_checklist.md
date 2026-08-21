# 🏛️ JanSaathi — Implementation Checklist
### Step-by-step build guide for AI coding assistants

> **Instructions for AI coder:** Work through each checkbox in order. Each task is self-contained with exact file paths, code expectations, and acceptance criteria. Mark `[x]` when done. Do NOT skip steps — later steps depend on earlier ones.

> **Project:** JanSaathi — AI for Civic & Legal Empowerment (Indian Hackathon)  
> **Stack:** Next.js 14 (App Router) + FastAPI (Python) + LangGraph + ChromaDB + Groq (Llama 3) + HuggingFace Local Embeddings
> **Repo Root:** `C:\Users\carpe\OOSC`

---

## Phase 0: Project Setup & Dependencies

- [x] **0.1 — Create Next.js Frontend**
  - Run: `npx -y create-next-app@latest ./frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm`
  - Working directory: `C:\Users\carpe\OOSC`
  - Verify: `frontend/` directory exists with `package.json`, `src/app/page.tsx`

- [x] **0.2 — Install frontend dependencies**
  - Working directory: `C:\Users\carpe\OOSC\frontend`
  - Run: `npm install lucide-react react-markdown remark-gfm`
  - Run: `npm install -D @types/react-markdown`

- [x] **0.3 — Add Google Fonts (Inter + DM Sans)**
  - File: `frontend/src/app/layout.tsx`
  - Import `Inter` and `DM_Sans` from `next/font/google`
  - Apply Inter as the body font, DM Sans available for headings

- [x] **0.4 — Create Python backend directory**
  - Create directory: `C:\Users\carpe\OOSC\backend`
  - Create file: `backend/requirements.txt` with:
    ```
    fastapi==0.115.0
    uvicorn[standard]==0.30.0
    python-dotenv==1.0.1
    openai==1.52.0
    langchain==0.3.7
    langchain-openai==0.2.9
    langchain-community==0.3.7
    langchain-experimental==0.3.3
    langgraph==0.2.53
    chromadb==0.5.18
    rank-bm25==0.2.2
    sentence-transformers==3.3.0
    transformers==4.46.0
    torch==2.5.0
    datasets==3.1.0
    networkx==3.4.2
    pydantic==2.9.2
    pymupdf==1.24.0
    jinja2==3.1.4
    weasyprint==63.1
    websockets==13.1
    python-jose[cryptography]==3.3.0
    passlib[bcrypt]==1.7.4
    bcrypt==4.2.0
    sqlalchemy==2.0.36
    aiosqlite==0.20.0
    ```
  - Run: `pip install -r requirements.txt` (from `backend/` directory)

- [x] **0.5 — Create `.env` files**
  - Create `backend/.env`:
    ```
    OPENAI_API_KEY=sk-your-key-here
    MODEL_NAME=gpt-4o
    MODEL_CHEAP=gpt-4o-mini
    EMBEDDING_MODEL=text-embedding-3-large
    CHROMA_PERSIST_DIR=./data/chroma_db
    JWT_SECRET=your-super-secret-key-change-this
    JWT_ALGORITHM=HS256
    JWT_EXPIRY_MINUTES=1440
    GOOGLE_CLIENT_ID=your-google-client-id
    GOOGLE_CLIENT_SECRET=your-google-client-secret
    ```
  - Create `frontend/.env.local`:
    ```
    NEXT_PUBLIC_API_URL=http://localhost:8000
    NEXTAUTH_SECRET=your-nextauth-secret
    NEXTAUTH_URL=http://localhost:3000
    NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
    ```

- [x] **0.6 — Create backend project structure**
  - Create these directories and empty `__init__.py` files:
    ```
    backend/
    ├── main.py              (FastAPI entry point)
    ├── .env
    ├── requirements.txt
    ├── auth/
    │   ├── __init__.py
    │   ├── models.py        (SQLAlchemy User model)
    │   ├── schemas.py       (Pydantic auth schemas)
    │   ├── router.py        (Auth API endpoints)
    │   ├── jwt_handler.py   (JWT token create/verify)
    │   ├── dependencies.py  (get_current_user dependency)
    │   └── database.py      (SQLite/SQLAlchemy setup)
    ├── agents/
    │   ├── __init__.py
    │   ├── graph.py         (LangGraph multi-agent orchestration)
    │   ├── supervisor.py    (Supervisor agent)
    │   ├── rti_agent.py     (RTI drafting agent)
    │   ├── rights_agent.py  (Rights navigator agent)
    │   ├── decoder_agent.py (Bureaucracy decoder agent)
    │   ├── scheme_agent.py  (Scheme matcher agent)
    │   ├── document_agent.py (Document analyzer agent)
    │   ├── form_agent.py    (Form filler agent)
    │   └── roadmap_agent.py (Action roadmap agent)
    ├── rag/
    │   ├── __init__.py
    │   ├── pipeline.py      (Hybrid RAG pipeline)
    │   ├── chunker.py       (Legal section splitter)
    │   └── ingest.py        (Data ingestion script)
    ├── knowledge/
    │   ├── __init__.py
    │   └── graph.py         (Knowledge graph)
    ├── guardrails/
    │   ├── __init__.py
    │   ├── pipeline.py      (Guardrail validation pipeline)
    │   ├── schemas.py       (Pydantic output schemas)
    │   └── verifier.py      (Citation verifier)
    ├── training/
    │   ├── __init__.py
    │   ├── intent_classifier.py  (Fine-tune intent model)
    │   └── download_datasets.py  (Download official datasets)
    ├── templates/
    │   ├── rti_form_a.jinja2
    │   ├── legal_notice.jinja2
    │   ├── consumer_complaint.jinja2
    │   └── rera_complaint.jinja2
    ├── data/
    │   ├── laws/            (Put law text files here)
    │   ├── schemes/         (Put scheme data here)
    │   ├── datasets/        (Official datasets downloaded here)
    │   └── chroma_db/       (Vector DB will be created here)
    ├── eval/
    │   ├── __init__.py
    │   ├── evaluate.py      (Evaluation framework)
    │   └── test_cases.json  (Test dataset)
    └── models/
        └── intent_classifier/  (Trained model saved here)
    ```

---

## Phase 0.5: Authentication & Login System

- [ ] **0.5.1 — Install frontend auth dependencies**
  - Working directory: `C:\Users\carpe\OOSC\frontend`
  - Run: `npm install next-auth@latest @auth/core`
  - Run: `npm install js-cookie`
  - Run: `npm install -D @types/js-cookie`

- [ ] **0.5.2 — Create backend database setup (SQLite + SQLAlchemy)**
  - File: `backend/auth/database.py`
  - Implement:
    ```python
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
    from sqlalchemy.orm import DeclarativeBase
    
    DATABASE_URL = "sqlite+aiosqlite:///./data/jansaathi.db"
    
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    class Base(DeclarativeBase):
        pass
    
    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def get_db() -> AsyncSession:
        async with async_session() as session:
            yield session
    ```
  - Uses SQLite (zero config, file-based — perfect for hackathon)
  - DB file created at `backend/data/jansaathi.db`

- [x] **0.5.3 — Create User model**
  - File: `backend/auth/models.py`
  - Implement SQLAlchemy models:
    ```python
    from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Text
    from sqlalchemy.orm import relationship
    import uuid
    from datetime import datetime
    
    class User(Base):
        __tablename__ = "users"
        
        id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
        email = Column(String, unique=True, index=True, nullable=False)
        name = Column(String, nullable=False)
        hashed_password = Column(String, nullable=True)  # null for Google OAuth users
        avatar_url = Column(String, nullable=True)
        provider = Column(String, default="email")  # "email" or "google"
        is_active = Column(Boolean, default=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        last_login = Column(DateTime, default=datetime.utcnow)
        
        # Relationships
        conversations = relationship("Conversation", back_populates="user")
        saved_documents = relationship("SavedDocument", back_populates="user")
    
    class Conversation(Base):
        __tablename__ = "conversations"
        
        id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
        user_id = Column(String, ForeignKey("users.id"), nullable=False)
        title = Column(String, default="New Conversation")
        mode = Column(String, default="chat")  # chat/rti/rights/decode/scheme
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        user = relationship("User", back_populates="conversations")
        messages = relationship("Message", back_populates="conversation")
    
    class Message(Base):
        __tablename__ = "messages"
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
        role = Column(String, nullable=False)  # "user" or "assistant"
        content = Column(Text, nullable=False)
        metadata_json = Column(Text, nullable=True)  # JSON string for citations, roadmap, etc.
        created_at = Column(DateTime, default=datetime.utcnow)
        
        conversation = relationship("Conversation", back_populates="messages")
    
    class SavedDocument(Base):
        __tablename__ = "saved_documents"
        
        id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
        user_id = Column(String, ForeignKey("users.id"), nullable=False)
        doc_type = Column(String)  # "rti", "legal_notice", "complaint"
        title = Column(String)
        content = Column(Text)
        created_at = Column(DateTime, default=datetime.utcnow)
        
        user = relationship("User", back_populates="saved_documents")
    ```
  - This gives us: user accounts, conversation history, message persistence, and saved documents

- [x] **0.5.4 — Create auth Pydantic schemas**
  - File: `backend/auth/schemas.py`
  - Implement:
    ```python
    class UserRegister(BaseModel):
        email: EmailStr
        name: str
        password: str  # min 8 chars
    
    class UserLogin(BaseModel):
        email: EmailStr
        password: str
    
    class GoogleLogin(BaseModel):
        token: str  # Google OAuth token from frontend
    
    class UserResponse(BaseModel):
        id: str
        email: str
        name: str
        avatar_url: str | None
        provider: str
        created_at: datetime
    
    class TokenResponse(BaseModel):
        access_token: str
        token_type: str = "bearer"
        user: UserResponse
    
    class ConversationResponse(BaseModel):
        id: str
        title: str
        mode: str
        created_at: datetime
        updated_at: datetime
        message_count: int
    ```

- [x] **0.5.5 — Create JWT handler**
  - File: `backend/auth/jwt_handler.py`
  - Implement:
    ```python
    from jose import jwt, JWTError
    from passlib.context import CryptContext
    from datetime import datetime, timedelta
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(password: str) -> str
    def verify_password(plain: str, hashed: str) -> bool
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str
    def decode_access_token(token: str) -> dict  # raises JWTError if invalid
    ```

- [x] **0.5.6 — Create auth dependency (get_current_user)**
  - File: `backend/auth/dependencies.py`
  - Implement:
    ```python
    from fastapi import Depends, HTTPException, status
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    
    security = HTTPBearer()
    
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        """Extract and validate JWT from Authorization header.
        Returns the User object or raises 401."""
    
    # Optional: allows unauthenticated access
    async def get_optional_user(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        db: AsyncSession = Depends(get_db)
    ) -> User | None:
    ```

- [x] **0.5.7 — Create auth API router**
  - File: `backend/auth/router.py`
  - Implement these endpoints:
    ```
    POST /api/auth/register
      → Body: {email, name, password}
      → Creates user, returns JWT + user data
      → Hash password with bcrypt
      → Return 409 if email already exists
    
    POST /api/auth/login
      → Body: {email, password}
      → Verify password, return JWT + user data
      → Return 401 if invalid credentials
    
    POST /api/auth/google
      → Body: {token} (Google OAuth ID token)
      → Verify token with Google's API
      → Create user if doesn't exist (auto-register)
      → Return JWT + user data
    
    GET /api/auth/me
      → Requires: Authorization Bearer token
      → Returns current user profile
    
    GET /api/auth/conversations
      → Requires: auth
      → Returns user's conversation history (list)
    
    GET /api/auth/conversations/{id}/messages
      → Requires: auth
      → Returns messages for a specific conversation
    
    GET /api/auth/documents
      → Requires: auth
      → Returns user's saved documents (RTIs, notices, etc.)
    
    DELETE /api/auth/conversations/{id}
      → Requires: auth
      → Deletes a conversation
    ```

- [x] **0.5.8 — Wire auth router into FastAPI main.py**
  - In `backend/main.py`:
    - Import and include the auth router: `app.include_router(auth_router)`
    - Call `init_db()` on startup to create tables
    - Protect the `/api/chat` endpoint: add `current_user: User = Depends(get_current_user)`
    - Save messages to DB in the chat endpoint (both user message and AI response)
    - Auto-create a conversation if `conversation_id` is "new"

- [x] **0.5.9 — Build frontend login page**
  - File: `frontend/src/app/login/page.tsx`
  - Full login/register page with:
    - **Login tab:** email + password fields + "Login" button
    - **Register tab:** name + email + password + confirm password + "Register" button
    - **Google Sign-In button:** "Continue with Google" (using Google Identity Services)
    - Styled to match the dark theme with amber accent
    - Form validation (email format, password min 8 chars, passwords match)
    - Error messages (invalid credentials, email taken, etc.)
    - Redirect to main app after successful login
    - **Design:** centered card on dark background, glassmorphism effect, app logo at top

- [x] **0.5.10 — Build frontend auth context/provider**
  - File: `frontend/src/lib/auth.tsx`
  - Create `AuthProvider` context that:
    - Stores user data + JWT token in state
    - Persists token in `localStorage` (or cookies via `js-cookie`)
    - Provides `login(email, password)`, `register(name, email, password)`, `googleLogin(token)`, `logout()` functions
    - Provides `user` object and `isAuthenticated` boolean
    - Auto-checks token validity on app load (calls `/api/auth/me`)
    - Redirects to `/login` if token is expired/invalid
  - Wrap the app with `AuthProvider` in `layout.tsx`

- [x] **0.5.11 — Build frontend protected route wrapper**
  - File: `frontend/src/components/ProtectedRoute.tsx`
  - Component that:
    - Checks if user is authenticated
    - If not → redirect to `/login`
    - If yes → render children
    - Shows loading spinner while checking auth status
  - Wrap the main page (`page.tsx`) with this component

- [x] **0.5.12 — Add user profile & history to frontend**
  - File: `frontend/src/components/UserMenu.tsx`
  - Top-right corner of the app:
    - User avatar (or initials circle) + name
    - Dropdown menu:
      - "📋 My Conversations" — opens sidebar/modal with conversation history
      - "📄 Saved Documents" — shows saved RTIs, notices, complaints
      - "⚙️ Settings" (placeholder)
      - "🚪 Logout"
  - File: `frontend/src/components/ConversationHistory.tsx`
  - Sidebar or modal showing:
    - List of past conversations with title, date, mode icon
    - Click to load and continue a past conversation
    - Delete button (swipe or icon) for each conversation

- [x] **0.5.13 — Add "Save Document" functionality**
  - When a document is generated (RTI, legal notice, complaint):
    - Add a "💾 Save to My Documents" button on the `DocumentCard` component
    - Calls `POST /api/auth/documents` with document content
    - Shows "✅ Saved!" confirmation
    - Saved documents appear in the user's "My Documents" section

- [x] **0.5.14 — Update API client with auth headers**
  - File: `frontend/src/lib/api.ts`
  - All API calls should include: `Authorization: Bearer <token>` header
  - Add interceptor: if 401 response → redirect to login page
  - Add functions: `getConversations()`, `getMessages(conversationId)`, `getSavedDocuments()`

---

## Phase 1: Legal Data Collection & Ingestion

- [ ] **1.1 — Download/create law text files**
  - Create `backend/data/laws/rti_act_2005.txt`
    - Go to `https://indiacode.nic.in` and search "Right to Information Act 2005"
    - Copy the full text of the Act (all sections, schedules)
    - Save as plain text
  - Create `backend/data/laws/rti_rules_2012.txt`
    - RTI Rules 2012 from same source
  - Create `backend/data/laws/consumer_protection_act_2019.txt`
    - Consumer Protection Act 2019, focus on Sections 2, 34-36, 69
  - Create `backend/data/laws/indian_contract_act_1872.txt`
    - Focus on Sections 73, 74, 124 (security deposits, breach)
  - Create `backend/data/laws/karnataka_rent_act_1961.txt`
    - Karnataka Rent Control Act
  - Create `backend/data/laws/maharashtra_rent_act_1999.txt`
    - Maharashtra Rent Control Act
  - Create `backend/data/laws/rera_act_2016.txt`
    - RERA Act, focus on Sections 18, 31, 38

- [ ] **1.2 — Create scheme eligibility data**
  - Create `backend/data/schemes/schemes.json` with structured data:
    ```json
    [
      {
        "id": "pmay",
        "name": "PM Awas Yojana (PMAY)",
        "description": "Housing subsidy for economically weaker sections",
        "benefit": "Subsidy up to ₹2.67 lakh for home loan",
        "eligibility": {
          "income_limit": 1800000,
          "categories": ["EWS", "LIG", "MIG-I", "MIG-II"],
          "requirements": ["No house owned by any family member in India", "First-time home buyer"],
          "applicable_to": ["all"]
        },
        "documents_needed": ["Aadhaar", "Income certificate", "Address proof", "Bank account"],
        "where_to_apply": "Nearest bank branch or Housing.com portal",
        "website": "https://pmaymis.gov.in"
      }
    ]
    ```
  - Include entries for: PMAY, Ayushman Bharat, PM Kisan, PMMVY, PM SVANidhi, PM Mudra Yojana, Sukanya Samriddhi, PMSYM, Atal Pension Yojana, PM Ujjwala Yojana (at least 10 schemes)

- [ ] **1.3 — Build the legal section splitter**
  - File: `backend/rag/chunker.py`
  - Implement `LegalSectionSplitter` class:
    - Input: raw text of a law
    - Split on patterns like `Section \d+`, `Chapter \w+`, `Schedule \w+`
    - Each chunk must have metadata: `section_number`, `act_name`, `chapter`, `chunk_type`
    - Keep chunks between 200-1000 tokens (don't split mid-sentence)
    - Preserve cross-references (e.g., "as mentioned in Section 8")
  - Also implement `SemanticChunkerWrapper` that uses LangChain's `SemanticChunker`
  - Export a `chunk_legal_document(text: str, act_name: str) -> list[Document]` function

- [ ] **1.4 — Build the data ingestion pipeline**
  - File: `backend/rag/ingest.py`
  - Implement `ingest_all()` function:
    1. Load all `.txt` files from `backend/data/laws/`
    2. For each file, run through `LegalSectionSplitter`
    3. Create OpenAI embeddings using `text-embedding-3-large`
    4. Store in ChromaDB at `backend/data/chroma_db/`
    5. Also build a BM25 index (pickle it to `backend/data/bm25_index.pkl`)
    6. Print stats: number of chunks, number of unique sections
  - Make it runnable as a script: `python -m rag.ingest`
  - Should be idempotent (delete and recreate collection if exists)

- [ ] **1.5 — Run the ingestion pipeline**
  - Working directory: `C:\Users\carpe\OOSC\backend`
  - Run: `python -m rag.ingest`
  - Verify: `backend/data/chroma_db/` has data, prints chunk count

---

## Phase 2: Knowledge Graph

- [x] **2.1 — Build the legal knowledge graph**
  - File: `backend/knowledge/graph.py`
  - Using `networkx.DiGraph`, create a 5-layer graph:
    - **Layer 1 — Laws:** RTI Act 2005, Consumer Protection Act 2019, RERA 2016, Karnataka Rent Act 1961, Maharashtra Rent Act 1999, Indian Contract Act 1872, Labour Codes 2020
    - **Layer 2 — Sections:** Key sections from each law (at least 20 section nodes total)
    - **Layer 3 — Rights:** At least 10 right nodes (right to information, right to refund, right to deposit return, right to fair rent, right to delayed possession compensation, right to safe workplace, etc.)
    - **Layer 4 — Remedies:** At least 8 remedy nodes (file RTI, send legal notice, consumer forum, RERA complaint, police complaint, labour tribunal, first appeal RTI, second appeal RTI)
    - **Layer 5 — Forms/Templates:** Link each remedy to its template file
  - Edges: `contains`, `grants`, `exercised_by` (with priority), `requires_form`, `escalates_to`
  - Export functions:
    - `get_rights_for_problem(problem_type: str, state: str) -> dict`
    - `get_remedies_for_right(right_id: str) -> list[dict]`
    - `get_escalation_path(remedy_id: str) -> list[dict]`
    - `get_applicable_law(problem_type: str, state: str) -> dict`
  - Include a `PROBLEM_TYPE_MAP` dict mapping problem keywords to right nodes

- [x] **2.2 — Add PIO/Authority lookup data**
  - In `backend/knowledge/graph.py`, add a `AUTHORITY_DIRECTORY` dict:
    ```python
    AUTHORITY_DIRECTORY = {
        "rti": {
            "central": {
                "default_pio": "Public Information Officer, [Department Name]",
                "fee": "₹10",
                "payment_modes": ["IPO", "DD", "Court Fee Stamp", "Online"],
                "appeal_authority": "First Appellate Authority under Section 19(1)",
                "second_appeal": "Central Information Commission"
            },
            "state": {
                "Karnataka": {"fee": "₹10", "appeal": "Karnataka Information Commission"},
                "Maharashtra": {"fee": "₹10", "appeal": "Maharashtra Information Commission"},
                "Delhi": {"fee": "₹10", "appeal": "Delhi Information Commission"},
                "Uttar Pradesh": {"fee": "₹10", "appeal": "UP Information Commission"},
                "Tamil Nadu": {"fee": "₹10", "appeal": "Tamil Nadu Information Commission"},
            }
        },
        "consumer": {
            "district_forum": {"jurisdiction": "Up to ₹1 crore", "portal": "edaakhil.nic.in"},
            "state_commission": {"jurisdiction": "₹1 crore to ₹10 crore"},
            "national_commission": {"jurisdiction": "Above ₹10 crore", "location": "New Delhi"},
            "helpline": "1800-11-4000 (National Consumer Helpline)"
        },
        "rera": {
            "Karnataka": {"portal": "rera.karnataka.gov.in"},
            "Maharashtra": {"portal": "maharera.mahaonline.gov.in"},
        },
        "legal_aid": {
            "nalsa": "nalsa.gov.in",
            "tele_law": "1800-XXX-XXXX",
            "helpline": "15100"
        }
    }
    ```
  - Export a function: `find_authority(case_type: str, state: str, department: str = None) -> dict`

- [x] **2.3 — RAG Retrieval Node**
  - File: `backend/rag/pipeline.py`
  - Implement `HybridRAGPipeline` class with:
    1. `__init__()`: Load ChromaDB collection + BM25 index from disk
    2. `_vector_search(query, k=10)`: MMR search on ChromaDB
    3. `_bm25_search(query, k=10)`: BM25 keyword search
    4. `_hybrid_merge(vector_results, bm25_results, weights=[0.6, 0.4])`: EnsembleRetriever logic — combine and deduplicate results
    5. `_rerank(query, candidates, top_n=5)`: Cross-encoder reranking using `cross-encoder/ms-marco-MiniLM-L-12-v2` from HuggingFace
    6. `_expand_query(query) -> list[str]`: Use GPT-4o-mini to generate 3 alternative legal phrasings of the user query
    7. `retrieve(query: str, filters: dict = None) -> list[Document]`: Full pipeline — expand → hybrid search → rerank → return top 5 with scores
  - Each returned document should include: `page_content`, `metadata` (act_name, section_number), `relevance_score`

- [x] **2.4 — Legal Context & Drafting Node**
  - File: `backend/agents/rti_agent.py`
  - Implement `rti_drafting_agent(state: JanSaathiState) -> JanSaathiState`:
    - Input: user's plain-language RTI query + retrieved legal context
    - Extract: department, state, time period, specific info requested
    - If missing info → return follow-up question to ask user
    - If complete → look up PIO from authority directory
    - Generate RTI using template + LLM to craft information points
    - Output: filled `RTIApplication` schema + rendered template
    - Always cite Section 6(1), include fee info, include 30-day timeline

- [x] **2.5 — Master Graph Assembly**
  - File: `backend/agents/graph.py`
  - Build the `StateGraph`:
    1. Entry: supervisor
    2. Supervisor → intent classifier (use fine-tuned model)
    3. Intent classifier → conditional routing to the correct agent
    4. Each agent → RAG retriever (if needed) → agent logic
    5. Agent output → roadmap generator
    6. Roadmap → guardrail pipeline
    7. Guardrail → response builder → END
  - Add memory (SqliteSaver) for multi-turn conversation
  - Compile the graph
  - Export `run_agent(user_message: str, conversation_id: str) -> dict`

---

## Phase 3: Hybrid RAG Pipeline

- [x] **3.1 — Build the hybrid RAG retriever**
  - File: `backend/rag/pipeline.py`
  - Implement `HybridRAGPipeline` class with:
    1. `__init__()`: Load ChromaDB collection + BM25 index from disk
    2. `_vector_search(query, k=10)`: MMR search on ChromaDB
    3. `_bm25_search(query, k=10)`: BM25 keyword search
    4. `_hybrid_merge(vector_results, bm25_results, weights=[0.6, 0.4])`: EnsembleRetriever logic — combine and deduplicate results
    5. `_rerank(query, candidates, top_n=5)`: Cross-encoder reranking using `cross-encoder/ms-marco-MiniLM-L-12-v2` from HuggingFace
    6. `_expand_query(query) -> list[str]`: Use GPT-4o-mini to generate 3 alternative legal phrasings of the user query
    7. `retrieve(query: str, filters: dict = None) -> list[Document]`: Full pipeline — expand → hybrid search → rerank → return top 5 with scores
  - Each returned document should include: `page_content`, `metadata` (act_name, section_number), `relevance_score`

- [x] **3.2 — Test the RAG pipeline**
  - Create `backend/rag/test_rag.py`:
    - Test queries:
      1. "How to file RTI application"
      2. "landlord not returning security deposit Bangalore"
      3. "consumer complaint for defective product"
      4. "delayed possession compensation RERA"
    - For each: print the top 5 results with scores and metadata
    - Verify that results are relevant and citations are correct
  - Run: `python -m rag.test_rag`

---

## Phase 4: Fine-Tuned Intent Classifier

- [x] **4.1 — Download official datasets (NOT GPT-generated)**
  - File: `backend/training/download_datasets.py`
  - Script that downloads and processes these **real, official datasets**:
  
  **Dataset 1: RTI-Bench (HuggingFace)**
  - Source: `huggingface.co/datasets/joyboseroy/rti-bench`
  - Download: `datasets.load_dataset("joyboseroy/rti-bench")`
  - Contains: Central Information Commission (CIC) decisions with outcome labels, exemption citations, reasoning
  - Use for: RTI intent classification, understanding RTI query patterns
  - Label mapping: extract query text → label as `rti`
  
  **Dataset 2: Grahak-Nyay Consumer Complaints (GitHub)**
  - Source: `github.com/ShreyGanatra/GrahakNyay`
  - Contains: `GeneralQA`, `SectoralQA`, `NyayChat` (annotated chatbot conversations for consumer grievance)
  - Use for: Consumer complaint intent classification + conversational patterns
  - Label mapping: extract complaint text → label as `consumer`
  
  **Dataset 3: Indian Legal Knowledge Base (HuggingFace)**
  - Source: `huggingface.co/datasets/d-riti/Dataset-For-Indian-Legal-Knowledge-Base`
  - Contains: Bilingual (English/Hindi) legal corpus — court judgments, statutes
  - Use for: Legal text understanding, decode/document intent samples
  - Label mapping: extract question text → label as `decode` or `document`
  
  **Dataset 4: Indian Law Dataset (HuggingFace)**
  - Source: `huggingface.co/datasets/169Pi/indian_law`
  - Contains: ~50M tokens of Indian jurisprudence with chain-of-thought reasoning
  - Use for: Legal reasoning training data, extracting tenant/workplace dispute patterns
  - Label mapping: filter by topic → label as `tenant`, `workplace`
  
  **Dataset 5: CIVICS Dataset (HuggingFace)**
  - Source: `huggingface.co/datasets/CIVICS-dataset/CIVICS`
  - Contains: Civic discourse and rights-based content
  - Use for: General civic intent classification
  
  **Dataset 6: Indian Government Schemes (Kaggle)**
  - Source: Kaggle — search "Indian Government Schemes"
  - Contains: Scheme names, eligibility criteria, benefits in CSV format
  - Use for: Scheme intent classification + enriching `schemes.json` with real data
  - Label mapping: generate eligibility questions from scheme data → label as `scheme`
  
  **Dataset 7: RTI Case Dataset (HuggingFace)**
  - Source: `huggingface.co/datasets/jatinmehra/RTI-CASE-DATASET`
  - Contains: RTI case documents for procedural and subject-matter classification
  - Use for: Additional RTI training samples
  
  - **Processing pipeline** (in `download_datasets.py`):
    ```python
    from datasets import load_dataset
    
    def download_and_process_all():
        all_samples = []
        
        # 1. RTI-Bench
        rti_bench = load_dataset("joyboseroy/rti-bench")
        for row in rti_bench["train"]:
            all_samples.append({"text": extract_query(row), "label": "rti"})
        
        # 2. Grahak-Nyay (clone repo or download files)
        # Process GeneralQA.json and NyayChat.json
        for row in grahak_nyay_data:
            all_samples.append({"text": row["question"], "label": "consumer"})
        
        # 3. Indian Legal KB
        legal_kb = load_dataset("d-riti/Dataset-For-Indian-Legal-Knowledge-Base")
        for row in legal_kb["train"]:
            label = classify_legal_topic(row)  # tenant/workplace/decode
            all_samples.append({"text": row["question"], "label": label})
        
        # 4. Government Schemes (Kaggle CSV)
        schemes_df = pd.read_csv("data/datasets/indian_govt_schemes.csv")
        for _, row in schemes_df.iterrows():
            # Generate natural questions from scheme data
            questions = generate_scheme_questions(row)
            for q in questions:
                all_samples.append({"text": q, "label": "scheme"})
        
        # 5. Balance classes — undersample majority, oversample minority
        balanced = balance_dataset(all_samples, target_per_class=200)
        
        # Save
        with open("data/datasets/intent_data.json", "w") as f:
            json.dump(balanced, f, indent=2)
        
        print(f"Total samples: {len(balanced)}")
        for label in LABELS:
            count = sum(1 for s in balanced if s['label'] == label)
            print(f"  {label}: {count}")
    ```
  - Run: `python -m training.download_datasets`
  - Target: ~200 samples per class, 7 classes = ~1400 total samples
  - Save processed data to: `backend/data/datasets/intent_data.json`

- [x] **4.1b — Download pre-trained InLegalBERT (Indian Legal BERT)**
  - Instead of generic `distilbert-base-uncased`, use **InLegalBERT** as base model:
  - Source: `huggingface.co/law-ai/InLegalBERT`
  - This model is **pre-trained on Indian legal texts** (Supreme Court + High Court judgments)
  - Much better than generic BERT for legal domain tasks
  - Download:
    ```python
    from transformers import AutoTokenizer, AutoModel
    tokenizer = AutoTokenizer.from_pretrained("law-ai/InLegalBERT")
    model = AutoModel.from_pretrained("law-ai/InLegalBERT")
    ```
  - This is a **real research model** from IIT Kharagpur — very impressive for judges

- [x] **4.2 — Train the intent classifier on official data**
  - File: `backend/training/intent_classifier.py`
  - Fine-tune **InLegalBERT** (`law-ai/InLegalBERT`) on the processed official dataset:
    1. Load processed data from `data/datasets/intent_data.json`
    2. Tokenize with InLegalBERT tokenizer
    3. Train/test split: 80/20
    4. Add classification head: `AutoModelForSequenceClassification.from_pretrained("law-ai/InLegalBERT", num_labels=7)`
    5. Train for 10 epochs, batch size 16, learning rate 2e-5
    6. Evaluate on test set — print accuracy, per-class precision/recall, confusion matrix
    7. Save model to `backend/models/intent_classifier/`
  - Target: >90% accuracy on test set (InLegalBERT should perform better than generic BERT on legal text)
  - Make runnable: `python -m training.intent_classifier`
  - **For presentation:** show that you used real datasets (RTI-Bench, Grahak-Nyay) + domain-specific model (InLegalBERT) — this is way more credible than GPT-generated data

- [ ] **4.3 — Create inference wrapper**
  - File: `backend/training/intent_classifier.py` (add to existing)
  - Add `IntentClassifier` class:
    ```python
    class IntentClassifier:
        def __init__(self, model_path="./models/intent_classifier"):
            # Load saved model and tokenizer
        
        def classify(self, text: str) -> dict:
            # Returns: {"intent": "tenant", "confidence": 0.94, "all_scores": {...}}
        
        def classify_batch(self, texts: list[str]) -> list[dict]:
            # Batch inference
    ```
  - Fallback: if model files don't exist, use LLM-based classification with a prompt

---

## Phase 5: Guardrails & Output Validation

- [x] **5.1 — Define Pydantic output schemas**
  - File: `backend/guardrails/schemas.py`
  - Define these models:
    ```python
    class LawCitation(BaseModel):
        act_name: str
        section: str
        relevance: str
    
    class Remedy(BaseModel):
        name: str
        priority: int
        cost: str
        timeline: str
        difficulty: Literal["easy", "medium", "hard"]
        description: str
    
    class ActionStep(BaseModel):
        step_number: int
        action: str
        deadline: str | None
        details: str
    
    class LegalResponse(BaseModel):
        summary: str
        applicable_laws: list[LawCitation]   # min 1
        rights_identified: list[str]
        remedies: list[Remedy]
        action_steps: list[ActionStep]
        confidence: Literal["high", "medium", "low"]
        disclaimer: str
        escalation_needed: bool
    
    class RTIApplication(BaseModel):
        addressed_to: str
        department: str
        subject: str
        information_points: list[str]
        fee_info: str
        applicant_placeholder: str
        date: str
        legal_reference: str
        next_steps: list[str]
    
    class LegalNotice(BaseModel):
        addressed_to: str
        subject: str
        facts: list[str]
        legal_basis: list[LawCitation]
        demand: str
        deadline_days: int
        consequence: str
    
    class SchemeMatch(BaseModel):
        scheme_name: str
        eligibility_status: Literal["eligible", "likely_eligible", "check_locally"]
        benefit: str
        documents_needed: list[str]
        where_to_apply: str
        website: str | None
    ```

- [x] **5.2 — Build citation verifier**
  - File: `backend/guardrails/verifier.py`
  - Implement `CitationVerifier` class:
    - `__init__(knowledge_graph)`: Takes the knowledge graph
    - `verify(response: LegalResponse) -> dict`: Checks each `LawCitation` against the knowledge graph nodes
    - Returns: `{"all_verified": bool, "details": [...], "unverified_count": int}`
    - Includes fuzzy matching for slight section format differences (e.g., "S.6" vs "Section 6" vs "S 6(1)")

- [x] **5.3 — Build hallucination detector**
  - File: `backend/guardrails/pipeline.py`
  - Implement `HallucinationDetector` class:
    - `check(response_text: str, retrieved_context: list[str]) -> dict`
    - Uses GPT-4o-mini to verify if each claim in the response is grounded in the retrieved context
    - Returns: `{"is_grounded": bool, "grounding_score": float, "unsupported_claims": [...]}`

- [x] **5.4 — Build confidence scorer**
  - File: `backend/guardrails/pipeline.py`
  - Implement `ConfidenceScorer` class:
    - Inputs: retrieval scores, citation verification result, grounding result, intent confidence
    - Weighted formula: `0.3*retrieval + 0.3*citation + 0.25*grounding + 0.15*intent`
    - Returns level: "high" (>0.85), "medium" (>0.65), "low" (<=0.65)
    - Low confidence → response is replaced with escalation message

- [ ] **5.5 — Build full guardrail pipeline**
  - File: `backend/guardrails/pipeline.py`
  - Implement `guardrail_pipeline(llm_response, retrieved_context, state) -> LegalResponse`:
    1. Parse LLM response into `LegalResponse` (reject if malformed, retry once)
    2. Run citation verifier
    3. Run hallucination detector
    4. Compute confidence score
    5. If low confidence → return escalation response with legal aid links
    6. If unverified citations → strip them, add warning
    7. Always inject mandatory disclaimer
    8. Return validated `LegalResponse`

---

## Phase 6: Document Templates

- [ ] **6.1 — Create RTI application template**
  - File: `backend/templates/rti_form_a.jinja2`
  - Jinja2 template for a properly formatted RTI application:
    - Addressed to the PIO with designation and department
    - Subject line citing Section 6(1)
    - Numbered list of information points requested
    - Fee declaration
    - Applicant details placeholder
    - Date
    - Section 7(1) reference for 30-day timeline

- [ ] **6.2 — Create legal notice template**
  - File: `backend/templates/legal_notice.jinja2`
  - Formal legal notice template:
    - LEGAL NOTICE header
    - "Under Section [X] of [Act]" reference
    - Facts of the case (numbered)
    - Legal basis with citations
    - Demand with deadline (15 days)
    - Consequence clause (consumer forum / police complaint)
    - Sender details placeholder

- [ ] **6.3 — Create consumer complaint template**
  - File: `backend/templates/consumer_complaint.jinja2`
  - Consumer forum complaint format:
    - "Before the District Consumer Disputes Redressal Forum, [City]"
    - Complainant details
    - Opposite Party details
    - Facts of the case
    - Deficiency in service / defect in goods
    - Relief sought (refund + compensation + litigation cost)
    - Applicable law citations
    - Verification and signature block

- [ ] **6.4 — Create RERA complaint template**
  - File: `backend/templates/rera_complaint.jinja2`
  - RERA complaint format:
    - Addressed to State RERA Authority
    - Project details and agreement details
    - Nature of complaint (delayed possession / quality / etc.)
    - Section 18 reference for compensation
    - Relief sought

- [ ] **6.5 — Create template renderer**
  - File: `backend/utils/template_renderer.py`
  - Implement `render_template(template_name: str, data: dict) -> str`:
    - Load Jinja2 template from `templates/` directory
    - Fill with provided data
    - Return formatted string
  - Implement `render_to_pdf(template_name: str, data: dict) -> bytes`:
    - Render template to HTML, then convert to PDF using WeasyPrint
    - Return PDF bytes

---

## Phase 7: LangGraph Multi-Agent System

- [ ] **7.1 — Define agent state**
  - File: `backend/agents/graph.py`
  - Define `JanSaathiState(MessagesState)`:
    ```python
    class JanSaathiState(MessagesState):
        intent: str
        intent_confidence: float
        case_type: str
        jurisdiction: str
        state: str
        user_profile: dict
        retrieved_context: list
        retrieval_scores: list
        draft_document: str
        document_type: str
        confidence_score: float
        citations: list
        action_roadmap: dict
        requires_escalation: bool
        current_step: str
    ```

- [ ] **7.2 — Build supervisor agent**
  - File: `backend/agents/supervisor.py`
  - Implement `supervisor_agent(state: JanSaathiState) -> JanSaathiState`:
    - Manages conversation state
    - Decides if we need more info from the user (multi-turn)
    - Tracks which agents have been called
    - Handles conversation memory

- [ ] **7.3 — Build RTI drafting agent**
  - File: `backend/agents/rti_agent.py`
  - Implement `rti_drafting_agent(state: JanSaathiState) -> JanSaathiState`:
    - Input: user's plain-language RTI query + retrieved legal context
    - Extract: department, state, time period, specific info requested
    - If missing info → return follow-up question to ask user
    - If complete → look up PIO from authority directory
    - Generate RTI using template + LLM to craft information points
    - Output: filled `RTIApplication` schema + rendered template
    - Always cite Section 6(1), include fee info, include 30-day timeline

- [ ] **7.4 — Build rights navigator agent**
  - File: `backend/agents/rights_agent.py`
  - Implement `rights_navigator_agent(state: JanSaathiState) -> JanSaathiState`:
    - Input: user's problem description + retrieved context
    - Use knowledge graph to find applicable rights and remedies
    - Use LLM to personalize the explanation based on user's specific details
    - Output: `LegalResponse` with rights, remedies (ranked by priority), and action steps
    - Include state-specific law references

- [ ] **7.5 — Build bureaucracy decoder agent**
  - File: `backend/agents/decoder_agent.py`
  - Implement `bureaucracy_decoder_agent(state: JanSaathiState) -> JanSaathiState`:
    - Input: confusing legal/government text pasted by user
    - Use LLM to:
      1. Identify what type of document/text it is
      2. Break down into plain-language bullet points
      3. Identify the applicable law area
      4. Flag any rights violations in the text
      5. Suggest what action the user should take
    - Output: decoded summary + rights flags + suggested next steps

- [ ] **7.6 — Build scheme matcher agent**
  - File: `backend/agents/scheme_agent.py`
  - Implement `scheme_matcher_agent(state: JanSaathiState) -> JanSaathiState`:
    - Input: user profile (state, age, gender, income, category, occupation, need)
    - Load scheme data from `schemes.json`
    - Match against eligibility criteria
    - Use LLM to generate personalized explanation for each matched scheme
    - Output: list of `SchemeMatch` objects with eligibility status

- [ ] **7.7 — Build document analyzer agent**
  - File: `backend/agents/document_agent.py`
  - Implement `document_analyzer_agent(state: JanSaathiState) -> JanSaathiState`:
    - Input: extracted text from uploaded document
    - Use LLM + RAG to:
      1. Summarize the document
      2. Identify key terms, obligations, amounts, dates
      3. Flag unfair/illegal clauses against applicable law
      4. List user's rights not mentioned in the document
    - Output: analysis with summary, key terms, red flags, rights

- [ ] **7.8 — Build form filler agent**
  - File: `backend/agents/form_agent.py`
  - Implement `form_filler_agent(state: JanSaathiState) -> JanSaathiState`:
    - Input: conversation history where user has answered questions
    - Extract all form fields from conversation
    - Select appropriate template based on case type
    - Fill template with extracted data
    - Output: rendered form/complaint ready for download

- [ ] **7.9 — Build roadmap generator agent**
  - File: `backend/agents/roadmap_agent.py`
  - Implement `roadmap_generator_agent(state: JanSaathiState) -> JanSaathiState`:
    - Input: case type, remedies identified, documents drafted
    - Generate step-by-step action plan with:
      - Numbered steps with timeline/deadlines
      - Specific addresses/portals/helplines
      - Evidence to collect
      - Escalation path if first remedy fails
    - Use knowledge graph `get_escalation_path()` for escalation steps
    - Output: structured roadmap object

- [ ] **7.10 — Wire up the LangGraph agent graph**
  - File: `backend/agents/graph.py`
  - Build the `StateGraph`:
    1. Entry: supervisor
    2. Supervisor → intent classifier (use fine-tuned model)
    3. Intent classifier → conditional routing to the correct agent
    4. Each agent → RAG retriever (if needed) → agent logic
    5. Agent output → roadmap generator
    6. Roadmap → guardrail pipeline
    7. Guardrail → response builder → END
  - Add memory (SqliteSaver) for multi-turn conversation
  - Compile the graph
  - Export `run_agent(user_message: str, conversation_id: str) -> dict`

---

## Phase 8: FastAPI Backend

- [ ] **8.1 — Create the main API server**
  - File: `backend/main.py`
  - Endpoints:
    ```
    POST /api/chat          → Send message, get streamed response
    POST /api/upload        → Upload document for analysis
    GET  /api/health        → Health check
    POST /api/generate-pdf  → Generate downloadable PDF
    GET  /api/graph         → Knowledge graph as JSON
    ```
  - Add CORS middleware for frontend
  - Load all components on startup (RAG pipeline, knowledge graph, intent classifier, agent graph)
  - WebSocket endpoint for streaming chat responses

- [ ] **8.2 — Implement streaming chat endpoint**
  - In `backend/main.py`:
  - Use Server-Sent Events (SSE) for streaming:
    - As the agent graph processes, stream intermediate results
    - Stream types: `thinking`, `retrieving`, `drafting`, `result`, `roadmap`, `citation`
    - Final message includes the full structured response
  - Handle multi-turn: use `conversation_id` to maintain state via LangGraph checkpointer

- [ ] **8.3 — Implement document upload**
  - In `backend/main.py`:
  - Accept PDF, image (PNG/JPG), or text files
  - Use PyMuPDF (`fitz`) to extract text from PDF
  - Return extracted text + auto-detected document type

- [ ] **8.4 — Test the backend**
  - Start server: `uvicorn main:app --reload --port 8000`
  - Test with curl:
    ```bash
    curl -X POST http://localhost:8000/api/chat \
      -H "Content-Type: application/json" \
      -d '{"message": "I want to file RTI about road construction in Delhi", "conversation_id": "test-1", "mode": "chat"}'
    ```
  - Verify: response includes citations, structured output, action steps

---

## Phase 9: Frontend — UI & Design

- [ ] **9.1 — Create the global CSS design system**
  - File: `frontend/src/app/globals.css`
  - Dark theme with amber/gold accent:
    ```css
    :root {
      --bg-primary: #0a0a12;
      --bg-secondary: #12121e;
      --bg-card: #1a1a2e;
      --bg-card-hover: #22223a;
      --text-primary: #f0f0f5;
      --text-secondary: #8888a0;
      --text-muted: #55556a;
      --accent: #e6a336;
      --accent-hover: #f5c563;
      --accent-subtle: rgba(230, 163, 54, 0.1);
      --success: #4caf50;
      --warning: #ff9800;
      --error: #f44336;
      --border: #2a2a3d;
      --border-light: #1e1e30;
    }
    ```
  - Include smooth animations, transitions, glassmorphism card styles
  - Add typing animation keyframes
  - Add fade-in animation for messages

- [ ] **9.2 — Build the main layout**
  - File: `frontend/src/app/layout.tsx`
  - Clean layout: Header with logo + tagline, main content area, no footer

- [ ] **9.3 — Build the home page with tab navigation**
  - File: `frontend/src/app/page.tsx`
  - Main tabs: `📝 RTI Drafter` | `⚖️ Know My Rights` | `🔍 Decode` | `📋 Schemes` | `📎 Analyze` | `💬 Chat`
  - Tab bar at top, content area below

- [ ] **9.4 — Build the chat interface component**
  - File: `frontend/src/components/ChatInterface.tsx`
  - Message list with styled user/AI bubbles
  - Streaming text display
  - Auto-scroll, typing indicator
  - Input bar at bottom with send button
  - Quick-start prompt buttons when chat is empty

- [ ] **9.5 — Build the document output card component**
  - File: `frontend/src/components/DocumentCard.tsx`
  - Styled card for generated RTI/notice/complaint
  - Copy to clipboard button with checkmark animation
  - Download as TXT button
  - Download as PDF button

- [ ] **9.6 — Build the citation badge component**
  - File: `frontend/src/components/CitationBadge.tsx`
  - Inline pill badges like `[RTI Act, S.6(1)]`
  - Color-coded by confidence
  - Hover tooltip with full section text

- [ ] **9.7 — Build the action roadmap component**
  - File: `frontend/src/components/ActionRoadmap.tsx`
  - Vertical timeline/stepper UI with icons, deadlines, expandable details

- [ ] **9.8 — Build the scheme results component**
  - File: `frontend/src/components/SchemeResults.tsx`
  - Card grid with eligibility badges, benefit amounts, documents needed

- [ ] **9.9 — Build the document upload component**
  - File: `frontend/src/components/DocumentUpload.tsx`
  - Drag-and-drop zone, file picker, upload progress, "Analyze" button

- [ ] **9.10 — Build the confidence indicator component**
  - File: `frontend/src/components/ConfidenceIndicator.tsx`
  - Shield icon with high/medium/low coloring
  - Disclaimer text + legal aid links

- [ ] **9.11 — Build the loading/thinking states**
  - File: `frontend/src/components/ThinkingIndicator.tsx`
  - Contextual messages: "Searching legal database...", "Drafting RTI...", "Verifying citations..."

- [ ] **9.12 — Connect frontend to backend API**
  - File: `frontend/src/lib/api.ts`
  - Implement: `sendMessage()`, `uploadDocument()`, `generatePdf()`, `healthCheck()`
  - Use EventSource or fetch with ReadableStream for SSE streaming
  - Handle errors gracefully

---

## Phase 10: Integration & Polish

- [ ] **10.1 — End-to-end RTI flow test**
  - Start both servers. Type RTI query → verify follow-ups → formatted RTI → action roadmap → copy/download works

- [ ] **10.2 — End-to-end rights navigator test**
  - Test tenant dispute → verify law citations → legal notice offered → roadmap shown

- [ ] **10.3 — End-to-end bureaucracy decoder test**
  - Paste RERA notice → plain language + rights violations flagged

- [ ] **10.4 — End-to-end scheme matcher test**
  - Answer eligibility questions → multiple scheme matches returned

- [ ] **10.5 — Add responsive design**
  - All components work on 360px mobile viewport

- [ ] **10.6 — Add micro-animations and polish**
  - Message fade-in, button hover effects, tab slide animation, copy checkmark, smooth scroll, skeleton loaders

- [ ] **10.7 — Add error handling**
  - Backend down → friendly message. LLM fail → retry. Upload fail → specific error. Timeout → retry button.

---

## Phase 11: Evaluation & Metrics

- [ ] **11.1 — Create test dataset**
  - File: `backend/eval/test_cases.json`
  - 50+ test cases across all features with expected outputs

- [ ] **11.2 — Build evaluation runner**
  - File: `backend/eval/evaluate.py`
  - Track: intent accuracy, citation precision/recall, answer relevance, hallucination-free rate, latency

- [ ] **11.3 — Run evaluation and capture results**
  - Run: `python -m eval.evaluate`
  - Capture metrics table for presentation slides

---

## Phase 12: Deployment

- [ ] **12.1 — Deploy backend to Railway or Render (free tier)**
  - Set environment variables, verify health endpoint

- [ ] **12.2 — Deploy frontend to Vercel**
  - Set `NEXT_PUBLIC_API_URL` to deployed backend URL, verify

- [ ] **12.3 — Prepare demo backup**
  - Record 2-minute screen recording, save screenshots, keep localhost ready

---

## Phase 13: Demo & Presentation Prep

- [ ] **13.1 — Prepare demo script**
  - Demo 1 (45s): RTI drafting live
  - Demo 2 (30s): Bureaucracy decoder + rights violation detection
  - Demo 3 (20s): Rights navigator + legal notice
  - Demo 4 (15s): Scheme matcher + action roadmap
  - Closing (10s): Evaluation metrics

- [ ] **13.2 — Create presentation slides (5 max)**
  - Slide 1: Problem + pitch
  - Slide 2: Architecture diagram
  - Slide 3: Live demo
  - Slide 4: Technical differentiators
  - Slide 5: Metrics + future vision

- [ ] **13.3 — Practice demo 3 times**
  - Time it (3-5 min). Pre-type inputs. Know fallback if something breaks.

---

## 🚨 Emergency Fallback Priorities

If running out of time, cut in this order (bottom = cut first):

| Cut Order | Feature | Alternative |
|---|---|---|
| Cut LAST | RTI Drafter + Rights Navigator + Action Roadmap | These 3 are the minimum |
| Cut 6th | Evaluation framework | Mention metrics verbally |
| Cut 5th | Document upload & analysis | "Coming soon" tab |
| Cut 4th | Form filler | Mention in future work |
| Cut 3rd | Scheme matcher | Hardcoded demo |
| Cut 2nd | Fine-tuned classifier | LLM-based classification fallback |
| Cut 1st | Cross-encoder reranking | Basic vector search still works |

**The rule: 3 polished features > 8 broken features. Always.**
