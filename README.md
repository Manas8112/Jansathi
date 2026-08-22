<div align="center">
  <h1>⚖️ JanSaathi</h1>
  <p><strong>Agentic Civic & Legal Reasoning Engine</strong></p>
</div>

<br/>

## 🚨 The Architectural Problem with Naive LLMs
Current access-to-justice solutions rely heavily on zero-shot inference against generic Large Language Models (LLMs). This monolithic approach introduces critical points of failure:
1. **Unbounded Hallucinations:** Autoregressive models lack deterministic verification, frequently hallucinating case laws and penal codes.
2. **Contextual Isolation:** Foundational models operate in a vacuum, lacking structured topological data regarding local civic jurisdictions, bureaucratic workflows, and welfare schemes.
3. **Execution Paralysis:** Standard chat wrappers cannot execute deterministic actions (e.g., extracting entities, parsing complex PDF contracts, or structurally formatting legal notices) without severe prompt injection vulnerability or context window overflow.

## 💡 System Architecture: The JanSaathi Multi-Agent Pipeline
JanSaathi resolves these limitations by abandoning the monolithic LLM approach in favor of a **directed cyclical graph (LangGraph)**. The system orchestrates highly specialized, narrow-scope AI agents bounded by strict structural constraints. 

### Core State Graph

```mermaid
graph TD
    User([User Input]) --> Router[Intent Router<br/>(Fine-Tuned RoBERTa)]
    
    Router -->|Intent: Draft Document| Drafter[Drafter Agent]
    Router -->|Intent: Analyze Contract| Analyzer[Document Analyzer]
    Router -->|Intent: General Legal| RAG[Hybrid RAG Retrieval]
    Router -->|Intent: Civic/Local| Jurisdiction[Knowledge Graph Lookup]

    RAG --> Advisor[Legal Advisor Agent]
    Jurisdiction --> Advisor

    Drafter --> Verifier{Verifier Agent<br/>(Reflexion Node)}
    Analyzer --> Output([State Output])
    Advisor --> Output
    
    Verifier -->|Fails Legal Integrity| Drafter
    Verifier -->|Passes Validation| Output
```

---

## 🧠 Technical Deep-Dive

### 1. Zero-Shot Intent Classification (Edge Routing)
To minimize latency and token expenditure, we completely bypassed LLM-based routing. Instead, we implemented a custom **Intent Classification Model** using a fine-tuned transformer architecture (RoBERTa sequence classification). 
* **Implementation:** The model intercepts incoming JSON payloads, tokenizes the user query, and predicts the highest probability edge (Draft, Analyze, Advice, ChitChat). 
* **Deployment:** The model weights (`model.safetensors`, 437MB) and configuration schemas are version-controlled strictly via Git LFS, allowing seamless local initialization without external API dependencies.

### 2. LangGraph State Orchestration
The core of JanSaathi is a stateful directed graph. The `AgentState` object passes dynamically between nodes, mutating context matrices and appending `BaseMessage` arrays. 
* **The Drafter Agent:** Receives strict system prompts enforcing XML output formatting. It dynamically parses extracted entities (Name, Location, Subject) and autonomously generates structured documents (RTI Applications, Consumer Complaints).
* **The Verifier Node (Adversarial Critique):** We implemented a Reflexion-style feedback loop. The Verifier acts as an adversarial node, rigorously analyzing the Drafter's output for missing legal parameters, hallucinated sections, or improper formatting. If the threshold fails, the state routes *back* to the Drafter with correction gradients. This deterministic safety net practically eliminates downstream hallucinations.

### 3. Topological Jurisdiction Mapping (Knowledge Graph)
We decoupled generic legal advice from localized civic action by engineering a custom **Jurisdiction Knowledge Graph** using `networkx`. 
* Instead of relying entirely on vector similarity, the `GraphLookup` node extracts civic entities (e.g., "Street Vendor", "Delhi") and traverses deterministic graph edges to locate specific welfare schemes (PM SVANidhi), geographic nodes (MCD Wards), and authoritative endpoints. 
* This hybridizes semantic embeddings with structured, deterministic data retrieval.

### 4. Semantic Contract Analysis
The `analyzer.py` node handles raw byte-streams of uploaded PDF documents. 
* It chunks the text, isolates key contractual obligations, and evaluates them against established Indian judicial parameters (e.g., identifying unconscionable penalties under Section 74 of the Indian Contract Act). 
* The extracted metadata is then injected into the active `AgentState` for conversational querying.

### 5. Production-Grade Stack & Concurrency
* **Backend:** FastAPI handles async HTTP requests, interacting seamlessly with the LangGraph executor. We implemented dynamic context-window truncation algorithms to prevent `HTTP 413 Payload Too Large` errors during heavy multi-turn interactions.
* **State Persistence:** SQLite (via SQLAlchemy async sessions) handles user authentication, session-based conversation branching, and persistent storage of generated XML documents.
* **Frontend:** Next.js 14 utilizing Server-Side Rendering (SSR) and Tailwind CSS for a high-performance, responsive UI that natively parses and renders markdown structures dynamically streamed from the backend API.

---

## 🚀 Deployment Instructions

The repository includes a deterministic PowerShell setup script to bypass environment configuration friction.

**Prerequisites:** Python 3.10+, Node.js v18+, Git LFS

```powershell
# 1. Clone the repository (Git LFS will automatically pull the ML weights)
git clone https://github.com/Manas8112/Jansathi.git
cd Jansathi

# 2. Run the automated environment orchestrator
.\setup.ps1
```

*The setup script automatically initiates the Python virtual environment, installs PyTorch/Transformers/LangChain dependencies, resolves the Next.js `node_modules` tree, and outputs the local server bindings.*
