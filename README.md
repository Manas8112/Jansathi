<div align="center">
  <h1>⚖️ JanSaathi</h1>
  <p><strong>India's First Agentic AI Legal & Civic Advisor for the Marginalized</strong></p>
</div>

<br/>

## 🚨 The Problem: Why ChatGPT Fails at Law
For marginalized Indian citizens (street vendors, daily wage workers), the justice system is practically inaccessible due to exorbitant lawyer fees and complex bureaucratic jargon. 

While generic LLMs (like ChatGPT or Claude) exist, they are **fundamentally flawed** for legal advice:
1. **Dangerous Hallucinations:** Generic models hallucinate penal codes, cite fake legal precedents, and provide wildly inaccurate advice.
2. **No Local Context:** They do not understand the localized civic structures of India (e.g., MCD wards in Delhi, PM SVANidhi schemes, E-Shram registrations).
3. **Lack of Agency:** They can answer questions, but they cannot *act*. They cannot analyze a complex PDF lease agreement, find predatory clauses, and autonomously draft a formal legal notice in one seamless workflow.

## 💡 Our Solution: The JanSaathi Architecture
**JanSaathi** is not just an LLM wrapper. It is a highly specialized, **Multi-Agent Orchestration Pipeline** built from the ground up to solve the access-to-justice crisis in India. We combine custom NLP intent classifiers, hybrid RAG, and an advanced Agentic Graph to provide free, flawless, and actionable legal power to those who need it most.

---

## 🧠 Technical Architecture: Why We Are Superior

### 1. Custom Intent Classification Model (Zero-Shot Routing)
Most hackathon projects use an LLM for everything, which is slow and expensive. Instead, we trained and deployed a custom **Intent Classifier Model** (utilizing HuggingFace Transformers). 
* When a user sends a message, this model intercepts it and instantly classifies the intent (`Legal Advice`, `Document Analysis`, `Drafting`, `General`).
* This saves massive API token costs and routes the user to the precise AI Agent specialized for their task.
* *Note: The final 437MB `.safetensors` ML model is securely tracked and deployed in this repository via Git LFS.*

### 2. LangGraph Multi-Agent Orchestration
We built a stateful, cyclical reasoning engine using **LangGraph**. Depending on the Intent Classifier's output, the graph routes the context through highly specialized autonomous agents:
* 📄 **The Analyzer Agent:** Users can upload PDFs (like predatory lease agreements). The Analyzer uses semantic chunking to parse the contract, flag illegal clauses under the *Indian Contract Act 1872*, and suggest immediate remedies.
* ✍️ **The Drafter Agent:** Triggered when the user needs to take action. It autonomously drafts formal, legally structured documents (RTI Applications, Consumer Court Complaints, Legal Notices) and wraps them in secure XML tags for backend processing.
* 🛡️ **The Verifier Agent (Reflexion Loop):** This is our "Secret Sauce." Before the user ever sees a drafted document, the Verifier Agent acts as an independent adversarial AI. It critiques the Drafter's output for legal soundness, structural integrity, and tone. If it fails, the Verifier forces the Drafter into a correction loop. This practically guarantees **zero hallucinations**.

### 3. Hybrid RAG & Jurisdiction Knowledge Graphs
To ground our AI in reality, we built a two-pronged knowledge retrieval system:
1. **BM25 + Dense Vector RAG:** A hybrid retrieval system that searches our curated vector database of actual Indian Penal Codes, Rent Control Acts, and Civic Welfare Schemes.
2. **Jurisdiction Engine:** A custom Knowledge Graph that maps user queries to hyper-local civic data. If a street vendor in Delhi asks for help, the AI doesn't just explain the law—it gives them the exact address of their local MCD Ward Office and the helpline for the PM SVANidhi micro-loan scheme.

### 4. Robust Engineering & Quality of Life
We didn't just build a backend script; we built a production-ready application:
* **Token Limit Management:** We implemented dynamic context-window truncation to ensure the free-tier API never hits a 413 Payload Error, forcing the AI to be concise and accurate.
* **Document Persistence:** Drafted documents are extracted from the AI's XML tags, saved to an asynchronous SQLite database via SQLAlchemy, and populated in a secure `My Documents` dashboard where users can download them.
* **Premium UI/UX:** Built on Next.js and Tailwind CSS, featuring a sleek, dark-mode native interface, markdown rendering, streaming state indicators ("Analyzing legal context..."), and fully functioning Chat History management (with delete functionality).

---

## 🛠️ Technology Stack

**Artificial Intelligence & Machine Learning:**
* **LangChain & LangGraph:** Multi-Agent cyclical routing and state management.
* **HuggingFace Transformers:** Custom NLP Intent Classification.
* **ChromaDB / Sentence-Transformers:** Dense vector embeddings and BM25 sparse retrieval for RAG.

**Backend (Python):**
* **FastAPI:** High-performance async API routing.
* **SQLAlchemy (Async):** User authentication, chat history, and document persistence.
* **Pydantic:** Strict data validation and structured outputs.

**Frontend (React):**
* **Next.js 14:** Server-side rendering and routing.
* **Tailwind CSS:** Responsive, utility-first styling.
* **React Markdown / Remark-GFM:** Rendering complex legal tables and bolded citations perfectly in the chat UI.

---

## 🚀 Running the Project Locally

We built a fully automated setup script for judges and teammates to spin up the entire architecture (Frontend, Backend, Database, and ML Models) with one command.

### Prerequisites
* Python 3.10+
* Node.js v18+
* Git LFS (Required to pull the 437MB intent classification model)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Manas8112/Jansathi.git
cd Jansathi
```

2. Run the automated setup script (Windows):
```powershell
.\setup.ps1
```
*(This script will automatically install Next.js dependencies, create a Python virtual environment, install all ML/backend requirements, and generate the SQLite database).*

3. Start the application:
* **Frontend:** `cd frontend && npm run dev`
* **Backend:** `cd backend && .\.venv\Scripts\activate && uvicorn main:app --reload`
