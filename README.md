# JanSaathi: AI Legal & Civic Advisor

JanSaathi is an intelligent, agentic AI platform designed to democratize legal and civic assistance for Indian citizens. Built with a focus on accessibility for marginalized communities, it provides actionable legal advice, analyzes complex contracts, and autonomously drafts formal legal documents.

## Our Approach

The legal system is often inaccessible due to high costs and complex jargon. Our approach focuses on building a highly specialized, multi-agent AI pipeline that breaks down legal barriers. Rather than relying on a single monolithic LLM, JanSaathi uses a modular, graph-based architecture where specialized AI agents (routers, drafters, and verifiers) work collaboratively to ensure high-accuracy, context-aware legal assistance.

## Key Technical Features

### 1. Fine-Tuned Intent Classification
We trained and deployed a custom NLP Intent Classifier (based on transformer architecture) to dynamically route user queries. Instead of relying on slow LLM calls for basic routing, our model instantly classifies inputs into categories such as `Legal Advice`, `Document Analysis`, `Drafting`, or `General Inquiry`. 
*Note: The final trained model weights (.safetensors) are version-controlled via Git LFS in this repository.*

### 2. Multi-Agent LangGraph Architecture
The core reasoning engine is built on **LangGraph**, orchestrating a specialized multi-agent workflow:
- **Intent Router:** Analyzes conversation history and current context to determine the execution path.
- **Document Analyzer:** Processes uploaded PDFs (contracts, lease agreements) and identifies predatory clauses or unenforceable terms under Indian Law.
- **Drafter Agent:** Autonomously drafts legally sound documents (RTI applications, Consumer Complaints, Legal Notices) with placeholders for user data.
- **Verifier Agent:** A self-reflection (critique) node that reviews the Drafter's output against Indian legal standards before presenting it to the user, ensuring zero hallucinations in document generation.

### 3. Legal Knowledge Retrieval (RAG)
We implemented a hybrid Retrieval-Augmented Generation (RAG) pipeline to ground the LLM in actual Indian penal codes, civic schemes, and welfare policies. The system utilizes both dense vector embeddings and BM25 sparse retrieval for high-precision context injection, strictly limiting output generation to verified knowledge.

### 4. Jurisdiction & Civic Entity Mapping
A custom Knowledge Graph engine maps local jurisdictions (e.g., Delhi MCD wards) to specific civic schemes (PM SVANidhi, e-Shram), allowing the AI to provide highly localized, actionable roadmaps rather than generic advice.

## Technology Stack

**AI & Machine Learning:**
- LangChain & LangGraph (Agent Orchestration)
- HuggingFace Transformers (Custom Intent Classification)
- Sentence-Transformers & BM25 (Hybrid RAG)

**Backend:**
- Python 3.10+
- FastAPI (High-performance API routing)
- SQLAlchemy (Asynchronous database management)
- SQLite (Local development)

**Frontend:**
- Next.js (React 18)
- Tailwind CSS (Premium, dark-mode native UI)
- React Markdown (Rich text & document rendering)

## Local Setup Instructions

A fully automated setup script is provided for easy deployment on Windows environments.

1. Clone the repository (ensure Git LFS is installed to pull the ML models).
```bash
git clone https://github.com/Manas8112/Jansathi.git
cd Jansathi
```

2. Run the initialization script:
```powershell
.\setup.ps1
```

The script will automatically install Node dependencies, initialize a Python virtual environment, install backend requirements, and provide commands to start both the FastAPI backend and Next.js frontend servers.
