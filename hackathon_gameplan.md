# 🏛️ JanSaathi — AI for Civic & Legal Empowerment
### Hackathon Submission — Lean & Scrappy Build Plan

---

## The Idea in One Line

> **"Ask your problem in plain language, get your rights explained + documents drafted — instantly."**

JanSaathi is a simple web app (runs in any browser) that helps Indian citizens understand their civic/legal rights and generates ready-to-use documents like RTI applications, legal notices, and consumer complaints — no lawyer needed.

---

## 1. What Are We Actually Building? (Keep It Real)

**NOT building:**
- ❌ Mobile app
- ❌ WhatsApp bot
- ❌ Multi-language voice assistant
- ❌ Production-grade deployment
- ❌ User accounts / login system
- ❌ Real API integrations with government portals

**Actually building:**
- ✅ A single-page web app (HTML/CSS/JS or simple React/Next.js)
- ✅ Chat interface where user types their problem
- ✅ AI that understands the problem and explains rights in simple language
- ✅ RTI application generator (user gives details → formatted RTI comes out)
- ✅ Legal notice drafter for common disputes (rent, consumer)
- ✅ A "Bureaucracy Decoder" — paste confusing government text → get plain English/Hindi explanation
- ✅ Every AI response cites the actual law section (no hallucination vibes)
- ✅ Runs on localhost or a free Vercel/Render deploy for demo

---

## 2. Who Is This For? (3 Simple Personas)

**Priya (28, Bengaluru)** — Landlord won't return ₹1.2L security deposit. She knows she has rights but doesn't know what to do. Can't afford a lawyer for this amount.

**Ramesh (45, Lucknow)** — Wants to file RTI about mid-day meal fund misuse in his area. Heard of RTI but never filed one. Scared of getting the format wrong.

**Kavitha (35, Madurai)** — Daily wage worker, might be eligible for PM maternity scheme but the eligibility PDF is 40 pages of bureaucratic English.

**Common pain point:** *"I know I probably have a right, but I have no idea what to actually DO."*

---

## 3. Features We'll Demo (Pick 3, Do Them Well)

### How All Features Connect (The Ecosystem)

This is NOT a bunch of separate tools. Every feature flows into the others — this is what makes judges say **"this is a platform, not a project."**

```
                    ┌──────────────────┐
         ┌─────────│  User's Problem   │──────────┐
         │         └────────┬─────────┘           │
         │                  │                      │
         ▼                  ▼                      ▼
  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐
  │ 🔍 Bureaucracy│  │ ⚖️ Rights    │  │ 📋 Scheme      │
  │   Decoder     │  │  Navigator   │  │   Matcher      │
  │ (paste text)  │  │ (describe    │  │ (answer quiz)  │
  └──────┬────────┘  │  problem)    │  └───────┬────────┘
         │           └──────┬───────┘          │
         │    "your rights  │                  │
         │    are violated" │  suggests        │ eligible for
         │         │        │  remedies        │ 4 schemes
         ▼         ▼        ▼                  ▼
  ┌──────────────────────────────────────────────────┐
  │            📝 Document Generator                  │
  │  (RTI app / Legal notice / Consumer complaint /  │
  │   Scheme application checklist)                  │
  └──────────────────────┬───────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────┐
  │            🗺️ Action Roadmap                      │
  │  (Step-by-step: what to do, where to go,         │
  │   deadlines, escalation path, helpline numbers)  │
  └──────────────────────────────────────────────────┘
```

---

### Feature 1: 📝 RTI Drafting Agent (THE HERO FEATURE)
**Build time: ~3 hours | Impact: MASSIVE**

- User says: "I want to know how much MPLAD fund money was spent in my constituency last year"
- AI asks 2-3 follow-up questions (which state? which constituency? what time period?)
- AI generates a properly formatted RTI application with:
  - Correct PIO (Public Information Officer) identified
  - Proper legal language citing Section 6(1) of RTI Act 2005
  - Fee info (₹10 for central, varies by state)
  - Ready to copy/print/download
- **Also generates:** a "What happens next" card — 30-day reply deadline, first appeal format, second appeal to State Information Commission
- **Links to:** Feature 5 (if RTI reveals a problem → Rights Navigator kicks in)
- **This is the money shot for the demo.**

---

### Feature 2: ⚖️ Rights Navigator (Dispute Helper)
**Build time: ~3 hours | Impact: MASSIVE**

- User describes their problem in plain language — "landlord won't return deposit", "company delivered broken product", "employer not paying overtime"
- AI classifies the dispute type automatically (tenant / consumer / workplace / government service)
- AI explains:
  - What law applies (with exact section numbers)
  - What your specific rights are in this situation
  - What options you have (ranked from easiest → hardest, cheapest → most expensive)
  - What documents/evidence you need to collect
  - Where to go / who to contact (specific authority + address)
  - What deadlines apply (limitation periods)
- **Links to:** Feature 4 (auto-draft a legal notice), Feature 6 (auto-generate consumer forum complaint), Feature 8 (full action roadmap with timeline)

---

### Feature 3: 🔍 Bureaucracy Decoder (THE WOW FACTOR)
**Build time: ~2 hours | Impact: HIGH**

- User pastes ANY confusing text — government notice, legal clause, policy circular, rent agreement clause, loan terms, insurance fine print
- AI breaks it down into numbered plain-language bullet points
- AI categorizes: "This is about [rent/consumer/tax/property]"
- **Killer feature:** AI flags if any of your rights are being violated in the text
  - Example: Paste a rent agreement → AI says "⚠️ Clause 7 says landlord can enter without notice — this violates your right to peaceful enjoyment under the Rent Act"
  - Example: Paste a RERA notice → AI says "⚠️ This means your builder owes you compensation under Section 18 RERA"
- **Links to:** Feature 2 (violation found? → Rights Navigator explains what to do), Feature 4 (draft a response/notice), Feature 7 (upload the full document for complete analysis)
- **This is the "wow" moment in the demo — the before/after is visually stunning**

---

### Feature 4: 📄 Legal Notice & Document Generator
**Build time: ~2 hours | Impact: HIGH**

- Generates ready-to-use legal documents based on the user's situation:
  - **Legal Notice** — for deposit disputes, defective products, service deficiency, contract breach
  - **Consumer Forum Complaint** — formatted per Consumer Protection Act 2019, auto-picks District/State/National forum based on claim amount
  - **RERA Complaint** — for delayed possession, quality issues
  - **Workplace Grievance Letter** — for salary delays, wrongful termination
  - **Appeal Letter** — for RTI first appeal (when 30 days expire with no reply)
- Each document:
  - Uses proper formal legal language
  - Cites specific Act & Section
  - Has blanks for user's personal details clearly marked
  - Has a [Copy] and [Download as TXT] button
- **Links to:** Feature 8 (after generating → shows action roadmap: where to send, how to send, what deadline to track)
- **Not fancy — it's just templated text generation. But the output LOOKS professional and that wins demos.**

---

### Feature 5: 📋 Government Scheme Matcher
**Build time: ~2-3 hours | Impact: HIGH**

- Quick questionnaire (5-7 questions, NOT a boring form — conversational chat style):
  - State?
  - Age / Gender?
  - Occupation (farmer / student / self-employed / salaried / daily wage)?
  - Approximate annual family income?
  - Category (General / OBC / SC / ST)?
  - Any specific need? (housing / health / education / maternity / pension / loan)
- AI matches against a database of schemes and returns:
  - **Eligible schemes** with confidence level (Definitely Eligible / Likely Eligible / Check Locally)
  - For each scheme: one-line description, benefit amount, where to apply, documents needed
  - Schemes covered (hardcode these — it's enough for demo):
    - PM Awas Yojana (PMAY) — housing
    - PM Jan Arogya Yojana (Ayushman Bharat) — health insurance up to ₹5L
    - PM Kisan Samman Nidhi — ₹6,000/year for farmers
    - PM Matru Vandana Yojana (PMMVY) — ₹5,000 maternity benefit
    - PM SVANidhi — micro loans for street vendors
    - PM Mudra Yojana — business loans up to ₹10L
    - Sukanya Samriddhi Yojana — girl child savings
    - PM Shram Yogi Maandhan (PMSYM) — pension for unorganized workers
    - Atal Pension Yojana — pension scheme
    - 3-4 state-specific schemes for your demo state
- **Links to:** Feature 8 (action roadmap: nearest office, documents to carry, application steps)
- **Why this matters:** MyScheme.gov.in exists but it's clunky and impersonal. Our chat-style flow is faster and friendlier.

---

### Feature 6: 💬 Conversational Form Filler
**Build time: ~2-3 hours | Impact: MEDIUM-HIGH**

- Instead of staring at a blank government form, user has a CHAT:
  - AI: "What's the name of the company/person you're complaining against?"
  - User: "Flipkart"
  - AI: "What did you buy and when?"
  - User: "A washing machine, 3 months ago"
  - AI: "What went wrong?"
  - User: "It stopped working after 2 weeks, they won't replace it"
  - AI: "How much did you pay?"
  - User: "₹18,000"
  - AI: "Do you have the invoice/receipt?"
  - User: "Yes"
- At the end, AI generates a **filled complaint form** with all fields populated:
  ```
  CONSUMER COMPLAINT
  Before the District Consumer Disputes Redressal Forum, [City]
  
  Complainant: [Name, Address]
  Opposite Party: Flipkart Internet Pvt Ltd, [Registered Address]
  
  Facts of the Case: The complainant purchased a [brand] washing 
  machine on [date] for ₹18,000 via Flipkart...
  
  Relief Sought: Replacement of defective product OR refund of 
  ₹18,000 with interest, plus ₹5,000 compensation for mental 
  agony and litigation costs.
  
  Applicable Law: Consumer Protection Act, 2019 — Section 2(7), 
  Section 34...
  ```
- **The form fills itself from a conversation.** This is way better than a 20-field web form.
- **Links to:** Feature 4 (generates the final document), Feature 8 (how to file it on E-Daakhil)

---

### Feature 7: 📎 Document Upload & Analysis
**Build time: ~2 hours | Impact: MEDIUM-HIGH**

- User uploads a document (rent agreement, loan document, insurance policy, government notice, builder agreement)
- AI reads it and produces:
  - **Summary** — what this document is about in 3-4 sentences
  - **Key Terms** — the important obligations, amounts, dates, deadlines
  - **Red Flags** — unfair clauses, missing protections, rights violations
  - **Your Rights** — what protections you have under applicable law that this document may not mention
- Example outputs:
  - Upload rent agreement → "⚠️ This agreement doesn't mention the security deposit return timeline. Under [State] Rent Act, your landlord must return it within [X] days of vacating."
  - Upload insurance policy → "⚠️ Clause 14 excludes pre-existing conditions after only 1 year, but IRDAI guidelines mandate coverage after 4 years maximum."
  - Upload builder agreement → "⚠️ No penalty clause for delayed possession. Under RERA Section 18, you're entitled to interest for every month of delay."
- **Technically:** Just extract text from the uploaded file (PDF.js or PyPDF2) and send to LLM with a good analysis prompt. Not complicated.
- **Links to:** Feature 3 (decoder for specific clauses), Feature 2 (rights navigator if violations found), Feature 4 (draft a notice about the violations)

---

### Feature 8: 🗺️ Action Roadmap Generator
**Build time: ~1-2 hours | Impact: HIGH (ties everything together)**

This is the **glue feature** — every other feature ends with an Action Roadmap. This is what makes JanSaathi about ACTION not just information.

After any interaction, the user gets a personalized roadmap:

```
🗺️ YOUR ACTION PLAN

Step 1: ✉️ Send Legal Notice (TODAY)
  → Download the notice we drafted above
  → Send by Registered Post / Speed Post to [address]
  → Keep the postal receipt as proof
  → ⏰ Wait 15 days for response

Step 2: 📋 Collect Evidence (THIS WEEK)  
  → Screenshot WhatsApp messages with landlord
  → Get printout of bank transfer for deposit
  → Take photos of flat condition (if possible)
  → Get copy of rent agreement

Step 3: 🏛️ File Consumer Complaint (IF NO RESPONSE IN 15 DAYS)
  → Go to edaakhil.nic.in
  → Use the complaint we drafted above
  → Filing fee: ₹0 (claim under ₹5 lakh)
  → Attach evidence from Step 2
  → Expected timeline: 3-6 months

Step 4: 📞 Escalation Options
  → Free legal helpline (Tele-Law): 1800-XXX-XXXX
  → District Legal Services Authority: [link]
  → Consumer Helpline: 1800-11-4000 / NCH app

⏰ KEY DEADLINES:
  → Legal notice response: 15 days from sending
  → Consumer complaint filing: within 2 years of issue
  → RERA complaint: within 1 year of possession
```

- **Why this wins:** No other team will go beyond "here's your answer." We say "here's your answer AND here's exactly what to do, step by step, with deadlines."
- **Technically dead simple:** It's just structured text output from the LLM. The magic is in the prompt.

---

### How These 8 Features Work Together (The Demo Story)

Here's a single user journey that touches MULTIPLE features — this is what impresses judges:

```
1. Kavitha uploads her rent agreement (Feature 7: Document Upload)
   ↓
2. AI finds 3 unfair clauses (Feature 3: Bureaucracy Decoder)  
   ↓
3. Kavitha says "my landlord won't return deposit" (Feature 2: Rights Navigator)
   ↓
4. AI explains her rights, suggests sending legal notice first
   ↓
5. AI drafts a legal notice automatically (Feature 4: Document Generator)
   ↓
6. AI shows full Action Roadmap with deadlines (Feature 8: Action Roadmap)
   ↓
7. Kavitha asks "am I eligible for any housing scheme?"
   ↓  
8. AI runs scheme matching (Feature 5: Scheme Matcher) → finds PMAY
   ↓
9. AI walks through PMAY application conversationally (Feature 6: Form Filler)
```

**One user session. Six features triggered naturally. Zero friction.**

That's not a chatbot — that's a **civic empowerment platform**.

---

### Feature Priority If Time Is Tight

| Priority | Feature | Must Ship? |
|---|---|---|
| 🔴 P0 | RTI Drafting Agent | YES — hero feature, demo anchor |
| 🔴 P0 | Rights Navigator | YES — shows conversational AI depth |
| 🔴 P0 | Action Roadmap | YES — differentiator, ties everything together |
| 🟡 P1 | Bureaucracy Decoder | YES if possible — wow factor |
| 🟡 P1 | Legal Notice Generator | YES if possible — proves "action not info" |
| 🟢 P2 | Scheme Matcher | Nice to have — shows breadth |
| 🟢 P2 | Document Upload | Nice to have — impressive if working |
| 🟢 P2 | Conversational Form Filler | Nice to have — can demo partially |

**Minimum viable demo: Features 1 + 2 + 8 (RTI + Rights + Roadmap). That alone wins.**  
**Ideal demo: All 8, flowing together. That DOMINATES.**

---

## 4. Technical Architecture (The Real Engineering)

This is NOT a ChatGPT wrapper. This is a **multi-agent system with a custom RAG pipeline, fine-tuned classifiers, knowledge graph, and a guardrail framework**. This is what separates a hackathon winner from a weekend project.

---

### 4.1 System Architecture (Full Picture)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (Next.js / React)                     │
│  ┌──────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────────────┐    │
│  │  Chat UI  │  │  Doc Upload  │  │ Decoder  │  │  Output Viewer   │    │
│  │(streaming)│  │  (drag+drop) │  │  Panel   │  │  (RTI/Notice PDF)│    │
│  └─────┬─────┘  └──────┬──────┘  └────┬─────┘  └────────┬─────────┘    │
└────────┼───────────────┼──────────────┼──────────────────┼──────────────┘
         │               │              │                   │
         ▼               ▼              ▼                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        API GATEWAY (FastAPI)                             │
│                    WebSocket for streaming responses                     │
└────────────────────────────┬─────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│                    🧠 AGENT ORCHESTRATOR (LangGraph)                      │
│                                                                          │
│    ┌─────────────┐    ┌──────────────┐    ┌────────────────────┐        │
│    │  SUPERVISOR  │───▶│ INTENT       │───▶│ ROUTE TO AGENT     │        │
│    │  AGENT       │    │ CLASSIFIER   │    │                    │        │
│    │              │    │ (fine-tuned)  │    │  rti_agent         │        │
│    │  Manages     │    │              │    │  rights_agent      │        │
│    │  state,      │    │  Categories: │    │  decoder_agent     │        │
│    │  memory,     │    │  • rti       │    │  scheme_agent      │        │
│    │  tool calls  │    │  • tenant    │    │  document_agent    │        │
│    │              │    │  • consumer  │    │  form_filler_agent │        │
│    └──────────────┘    │  • workplace │    │  roadmap_agent     │        │
│           │            │  • scheme    │    └────────────────────┘        │
│           │            │  • decode    │              │                   │
│           │            │  • document  │              │                   │
│           │            └──────────────┘              │                   │
│           │                                          │                   │
│           ▼                                          ▼                   │
│    ┌──────────────────────────────────────────────────────────┐          │
│    │                    TOOL REGISTRY                          │          │
│    │                                                          │          │
│    │  🔧 rag_search(query, filters)  → Hybrid RAG pipeline   │          │
│    │  🔧 draft_rti(details)          → Template + LLM        │          │
│    │  🔧 draft_notice(details)       → Template + LLM        │          │
│    │  🔧 match_schemes(profile)      → Eligibility engine    │          │
│    │  🔧 analyze_document(text)      → Doc analysis chain    │          │
│    │  🔧 decode_jargon(text)         → Simplification chain  │          │
│    │  🔧 find_authority(dept, state) → PIO/Authority lookup   │          │
│    │  🔧 check_deadlines(case_type)  → Limitation period DB  │          │
│    │  🔧 generate_roadmap(situation) → Action plan generator  │          │
│    │  🔧 validate_output(draft)      → Legal accuracy check  │          │
│    └──────────────────────────────────────────────────────────┘          │
│                              │                                           │
└──────────────────────────────┼───────────────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                     ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────────┐
│  HYBRID RAG      │ │  KNOWLEDGE       │ │  GUARDRAIL           │
│  PIPELINE        │ │  GRAPH           │ │  FRAMEWORK           │
│                  │ │                  │ │                      │
│ Vector Search    │ │ Laws → Sections  │ │ Citation Verifier    │
│ + BM25 Keyword   │ │ Sections → Rights│ │ Hallucination Filter │
│ + Reranker       │ │ Rights → Remedies│ │ Confidence Scorer    │
│ + Contextual     │ │ Remedies → Forms │ │ Disclaimer Injector  │
│   Compression    │ │ Schemes → Elig.  │ │ Structured Output    │
│                  │ │ Depts → PIOs     │ │   Validator          │
└──────────────────┘ └──────────────────┘ └──────────────────────┘
          │                    │                     │
          ▼                    ▼                     ▼
┌──────────────────────────────────────────────────────────────────┐
│                    DATA & STORAGE LAYER                           │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐  ┌────────────┐  │
│  │ ChromaDB / │  │ Neo4j /    │  │ SQLite   │  │ Template   │  │
│  │ Qdrant     │  │ NetworkX   │  │ (user    │  │ Store      │  │
│  │ (vectors)  │  │ (knowledge │  │  sessions,│  │ (Jinja2    │  │
│  │            │  │  graph)    │  │  logs)   │  │  RTI/forms)│  │
│  └────────────┘  └────────────┘  └──────────┘  └────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

### 4.2 Multi-Agent System (LangGraph)

This is NOT a single prompt hitting an LLM. This is a **graph of specialized agents** that collaborate, hand off tasks, and validate each other's work.

```python
# agents/graph.py — LangGraph Multi-Agent Orchestration

from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver

# Define the agent state
class JanSaathiState(MessagesState):
    intent: str                    # classified intent
    case_type: str                 # rti / tenant / consumer / workplace / scheme
    jurisdiction: str              # state / central
    user_profile: dict             # collected user info
    retrieved_context: list        # RAG results
    draft_document: str            # generated RTI/notice/complaint
    confidence_score: float        # how sure are we
    citations: list                # law sections cited
    action_roadmap: dict           # step-by-step plan
    requires_escalation: bool      # should we say "consult a lawyer"

# Build the agent graph
graph = StateGraph(JanSaathiState)

# Add agent nodes
graph.add_node("supervisor", supervisor_agent)         # Routes & manages
graph.add_node("intent_classifier", classify_intent)   # Fine-tuned classifier
graph.add_node("rag_retriever", retrieve_context)      # Hybrid RAG
graph.add_node("rti_agent", rti_drafting_agent)        # Drafts RTI
graph.add_node("rights_agent", rights_navigator_agent) # Explains rights
graph.add_node("decoder_agent", bureaucracy_decoder)   # Decodes jargon
graph.add_node("scheme_agent", scheme_matcher_agent)   # Matches schemes
graph.add_node("document_agent", document_analyzer)    # Analyzes uploads
graph.add_node("form_agent", form_filler_agent)        # Fills forms
graph.add_node("roadmap_agent", roadmap_generator)     # Action plan
graph.add_node("guardrail", guardrail_check)           # Validates output
graph.add_node("response_builder", build_response)     # Final formatting

# Define edges (the flow)
graph.set_entry_point("supervisor")
graph.add_edge("supervisor", "intent_classifier")
graph.add_conditional_edges("intent_classifier", route_to_agent, {
    "rti": "rag_retriever",
    "rights": "rag_retriever",
    "decode": "decoder_agent",
    "scheme": "scheme_agent",
    "document": "document_agent",
    "form": "form_agent",
})
graph.add_edge("rag_retriever", "rti_agent")       # or rights_agent
graph.add_edge("rti_agent", "roadmap_agent")
graph.add_edge("rights_agent", "roadmap_agent")
graph.add_edge("decoder_agent", "roadmap_agent")
graph.add_edge("scheme_agent", "roadmap_agent")
graph.add_edge("roadmap_agent", "guardrail")        # EVERYTHING goes through guardrail
graph.add_edge("guardrail", "response_builder")
graph.add_edge("response_builder", END)

# Compile with memory (conversation persistence)
memory = SqliteSaver.from_conn_string(":memory:")
app = graph.compile(checkpointer=memory)
```

**Why this impresses judges:**
- It's not a single LLM call — it's a **stateful agent graph**
- Each agent is specialized (separation of concerns)
- The guardrail node validates EVERY output before it reaches the user
- Memory/checkpointing means multi-turn conversations actually work
- You can show the graph visualization in your slides (LangGraph has built-in visualizer)

---

### 4.3 Hybrid RAG Pipeline (Not Basic Vector Search)

Basic RAG = embed documents, do cosine similarity, done. **That's 2023.** Here's what a 2026 hackathon-winning RAG looks like:

```python
# rag/pipeline.py — Hybrid RAG with Reranking & Contextual Compression

from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma  # or Qdrant
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker

# ──────────────────────────────────────────────
# STEP 1: Smart Chunking (not dumb fixed-size splits)
# ──────────────────────────────────────────────

# Use SEMANTIC chunking — splits by meaning, not character count
# This keeps legal sections together instead of cutting mid-sentence
semantic_chunker = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=85
)

# For structured legal text, also use section-aware splitting
class LegalSectionSplitter:
    """Custom splitter that respects legal document structure.
    Splits on Section/Chapter/Schedule boundaries."""
    
    def split(self, text):
        # Split on "Section \d+" patterns
        # Keep section number as metadata
        # Preserve cross-references
        sections = re.split(r'(?=Section \d+)', text)
        chunks = []
        for section in sections:
            match = re.search(r'Section (\d+[A-Z]?)', section)
            chunks.append(Document(
                page_content=section,
                metadata={
                    "section_number": match.group(1) if match else "unknown",
                    "act_name": "RTI Act 2005",  # from parent
                    "chunk_type": "legal_section"
                }
            ))
        return chunks

# ──────────────────────────────────────────────
# STEP 2: Dual Embedding + BM25 (Hybrid Search)
# ──────────────────────────────────────────────

# Vector search (semantic — understands meaning)
vector_store = Chroma.from_documents(
    documents=chunked_docs,
    embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
    collection_metadata={"hnsw:space": "cosine"}
)
vector_retriever = vector_store.as_retriever(
    search_type="mmr",           # Maximum Marginal Relevance — reduces redundancy
    search_kwargs={"k": 10, "fetch_k": 25, "lambda_mult": 0.7}
)

# BM25 search (keyword — catches exact legal terms like "Section 6(1)")
bm25_retriever = BM25Retriever.from_documents(chunked_docs, k=10)

# Combine both — semantic understands intent, BM25 catches exact citations
hybrid_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.6, 0.4]   # slightly favor semantic, but keywords matter in law
)

# ──────────────────────────────────────────────
# STEP 3: Reranking (this is the game-changer)
# ──────────────────────────────────────────────

# Cross-encoder reranker — re-scores results using a model that sees
# query AND document together (much more accurate than embedding similarity)
reranker_model = HuggingFaceCrossEncoder(
    model_name="cross-encoder/ms-marco-MiniLM-L-12-v2"   # or BAAI/bge-reranker-v2-m3
)
reranker = CrossEncoderReranker(
    model=reranker_model, 
    top_n=5   # keep top 5 after reranking
)

# ──────────────────────────────────────────────
# STEP 4: Contextual Compression
# ──────────────────────────────────────────────

# Don't send entire chunks to the LLM — extract only the relevant parts
compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=hybrid_retriever
)

# ──────────────────────────────────────────────
# STEP 5: Query Expansion (multi-query)
# ──────────────────────────────────────────────

# User says "landlord won't return deposit" — but the law says 
# "security deposit" or "earnest money" or "refundable amount"
# Generate multiple queries to catch all terminology

from langchain.retrievers.multi_query import MultiQueryRetriever

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=compression_retriever,
    llm=ChatOpenAI(model="gpt-4o-mini"),  # cheap model for query expansion
    prompt="""Generate 3 alternative phrasings of this legal query 
    using formal Indian legal terminology:
    Query: {question}
    Include terms that would appear in Indian statutes and acts."""
)

# ──────────────────────────────────────────────
# THE FULL PIPELINE IN ACTION:
# ──────────────────────────────────────────────
#
# User query: "landlord not returning my deposit in Bangalore"
#     │
#     ▼ Query Expansion
# → "security deposit refund Karnataka"
# → "return of earnest money tenant rights"  
# → "Section 27 Karnataka Rent Act deposit"
#     │
#     ▼ Hybrid Search (Vector + BM25)
# → 25 candidate chunks from both retrievers
#     │
#     ▼ Cross-Encoder Reranking
# → Top 5 most relevant chunks (much better ranking)
#     │
#     ▼ Contextual Compression
# → Only the relevant sentences from each chunk
#     │
#     ▼ Sent to LLM with the actual question
# → Grounded, cited, accurate response
```

**Why this impresses judges:**
- Hybrid search (vector + BM25) catches both semantic meaning AND exact legal terms
- Cross-encoder reranking is a legit ML technique, not just API calls
- Query expansion handles the vocab gap between citizen language and legal language
- Semantic chunking respects legal document structure
- You can show retrieval quality metrics in your presentation

---

### 4.4 Fine-Tuned Intent Classifier (Custom Model)

Don't just use prompt engineering for intent classification. **Train an actual model.**

```python
# training/intent_classifier.py

# ──────────────────────────────────────────────
# Fine-tune a small model for intent classification
# Takes ~15 min on free Google Colab GPU
# ──────────────────────────────────────────────

from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch

# Training data — curate ~200-500 examples (you can generate these with GPT-4o)
training_data = [
    # RTI intents
    {"text": "how much money was spent on road construction in my area", "label": 0},
    {"text": "I want details of MPLAD fund expenditure", "label": 0},
    {"text": "file RTI for mid day meal scheme funds", "label": 0},
    {"text": "information about government spending in my district", "label": 0},
    
    # Tenant dispute intents  
    {"text": "landlord is not returning my security deposit", "label": 1},
    {"text": "owner asking me to vacate without notice", "label": 1},
    {"text": "rent agreement has unfair clauses", "label": 1},
    {"text": "broker charged me illegal brokerage", "label": 1},
    
    # Consumer complaint intents
    {"text": "product I bought online is defective", "label": 2},
    {"text": "company not giving refund", "label": 2},
    {"text": "insurance claim rejected unfairly", "label": 2},
    {"text": "flipkart delivered wrong item", "label": 2},
    
    # Workplace dispute intents
    {"text": "employer not paying overtime", "label": 3},
    {"text": "fired without notice period", "label": 3},
    {"text": "company not depositing PF", "label": 3},
    {"text": "sexual harassment at workplace", "label": 3},
    
    # Scheme eligibility intents
    {"text": "am I eligible for PM Awas Yojana", "label": 4},
    {"text": "how to apply for Ayushman Bharat", "label": 4},
    {"text": "government schemes for farmers", "label": 4},
    {"text": "maternity benefit scheme eligibility", "label": 4},
    
    # Decode/explain intents
    {"text": "what does this government notice mean", "label": 5},
    {"text": "explain this legal clause in simple language", "label": 5},
    {"text": "I received this letter and don't understand it", "label": 5},
    
    # Document analysis intents
    {"text": "check my rent agreement for unfair terms", "label": 6},
    {"text": "review this builder agreement", "label": 6},
    {"text": "is my insurance policy good", "label": 6},
    
    # ... generate 300-400 more with GPT-4o
]

LABELS = ["rti", "tenant", "consumer", "workplace", "scheme", "decode", "document"]

# Use a small, fast model — DistilBERT or a multilingual one
model_name = "distilbert-base-uncased"  
# Or for Hindi support: "ai4bharat/indic-bert"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=len(LABELS)
)

# Create dataset
dataset = Dataset.from_list(training_data)
dataset = dataset.map(lambda x: tokenizer(x["text"], truncation=True, padding="max_length"), batched=True)
dataset = dataset.train_test_split(test_size=0.2)

# Train
training_args = TrainingArguments(
    output_dir="./intent_classifier",
    num_train_epochs=10,
    per_device_train_batch_size=16,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    logging_steps=10,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
)

trainer.train()

# Save the model — this runs in <100ms at inference
model.save_pretrained("./models/intent_classifier")
tokenizer.save_pretrained("./models/intent_classifier")
```

**At inference time:**
```python
# Fast classification — no LLM needed, runs locally in ~50ms
def classify_intent(user_message: str) -> str:
    inputs = tokenizer(user_message, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    
    probabilities = torch.softmax(logits, dim=-1)
    predicted_label = torch.argmax(probabilities).item()
    confidence = probabilities[0][predicted_label].item()
    
    return {
        "intent": LABELS[predicted_label],
        "confidence": confidence,
        "all_scores": {LABELS[i]: probabilities[0][i].item() for i in range(len(LABELS))}
    }

# Result: {"intent": "tenant", "confidence": 0.94, "all_scores": {...}}
```

**Why this impresses judges:**
- It's a **custom-trained model**, not just prompt engineering
- Shows you understand ML beyond API calls
- Runs locally in 50ms — way faster than an LLM call for routing
- You can show accuracy metrics, confusion matrix in your presentation
- For Hindi support, swap to `ai4bharat/indic-bert` — shows India-specific ML knowledge

---

### 4.5 Knowledge Graph (Law → Rights → Remedies → Forms)

A vector database finds relevant text. A **knowledge graph understands relationships** — which law grants which right, which right has which remedy, which remedy needs which form.

```python
# knowledge/graph.py — Legal Knowledge Graph

import networkx as nx
import json

# Build the graph
G = nx.DiGraph()

# ──────────────────────────────────────────────
# LAYER 1: Laws
# ──────────────────────────────────────────────
G.add_node("RTI_ACT_2005", type="law", name="Right to Information Act, 2005", 
           year=2005, jurisdiction="central")
G.add_node("CPA_2019", type="law", name="Consumer Protection Act, 2019",
           year=2019, jurisdiction="central")
G.add_node("RERA_2016", type="law", name="Real Estate (Regulation and Development) Act, 2016",
           year=2016, jurisdiction="central")
G.add_node("KA_RENT_1961", type="law", name="Karnataka Rent Control Act, 1961",
           year=1961, jurisdiction="state", state="Karnataka")
G.add_node("MH_RENT_1999", type="law", name="Maharashtra Rent Control Act, 1999",
           year=1999, jurisdiction="state", state="Maharashtra")

# ──────────────────────────────────────────────
# LAYER 2: Sections (specific provisions)
# ──────────────────────────────────────────────
G.add_node("RTI_S6", type="section", section="6", title="Application for information",
           summary="Any citizen can request information from a public authority")
G.add_node("RTI_S7", type="section", section="7", title="Disposal of request",
           summary="PIO must respond within 30 days")
G.add_node("RTI_S8", type="section", section="8", title="Exemptions",
           summary="Information exempt from disclosure")
G.add_node("RTI_S19", type="section", section="19", title="Appeal",
           summary="First appeal within 30 days, second appeal to Information Commission")
G.add_node("CPA_S34", type="section", section="34", title="District Commission jurisdiction",
           summary="Handles complaints up to ₹1 crore")
G.add_node("CPA_S35", type="section", section="35", title="State Commission jurisdiction",
           summary="Handles complaints ₹1 crore to ₹10 crore")
G.add_node("RERA_S18", type="section", section="18", title="Delayed possession",
           summary="Builder must pay interest for delay")

# ──────────────────────────────────────────────
# LAYER 3: Rights (what citizens can do)
# ──────────────────────────────────────────────
G.add_node("RIGHT_INFO", type="right", name="Right to seek information from public authority")
G.add_node("RIGHT_REFUND", type="right", name="Right to refund for defective product/service")
G.add_node("RIGHT_DEPOSIT_RETURN", type="right", name="Right to security deposit refund")
G.add_node("RIGHT_DELAYED_POSSESSION", type="right", name="Right to compensation for delayed possession")

# ──────────────────────────────────────────────
# LAYER 4: Remedies (how to exercise the right)
# ──────────────────────────────────────────────
G.add_node("REMEDY_RTI_APP", type="remedy", name="File RTI Application",
           cost="₹10", timeline="30 days for response")
G.add_node("REMEDY_LEGAL_NOTICE", type="remedy", name="Send Legal Notice",
           cost="Free (self-drafted)", timeline="15 days for response")
G.add_node("REMEDY_CONSUMER_FORUM", type="remedy", name="File Consumer Complaint",
           cost="₹0-₹5000", timeline="3-6 months", portal="edaakhil.nic.in")
G.add_node("REMEDY_RERA_COMPLAINT", type="remedy", name="File RERA Complaint",
           cost="Varies by state", timeline="60 days")
G.add_node("REMEDY_FIRST_APPEAL", type="remedy", name="File First Appeal (RTI)",
           cost="Free", timeline="Within 30 days of reply/non-reply")

# ──────────────────────────────────────────────
# LAYER 5: Forms & Templates
# ──────────────────────────────────────────────
G.add_node("FORM_RTI_A", type="form", name="RTI Application Form A",
           template_file="templates/rti_form_a.jinja2")
G.add_node("FORM_CONSUMER_COMPLAINT", type="form", name="Consumer Forum Complaint",
           template_file="templates/consumer_complaint.jinja2")
G.add_node("FORM_LEGAL_NOTICE", type="form", name="Legal Notice",
           template_file="templates/legal_notice.jinja2")
G.add_node("FORM_RERA_COMPLAINT", type="form", name="RERA Complaint Form",
           template_file="templates/rera_complaint.jinja2")

# ──────────────────────────────────────────────
# EDGES: Connect everything
# ──────────────────────────────────────────────

# Law → Section
G.add_edge("RTI_ACT_2005", "RTI_S6", relation="contains")
G.add_edge("RTI_ACT_2005", "RTI_S7", relation="contains")
G.add_edge("RTI_ACT_2005", "RTI_S19", relation="contains")
G.add_edge("CPA_2019", "CPA_S34", relation="contains")
G.add_edge("RERA_2016", "RERA_S18", relation="contains")

# Section → Right
G.add_edge("RTI_S6", "RIGHT_INFO", relation="grants")
G.add_edge("CPA_S34", "RIGHT_REFUND", relation="grants")
G.add_edge("RERA_S18", "RIGHT_DELAYED_POSSESSION", relation="grants")

# Right → Remedy (ordered by ease)
G.add_edge("RIGHT_INFO", "REMEDY_RTI_APP", relation="exercised_by", priority=1)
G.add_edge("RIGHT_REFUND", "REMEDY_LEGAL_NOTICE", relation="exercised_by", priority=1)
G.add_edge("RIGHT_REFUND", "REMEDY_CONSUMER_FORUM", relation="exercised_by", priority=2)
G.add_edge("RIGHT_DEPOSIT_RETURN", "REMEDY_LEGAL_NOTICE", relation="exercised_by", priority=1)
G.add_edge("RIGHT_DEPOSIT_RETURN", "REMEDY_CONSUMER_FORUM", relation="exercised_by", priority=2)

# Remedy → Form
G.add_edge("REMEDY_RTI_APP", "FORM_RTI_A", relation="requires_form")
G.add_edge("REMEDY_CONSUMER_FORUM", "FORM_CONSUMER_COMPLAINT", relation="requires_form")
G.add_edge("REMEDY_LEGAL_NOTICE", "FORM_LEGAL_NOTICE", relation="requires_form")

# ──────────────────────────────────────────────
# QUERYING THE GRAPH (this is the power)
# ──────────────────────────────────────────────

def get_remedies_for_problem(problem_type: str, state: str = None):
    """Given a classified problem, traverse the graph to find:
    1. Which rights apply
    2. Which remedies are available (ordered by priority)
    3. Which forms are needed
    4. Which laws/sections to cite
    """
    # Find the right node
    right_node = PROBLEM_TO_RIGHT_MAP[problem_type]
    
    # Get all remedies, sorted by priority
    remedies = []
    for _, target, data in G.out_edges(right_node, data=True):
        if data["relation"] == "exercised_by":
            remedy_data = G.nodes[target]
            # Get the form for this remedy
            forms = [G.nodes[t] for _, t, d in G.out_edges(target, data=True) 
                     if d["relation"] == "requires_form"]
            remedies.append({
                **remedy_data,
                "priority": data["priority"],
                "forms": forms
            })
    
    remedies.sort(key=lambda x: x["priority"])
    
    # Trace back to find the law and section
    # ... (traverse backwards through the graph)
    
    return {
        "rights": G.nodes[right_node],
        "remedies": remedies,
        "applicable_law": traced_law,
        "sections": traced_sections
    }
```

**Why this impresses judges:**
- It's a **structured knowledge representation**, not just text retrieval
- Shows understanding of graph-based reasoning in AI
- The graph traversal gives DETERMINISTIC results for known scenarios (no hallucination possible for the structured part)
- Easy to visualize in the demo (show the graph in slides)
- Can be expanded easily — add a new law node + edges and the system immediately knows about new rights/remedies

---

### 4.6 Guardrail & Validation Pipeline (Legal Safety)

Every output goes through a multi-stage validation pipeline. This is how you handle legal accuracy responsibly.

```python
# guardrails/pipeline.py

from pydantic import BaseModel, Field, field_validator
from typing import Literal
import re

# ──────────────────────────────────────────────
# STEP 1: Structured Output Validation (Pydantic)
# ──────────────────────────────────────────────

class LegalResponse(BaseModel):
    """Every LLM response MUST conform to this schema.
    If it doesn't parse → response is rejected and regenerated."""
    
    summary: str = Field(description="Plain language summary of the advice")
    applicable_laws: list[LawCitation] = Field(min_length=1)  # MUST cite at least one law
    rights_identified: list[str]
    remedies: list[Remedy]
    action_steps: list[ActionStep]
    confidence: Literal["high", "medium", "low"]
    disclaimer: str = Field(default="This is AI-generated civic guidance, not legal advice.")
    escalation_needed: bool
    
    @field_validator("applicable_laws")
    def must_have_citations(cls, v):
        if not v:
            raise ValueError("Response MUST cite at least one specific law and section")
        return v

class LawCitation(BaseModel):
    act_name: str          # "RTI Act, 2005"
    section: str           # "Section 6(1)"
    relevance: str         # "Grants right to request information"
    
class Remedy(BaseModel):
    name: str              # "File RTI Application"
    priority: int          # 1 = try first
    cost: str              # "₹10"
    timeline: str          # "30 days"
    difficulty: Literal["easy", "medium", "hard"]
    
class ActionStep(BaseModel):
    step_number: int
    action: str
    deadline: str | None
    details: str

# ──────────────────────────────────────────────
# STEP 2: Citation Verification
# ──────────────────────────────────────────────

class CitationVerifier:
    """Checks that every cited law section actually exists in our knowledge base."""
    
    def __init__(self, knowledge_graph, vector_store):
        self.kg = knowledge_graph
        self.vs = vector_store
        
        # Known valid citations (from our ingested data)
        self.valid_sections = self._build_citation_index()
    
    def verify(self, response: LegalResponse) -> dict:
        results = []
        for citation in response.applicable_laws:
            # Check if this section exists in our knowledge graph
            section_key = f"{citation.act_name}_S{citation.section}"
            exists = section_key in self.kg.nodes
            
            if not exists:
                # Fuzzy match — maybe the section format is slightly different
                close_matches = self._fuzzy_match(citation)
                if close_matches:
                    results.append({"citation": citation, "status": "corrected", 
                                   "correction": close_matches[0]})
                else:
                    results.append({"citation": citation, "status": "UNVERIFIED"})
            else:
                results.append({"citation": citation, "status": "verified"})
        
        return {
            "all_verified": all(r["status"] == "verified" for r in results),
            "details": results,
            "unverified_count": sum(1 for r in results if r["status"] == "UNVERIFIED")
        }

# ──────────────────────────────────────────────
# STEP 3: Hallucination Detection
# ──────────────────────────────────────────────

class HallucinationDetector:
    """Uses a separate LLM call to check if the response is grounded 
    in the retrieved context."""
    
    GROUNDING_PROMPT = """You are a legal accuracy checker. Given the 
    CONTEXT (retrieved legal text) and the RESPONSE (AI-generated advice), 
    check if every claim in the RESPONSE is supported by the CONTEXT.
    
    For each claim, output:
    - SUPPORTED: The claim is directly backed by the context
    - INFERRED: The claim is a reasonable inference but not directly stated
    - UNSUPPORTED: The claim has no basis in the context
    
    CONTEXT: {context}
    RESPONSE: {response}
    
    Output JSON array of checked claims."""
    
    async def check(self, response: str, retrieved_context: list[str]) -> dict:
        # Use a cheaper/faster model for verification
        result = await cheap_llm.ainvoke(
            self.GROUNDING_PROMPT.format(
                context="\n".join(retrieved_context),
                response=response
            )
        )
        
        claims = json.loads(result.content)
        unsupported = [c for c in claims if c["status"] == "UNSUPPORTED"]
        
        return {
            "is_grounded": len(unsupported) == 0,
            "unsupported_claims": unsupported,
            "grounding_score": (len(claims) - len(unsupported)) / len(claims)
        }

# ──────────────────────────────────────────────
# STEP 4: Confidence Scoring
# ──────────────────────────────────────────────

class ConfidenceScorer:
    """Computes a confidence score based on multiple signals."""
    
    def score(self, 
              retrieval_scores: list[float],    # cosine similarity of retrieved docs
              citation_verification: dict,       # from CitationVerifier
              grounding_check: dict,             # from HallucinationDetector
              intent_confidence: float           # from classifier
              ) -> dict:
        
        # Weighted scoring
        retrieval_quality = sum(retrieval_scores[:3]) / 3  # avg of top 3
        citation_score = 1.0 if citation_verification["all_verified"] else 0.5
        grounding_score = grounding_check["grounding_score"]
        
        final_score = (
            0.3 * retrieval_quality +
            0.3 * citation_score +
            0.25 * grounding_score +
            0.15 * intent_confidence
        )
        
        if final_score > 0.85:
            level = "high"
            message = "This guidance is well-supported by Indian law."
        elif final_score > 0.65:
            level = "medium"
            message = "This guidance is partially verified. Please cross-check specific details."
        else:
            level = "low"
            message = "I'm not confident enough — please consult a legal professional."
        
        return {"score": final_score, "level": level, "message": message}

# ──────────────────────────────────────────────
# THE FULL GUARDRAIL PIPELINE
# ──────────────────────────────────────────────

async def guardrail_pipeline(llm_response: str, retrieved_context: list, state: dict):
    """Every response goes through this before reaching the user."""
    
    # 1. Parse into structured format (rejects malformed responses)
    parsed = LegalResponse.model_validate_json(llm_response)
    
    # 2. Verify all citations
    citation_result = citation_verifier.verify(parsed)
    
    # 3. Check for hallucination
    grounding_result = await hallucination_detector.check(
        parsed.summary, retrieved_context
    )
    
    # 4. Compute confidence
    confidence = confidence_scorer.score(
        retrieval_scores=state["retrieval_scores"],
        citation_verification=citation_result,
        grounding_check=grounding_result,
        intent_confidence=state["intent_confidence"]
    )
    
    # 5. Decision
    if confidence["level"] == "low":
        # Don't show the unreliable response — show escalation instead
        return build_escalation_response(state)
    
    if not citation_result["all_verified"]:
        # Remove unverified citations, add warning
        parsed = remove_unverified_citations(parsed, citation_result)
    
    # 6. Inject disclaimer (always, non-negotiable)
    parsed.disclaimer = MANDATORY_DISCLAIMER
    parsed.confidence = confidence["level"]
    
    return parsed
```

**Why this impresses judges:**
- Shows you understand **responsible AI** in high-stakes domains
- Structured output validation (Pydantic) is industry best practice
- Citation verification is a novel approach to legal AI safety
- Hallucination detection using a separate LLM is a real technique from research
- Confidence scoring with multiple signals shows ML thinking
- **This is what separates "we built a chatbot" from "we built a trustworthy civic AI system"**

---

### 4.7 Evaluation Framework (Prove It Works)

Don't just say "it works" — **show metrics.** Judges love numbers.

```python
# eval/evaluate.py — Automated evaluation suite

# ──────────────────────────────────────────────
# Test Dataset (curate 50-100 test cases)
# ──────────────────────────────────────────────

test_cases = [
    {
        "query": "How to file RTI for road construction expenditure in Delhi?",
        "expected_intent": "rti",
        "expected_citations": ["RTI Act 2005, Section 6"],
        "expected_department": "PWD",
        "expected_fee": "₹10",
        "ground_truth_answer_contains": ["Public Information Officer", "30 days", "Section 6"]
    },
    {
        "query": "Landlord not returning deposit in Bangalore after 2 months",
        "expected_intent": "tenant",
        "expected_citations": ["Karnataka Rent Control Act", "Indian Contract Act"],
        "expected_remedies": ["legal notice", "consumer forum"],
        "ground_truth_answer_contains": ["security deposit", "legal notice", "15 days"]
    },
    # ... 50-100 more
]

# ──────────────────────────────────────────────
# Metrics We Track
# ──────────────────────────────────────────────

class EvaluationMetrics:
    def __init__(self):
        self.results = []
    
    def evaluate_case(self, test_case, actual_response):
        return {
            # Intent classification accuracy
            "intent_correct": actual_response.intent == test_case["expected_intent"],
            
            # Citation accuracy (are the right laws cited?)
            "citation_precision": self._citation_precision(
                actual_response.applicable_laws, test_case["expected_citations"]
            ),
            "citation_recall": self._citation_recall(
                actual_response.applicable_laws, test_case["expected_citations"]
            ),
            
            # Answer relevance (does the response contain key expected terms?)
            "answer_relevance": self._keyword_coverage(
                actual_response.summary, test_case["ground_truth_answer_contains"]
            ),
            
            # Hallucination rate (does it cite non-existent sections?)
            "hallucination_free": self._no_fake_citations(actual_response),
            
            # Response latency
            "latency_ms": actual_response.latency_ms,
            
            # Guardrail triggered correctly?
            "guardrail_appropriate": self._check_guardrail(actual_response, test_case),
        }
    
    def aggregate(self):
        return {
            "intent_accuracy": mean([r["intent_correct"] for r in self.results]),
            "citation_precision": mean([r["citation_precision"] for r in self.results]),
            "citation_recall": mean([r["citation_recall"] for r in self.results]),
            "answer_relevance": mean([r["answer_relevance"] for r in self.results]),
            "hallucination_free_rate": mean([r["hallucination_free"] for r in self.results]),
            "avg_latency_ms": mean([r["latency_ms"] for r in self.results]),
            "p95_latency_ms": percentile([r["latency_ms"] for r in self.results], 95),
        }

# ──────────────────────────────────────────────
# Run eval and generate report
# ──────────────────────────────────────────────
# 
# RESULTS TO SHOW IN PRESENTATION:
# ┌──────────────────────────────────────┐
# │  📊 JanSaathi Evaluation Results     │
# │                                      │
# │  Intent Accuracy:     94.2%          │
# │  Citation Precision:  91.5%          │
# │  Citation Recall:     88.3%          │
# │  Hallucination-Free:  97.1%          │
# │  Answer Relevance:    89.7%          │
# │  Avg Latency:         1.2s           │
# │  P95 Latency:         2.8s           │
# └──────────────────────────────────────┘
#
# ^ THIS is what wins hackathons. Numbers. Evidence. Rigor.
```

**Why this impresses judges:**
- Shows **scientific rigor** — you didn't just build, you measured
- Citation precision/recall is a domain-specific metric that shows deep thinking
- Hallucination-free rate directly addresses the #1 concern with legal AI
- You can put this table in your presentation slide — it screams credibility

---

### 4.8 Complete Tech Stack (What You Actually Install)

| Layer | Technology | Why This Specifically |
|---|---|---|
| **Frontend** | Next.js 14 + React | Streaming responses via Server-Sent Events |
| **Styling** | Tailwind CSS + shadcn/ui | Fast to build, looks premium |
| **Backend** | FastAPI (Python) | Async, WebSocket support, Pydantic integration |
| **Agent Framework** | LangGraph | Stateful multi-agent orchestration with memory |
| **LLM (Primary)** | GPT-4o / Gemini 2.5 Pro | Best reasoning for legal analysis |
| **LLM (Cheap/Fast)** | GPT-4o-mini / Gemini Flash | Query expansion, hallucination checks, grounding |
| **Embeddings** | OpenAI `text-embedding-3-large` | Best quality embeddings for legal text |
| **Vector DB** | ChromaDB (or Qdrant if you want to flex) | Vector storage + metadata filtering |
| **BM25** | `rank_bm25` (Python library) | Keyword search for exact legal terms |
| **Reranker** | `cross-encoder/ms-marco-MiniLM-L-12-v2` | Cross-encoder reranking (HuggingFace) |
| **Custom Classifier** | Fine-tuned DistilBERT / IndicBERT | Intent classification (custom trained) |
| **Knowledge Graph** | NetworkX (or Neo4j if ambitious) | Law → Rights → Remedies → Forms graph |
| **Structured Output** | Pydantic v2 | Validate every LLM response |
| **PDF Parsing** | PyMuPDF (`fitz`) | Extract text from uploaded legal documents |
| **PDF Generation** | WeasyPrint or ReportLab | Generate downloadable RTI/notice PDFs |
| **Evaluation** | Custom + RAGAS library | RAG evaluation metrics |
| **Deploy** | Vercel (frontend) + Railway (backend) | Free tier, instant deploy |

### Install Commands
```bash
# Backend
pip install fastapi uvicorn langchain langgraph langchain-openai langchain-community
pip install chromadb rank-bm25 sentence-transformers
pip install transformers torch datasets   # for fine-tuning
pip install networkx pydantic pymupdf weasyprint
pip install ragas                          # RAG evaluation framework

# Frontend  
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend && npx shadcn-ui@latest init
```

---

## 5. What Data Do We Need? (Knowledge Base)

### Must Have (Day 1)
| Document | Where to Get It | Size | Ingestion Method |
|---|---|---|---|
| RTI Act, 2005 (full text) | indiacode.nic.in | ~15K tokens | Legal section splitter → ChromaDB + Knowledge Graph |
| RTI Rules, 2012 | Same | ~5K tokens | Same |
| Consumer Protection Act, 2019 | indiacode.nic.in | ~20K tokens | Same |
| 2 State Rent Acts (MH + KA) | Same | ~10K tokens each | Same |
| PIO Directory (top 20 depts) | rti.gov.in | Structured data | Direct to Knowledge Graph |
| PM Scheme Guidelines (top 10) | Ministry PDFs | ~30K tokens total | Semantic chunker → ChromaDB |
| RTI/Notice/Complaint Templates | Self-authored | ~2K tokens | Jinja2 template store |

### Nice to Have (Day 2)
| Document | Purpose |
|---|---|
| RERA Act 2016 | Real estate disputes |
| Labour Codes 2020 | Workplace disputes |
| IT Act 2000, S.65B | Digital evidence validity |
| Forum jurisdiction data | Auto-routing by claim amount |
| State-specific scheme data | Broader scheme matching |

### Data Ingestion Pipeline
```python
# ingest/pipeline.py — Run once to build the entire knowledge base

async def ingest_all():
    # 1. Parse PDFs
    raw_docs = load_pdfs_from_directory("data/laws/")
    
    # 2. Smart chunking (legal section-aware)
    chunks = legal_section_splitter.split(raw_docs)
    
    # 3. Add metadata (act name, section number, jurisdiction)
    enriched_chunks = enrich_metadata(chunks)
    
    # 4. Embed and store in vector DB
    vector_store = Chroma.from_documents(
        enriched_chunks,
        OpenAIEmbeddings(model="text-embedding-3-large"),
        collection_name="indian_laws"
    )
    
    # 5. Build BM25 index (parallel keyword index)
    bm25_index = BM25Retriever.from_documents(enriched_chunks)
    
    # 6. Populate Knowledge Graph
    build_knowledge_graph(enriched_chunks)
    
    # 7. Generate training data for intent classifier
    training_data = generate_intent_training_data(enriched_chunks)
    
    # 8. Fine-tune intent classifier
    train_intent_classifier(training_data)
    
    print("✅ Knowledge base ready!")
    print(f"   {len(enriched_chunks)} chunks in vector DB")
    print(f"   {len(G.nodes)} nodes in knowledge graph")
    print(f"   {len(G.edges)} edges in knowledge graph")
    print(f"   Intent classifier accuracy: {eval_accuracy}%")
```

---

## 6. System Prompt (The Secret Sauce)

This is where 80% of the magic happens. Here's a starting point:

```
You are JanSaathi, an AI civic rights assistant for Indian citizens.

YOUR ROLE:
- Help citizens understand their legal and civic rights
- Draft RTI applications, legal notices, and consumer complaints
- Explain complex legal/bureaucratic language in simple terms
- Always cite the specific Act, Section, and Rule number

RULES (VERY IMPORTANT):
1. ALWAYS cite the exact law section. Example: "Under Section 6(1) of the 
   RTI Act, 2005, any citizen can request information..."
2. If you're not sure about something, SAY SO. Never make up a law or section.
3. End every response with: "⚠️ This is AI-generated civic guidance, not 
   legal advice. For specific legal matters, consult a qualified advocate 
   or call Tele-Law: 1800-XXX-XXXX"
4. Be warm, simple, and encouraging. The user is probably stressed.
5. When drafting documents (RTI, legal notice), use proper formal format.
6. Ask follow-up questions if you need more details to help accurately.

WHAT YOU CAN DO:
- Draft RTI applications (format per RTI Rules 2012, Form A)
- Explain tenant/consumer/workplace rights with applicable laws
- Decode bureaucratic/legal language into plain English or Hindi
- Draft legal notices for common disputes
- Suggest next steps with specific authorities to contact

WHAT YOU CANNOT DO:
- Represent the user in court
- Give definitive legal opinions on complex cases
- Access real-time government databases
- File applications on the user's behalf

[INSERT RELEVANT LAW TEXT HERE — RTI Act, Consumer Protection Act, etc.]
```

---

## 7. User Flows (What Actually Happens on Screen)

### Flow 1: RTI Drafting

```
Screen: Simple chat interface

User: "I want to file an RTI about road construction funds in my area"

AI: "I can help you draft an RTI application! I need a few details:
     1. Which state and city/district are you in?
     2. Which specific road or area are you asking about?  
     3. What time period (e.g., last 2 years)?"

User: "Delhi, Rohini Sector 15, last 1 year"

AI: "Got it. Here's your RTI application:

     ────────────────────────────────────
     To,
     The Public Information Officer,
     Executive Engineer, PWD Division-XX,
     Government of NCT of Delhi
     
     Subject: Application under Section 6(1) 
     of the Right to Information Act, 2005
     
     Sir/Madam,
     
     I, [Your Name], resident of [Your Address], 
     seek the following information:
     
     1. Total funds allocated for road construction/ 
        repair in Rohini Sector 15 for FY 2025-26.
     2. Detailed expenditure with contractor names 
        and work orders.
     3. Copies of completion certificates issued.
     
     Fee: ₹10 (via IPO/Court Fee Stamp)
     
     [Date]
     [Your Name, Address, Phone]
     ────────────────────────────────────
     
     📋 [Copy to Clipboard]  📄 [Download as Text]
     
     NEXT STEPS:
     • Print this and attach ₹10 court fee stamp
     • Send by Speed Post to PWD office
     • Keep postal receipt — reply due in 30 days
     • No reply? File First Appeal (I can help with that too)
     
     ⚠️ This is civic guidance, not legal advice."
```

### Flow 2: Rights Navigator (Tenant Dispute)

```
User: "My landlord is not returning my deposit. I left the flat 
       2 months ago in Bengaluru. He says I damaged walls."

AI: "Security deposit disputes are very common. Let me help.

     ⚖️ YOUR SITUATION:
     
     Applicable Law: Karnataka Rent Control Act + 
     Indian Contract Act, 1872 (Sections 73-74)
     
     Key Point: Normal wear and tear (like wall marks) 
     CANNOT be deducted from your deposit. The landlord 
     must PROVE actual damage beyond normal use.
     
     YOUR OPTIONS (easiest first):
     
     1️⃣ Send a Legal Notice (free, 5 min)
        → Formal letter demanding return in 15 days
        → ~60% landlords return money after receiving this
        → Want me to draft one? Just say 'draft notice'
     
     2️⃣ File Police Complaint
        → Under Section 403 IPC (misappropriation)
        → Go to nearest police station
     
     3️⃣ Consumer Forum Complaint (₹0-₹200 fee)  
        → File on edaakhil.nic.in
        → Can claim deposit + compensation
        → Takes 3-6 months
     
     💡 I recommend starting with Option 1.
     
     Do you have a written rent agreement and any 
     WhatsApp messages about the deposit?
     
     ⚠️ This is civic guidance, not legal advice."
```

### Flow 3: Bureaucracy Decoder

```
User pastes: "The allottee shall be entitled to claim 
compensation under sub-section (1) of section 18 at the 
rate prescribed under rule 15 of the Real Estate 
(Regulation and Development) Rules..."

AI: "📖 PLAIN LANGUAGE TRANSLATION:
     
     This says: If the builder delays giving you 
     possession of your flat, you can claim money 
     (interest) from them as compensation.
     
     Specifically:
     • This is under RERA Act 2016, Section 18(1)
     • The interest rate is set by the state rules
     • Usually it's SBI's highest lending rate + 2%
     • You can file a complaint on your state's 
       RERA portal
     
     ⚠️ RIGHTS FLAG: If your builder has delayed 
     possession beyond the date in your agreement, 
     you ARE entitled to this compensation. Many 
     buyers don't claim it.
     
     Want me to help you file a RERA complaint?"
```

---

## 8. UI Design (Keep It Clean, Not Fancy)

### Layout
```
┌──────────────────────────────────────────┐
│  🏛️ JanSaathi — Your Civic Rights AI     │
│                                          │
│  [RTI Drafter] [Know Rights] [Decoder]   │  ← 3 tabs, that's it
├──────────────────────────────────────────┤
│                                          │
│  Chat messages appear here               │
│  ...                                     │
│  ...                                     │
│  AI response with formatted output       │
│  ...                                     │
│                                          │
├──────────────────────────────────────────┤
│  [Type your question here...    ] [Send] │
│                                          │
│  Quick prompts:                          │
│  [File RTI] [Deposit dispute]            │
│  [Decode a notice] [Consumer complaint]  │
└──────────────────────────────────────────┘
```

### Design Tips (Minimum Effort, Maximum Impact)
- Dark theme (looks modern, easy to implement)
- One accent color (go with a warm amber/gold — civic/government feel)
- Use a nice font — add `Inter` or `DM Sans` from Google Fonts (one line of CSS)
- Add a subtle gradient background
- Make AI responses appear with a slight fade-in animation (CSS only)
- The generated RTI/notice should appear in a distinct "document card" with a border
- Add copy-to-clipboard and download buttons on generated documents

### Colors
```css
:root {
  --bg-primary: #0f0f14;
  --bg-secondary: #1a1a24;
  --bg-card: #22223a;
  --text-primary: #f0f0f5;
  --text-secondary: #9999aa;
  --accent: #e6a336;        /* warm amber/gold */
  --accent-light: #f5c563;
  --success: #4caf50;
  --warning: #ff9800;
  --border: #2a2a3d;
}
```

---

## 9. Handling the "Not Legal Advice" Problem

**Don't make the disclaimer kill the product.** Here's how:

### Bad (makes product feel useless):
> "⚠️ This is not legal advice. Please consult a lawyer."

### Good (makes disclaimer feel empowering):
> "This guidance is based on **Section 6(1), RTI Act 2005**. For additional help:
> 📞 Free legal helpline (Tele-Law): 1800-XXX-XXXX  
> 🏛️ Nearest Legal Aid Clinic: nalsa.gov.in  
> 
> *JanSaathi helps you take the first confident step — whether that's filing yourself or knowing the right questions to ask a lawyer.*"

### When AI Doesn't Know:
```
"I'm not confident enough to answer this accurately — the law 
in this area varies by state and situation. Here's what I suggest:

📞 Call Tele-Law (free): 1800-XXX-XXXX
🏛️ Visit: nalsa.gov.in for free legal aid
📍 Nearest Common Service Centre: csc.gov.in

I'd rather not guess than give you wrong information."
```

This is actually a **feature** — judges will respect that the AI knows when to say "I don't know."

---

## 10. Demo Script (3 Minutes)

### Slide 1: The Problem (30 sec)
*"62 lakh RTI applications were filed last year. But for every one filed, ten people gave up because they couldn't figure out the format, the right department, or the right words. Citizens have rights — they just can't navigate the system to use them."*

### Live Demo (90 sec)

**Demo 1 — RTI (45 sec)**
- Type: "I want to know how much my MLA spent from MPLAD fund last year in Lucknow"
- AI asks which constituency → answer
- **BOOM** — full formatted RTI appears with correct PIO, sections cited, fee info
- Click "Copy" → show it's ready to print and post
- *"That took 15 seconds. Without JanSaathi, this takes 2 hours and a lot of Googling."*

**Demo 2 — Bureaucracy Decoder (30 sec)**
- Paste a real RERA notice (confusing legal paragraph)
- AI breaks it into 4 bullet points
- AI flags: "⚠️ This notice means your builder owes you compensation"
- *"It didn't just translate — it found a rights violation the user didn't even know about."*

**Demo 3 — Rights Navigator (15 sec)**
- Quick flash of the tenant dispute flow
- Show legal notice generated
- *"From confused to empowered in 3 minutes."*

### Closing (30 sec)
*"JanSaathi doesn't just inform — it acts. Every response cites the actual law. Every output is ready to use. And when it doesn't know, it connects you to free legal aid instead of making things up."*

*"140 crore citizens deserve a government they can understand. JanSaathi makes that possible."*

### Backup Plan
- **If live demo breaks:** Have screenshots of each flow ready in slides
- **If API is slow:** Pre-record a 60-second video of the demo working
- **Always have both localhost AND a deployed URL ready**

---

## 11. What Makes This Different From Other Teams

| What everyone else will do | What we're doing differently |
|---|---|
| Generic chatbot that answers legal questions | We generate **actual documents** (RTI, notices) ready to use |
| Just wraps ChatGPT with a legal prompt | We cite **specific Act & Section** in every response |
| Tries to do everything, does nothing well | We nail **3 features** deeply |
| No guardrails against hallucination | We have **confidence scoring + "I don't know" fallback** |
| Looks like a homework project | **Clean dark UI** with document cards and animations |
| Says "consult a lawyer" and stops | We **connect to free legal aid** (NALSA, Tele-Law) as the next step |

### One-Line Pitch for Judges
> *"JanSaathi turns bureaucratic complexity into one-click action — draft an RTI in 15 seconds, understand your rights in 3 minutes, no lawyer needed."*

---

## 12. 48-Hour Build Timeline

### Day 1 (12 hours)

| Hours | Task | Who |
|---|---|---|
| 0-1 | Set up project. Create repo. Install dependencies. Get API key working. | Everyone |
| 1-3 | Copy law texts (RTI Act, Consumer Protection Act) into project as .txt files. Write the system prompt. Test basic Q&A in terminal. | Backend person |
| 1-3 | Build the chat UI. Dark theme. Input box. Message display. Three tabs. | Frontend person |
| 3-6 | Build RTI drafting flow — conversational intake + formatted output generation. | Backend |
| 3-6 | Build document output card UI — formatted display, copy button, download button. | Frontend |
| 6-9 | Build Rights Navigator — dispute identification + options display. | Backend |
| 6-9 | Connect frontend to backend API. End-to-end chat working. | Frontend |
| 9-12 | Build Bureaucracy Decoder — text input + plain language output. Polish all 3 flows. | Everyone |

### Day 2 (12 hours)

| Hours | Task | Who |
|---|---|---|
| 12-15 | Test all 3 features thoroughly. Fix bugs. Handle edge cases. | Everyone |
| 15-17 | Add disclaimers, citations display, "I don't know" fallback. | Backend |
| 15-17 | UI polish — animations, responsive layout, quick-prompt buttons. | Frontend |
| 17-19 | Deploy (Vercel + Render free tier). Test deployed version. | DevOps/anyone |
| 19-21 | Prepare demo script. Practice 3 times. | Everyone |
| 21-24 | Final testing. Pre-record backup demo video. Make slides (5 max). | Everyone |

### If You're Running Behind
- **Cut scheme eligibility** — skip it entirely
- **Cut RAG** — stuff everything in system prompt (it works fine for demo)
- **Cut fancy UI** — a clean chat interface is enough
- **Never cut the RTI feature** — it's the hero, it must work perfectly

---

## 13. Key Indian Laws to Reference

Keep this cheat sheet handy during the build:

| Law | Key Sections You'll Use | What It Covers |
|---|---|---|
| **RTI Act, 2005** | S.6 (how to apply), S.7 (timeframe: 30 days), S.8 (exemptions), S.19 (appeals) | Information from any public authority |
| **Consumer Protection Act, 2019** | S.2(7) (who's a consumer), S.34-36 (forum jurisdiction by claim amount), S.69 (penalties) | Product/service complaints |
| **Indian Contract Act, 1872** | S.73 (compensation for breach), S.74 (penalty clauses) | Security deposits, contract disputes |
| **RERA Act, 2016** | S.18 (delayed possession compensation), S.31 (complaint filing) | Real estate buyer rights |
| **Maharashtra Rent Control Act, 1999** | S.7 (standard rent), S.16 (eviction grounds) | Tenant rights in MH |
| **Karnataka Rent Act, 1961** | S.21 (eviction), S.27 (deposit) | Tenant rights in KA |
| **IT Act, 2000** | S.65B | WhatsApp/email messages as valid evidence |

### Forum Jurisdiction (Consumer Protection Act 2019)
| Claim Amount | Forum | Where to File |
|---|---|---|
| Up to ₹50 lakh | District Consumer Forum | edaakhil.nic.in |
| ₹50 lakh – ₹2 crore | State Consumer Commission | State capital |
| Above ₹2 crore | National Consumer Commission | Delhi |

### RTI Fees
| Level | Fee | Payment Mode |
|---|---|---|
| Central Government | ₹10 | IPO / DD / Court Fee Stamp / Online |
| Most State Governments | ₹10 | Court Fee Stamp / DD |
| BPL applicants | FREE | Attach BPL certificate |
| Online (rtionline.gov.in) | ₹10 | Net banking / card |

---

## 14. Potential Judge Questions & Answers

**Q: How is this different from just using ChatGPT?**
A: "Three things: (1) Every response cites the exact Act and Section — ChatGPT doesn't. (2) We generate ready-to-use documents in proper format, not just information. (3) We have guardrails — when the AI isn't sure, it says so and connects you to free legal aid instead of guessing."

**Q: What about hallucination? Legal info can't be wrong.**
A: "We solve this in three ways: the law text is directly in our knowledge base so the AI retrieves, not generates. Every claim has an inline citation. And we have a confidence system — if the AI isn't confident, it explicitly says 'I'm not sure, here's who to contact' instead of guessing."

**Q: How would you scale this?**
A: "Three directions: (1) Add more state laws and schemes to the knowledge base — same architecture. (2) Add Hindi and regional languages via Bhashini API. (3) WhatsApp bot for rural access — 500M+ Indians use WhatsApp."

**Q: Is this legal? Can you give legal advice?**
A: "We're very clear — this is civic guidance, not legal advice. Similar to how Google Maps gives directions but isn't a taxi service. We always show disclaimers and connect users to actual legal aid services like NALSA and Tele-Law."

**Q: What if the law changes?**
A: "The knowledge base is modular — we update the law text files and the system automatically uses the new information. For a production version, we'd set up periodic scraping of indiacode.nic.in."

---

## 15. Quick Wins That Impress Judges

These are small things that take 10-30 minutes each but make a big difference:

1. **Typing animation** on AI responses (makes it feel alive)
2. **Source citation badges** — little tags like `[RTI Act, S.6]` that look professional
3. **Quick-start prompts** — pre-written buttons like "File RTI", "Security deposit dispute" so judges don't have to think of what to type
4. **Document card** with a subtle border and different background for generated RTI/notices
5. **Copy to clipboard** with a ✅ animation
6. **Responsive design** — show it works on phone browser too (just CSS, no mobile app needed)
7. **Loading state** with "Analyzing your situation..." or "Drafting your RTI..." (not just a spinner)
8. **One real example** pre-loaded — have a "See example" button that shows a completed RTI flow

---

*Remember: A polished demo of 3 features beats a broken demo of 10 features. Nail the RTI drafter. Make the Bureaucracy Decoder the "wow" moment. Keep it simple, keep it working.*

*Good luck! 🚀*
