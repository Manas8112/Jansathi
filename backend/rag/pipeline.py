import os
import json
from collections import Counter
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from rag.chroma_store import get_collection

class HybridRAGPipeline:
    def __init__(self, collection_name="jansaathi_legal_kb"):
        self.collection_name = collection_name
        self.collection = get_collection(collection_name)
        
        # Cross-Encoder for reranking
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2', max_length=512)
        
        # LLM for query expansion
        self.llm = ChatGroq(
            model=os.getenv("MODEL_CHEAP", "llama-3.1-8b-instant"),
            temperature=0.0
        )
        
        self.bm25 = None
        self.bm25_documents = []
        self.bm25_ids = []
        self._initialize_bm25()

    def _initialize_bm25(self):
        """Loads all documents from ChromaDB and initializes BM25 for keyword search."""
        data = self.collection.get()
        if data and data['documents']:
            self.bm25_documents = data['documents']
            self.bm25_ids = data['ids']
            
            # Simple tokenization for BM25
            tokenized_corpus = [doc.lower().split(" ") for doc in self.bm25_documents]
            self.bm25 = BM25Okapi(tokenized_corpus)
            print(f"BM25 initialized with {len(self.bm25_documents)} documents.")

    def _vector_search(self, query: str, k: int = 10) -> list[dict]:
        """Perform semantic search using ChromaDB."""
        from rag.chroma_store import search_documents
        
        results = search_documents(self.collection_name, query, n_results=k)
        
        docs = []
        if results and "documents" in results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                docs.append({
                    "id": results["ids"][0][i],
                    "content": doc,
                    "metadata": results["metadatas"][0][i],
                    "score": results["distances"][0][i]  # Distance (lower is better for cosine)
                })
        return docs

    def _bm25_search(self, query: str, k: int = 10) -> list[dict]:
        """Perform exact keyword search using BM25."""
        if not self.bm25:
            return []
            
        tokenized_query = query.lower().split(" ")
        doc_scores = self.bm25.get_scores(tokenized_query)
        
        # Get top k indices
        top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:k]
        
        docs = []
        for i in top_indices:
            if doc_scores[i] > 0: # Only return docs that have some match
                # Find metadata by fetching from Chroma by ID
                chroma_doc = self.collection.get(ids=[self.bm25_ids[i]])
                metadata = chroma_doc['metadatas'][0] if chroma_doc and chroma_doc['metadatas'] else {}
                
                docs.append({
                    "id": self.bm25_ids[i],
                    "content": self.bm25_documents[i],
                    "metadata": metadata,
                    "score": doc_scores[i] # BM25 score (higher is better)
                })
        return docs

    def _hybrid_merge(self, vector_results, bm25_results, weight_vector=0.6, weight_bm25=0.4):
        """Merges vector and BM25 results using reciprocal rank fusion (RRF)."""
        rrf_scores = Counter()
        doc_store = {}
        
        # Add vector ranks (1-indexed)
        for rank, doc in enumerate(vector_results, 1):
            rrf_scores[doc['id']] += weight_vector * (1 / (60 + rank))
            doc_store[doc['id']] = doc
            
        # Add BM25 ranks
        for rank, doc in enumerate(bm25_results, 1):
            rrf_scores[doc['id']] += weight_bm25 * (1 / (60 + rank))
            doc_store[doc['id']] = doc
            
        # Sort by RRF score
        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [doc_store[doc_id] for doc_id, score in sorted_docs]

    def _rerank(self, query: str, candidates: list[dict], top_n: int = 5) -> list[dict]:
        """Use a local cross-encoder model to accurately rerank the merged candidates."""
        if not candidates:
            return []
            
        pairs = [[query, doc["content"]] for doc in candidates]
        scores = self.reranker.predict(pairs)
        
        # Attach scores and sort
        for i, score in enumerate(scores):
            candidates[i]["rerank_score"] = float(score)
            
        return sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)[:top_n]

    def _expand_query(self, query: str) -> list[str]:
        """Uses LLM to generate alternative phrasing of the query with legal terminology."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an Indian legal assistant. Given a user query, generate 3 alternative ways to phrase this query using formal Indian legal terminology to improve search retrieval. Output ONLY the 3 queries separated by newlines."),
            ("user", "{query}")
        ])
        
        chain = prompt | self.llm
        try:
            res = chain.invoke({"query": query})
            expanded = res.content.strip().split('\n')
            # Clean up potential list numbering
            expanded = [q.strip('1234567890. -') for q in expanded if q.strip()]
            return [query] + expanded # include original
        except:
            return [query]

    def retrieve(self, query: str, top_n: int = 5) -> list[dict]:
        """Full Hybrid RAG retrieval pipeline."""
        # 1. Query Expansion
        queries = self._expand_query(query)
        
        all_vector_results = []
        all_bm25_results = []
        
        # 2. Parallel Search for each variant
        for q in queries:
            all_vector_results.extend(self._vector_search(q, k=5))
            all_bm25_results.extend(self._bm25_search(q, k=5))
            
        # Deduplicate before merge
        unique_vector = {d['id']: d for d in all_vector_results}.values()
        unique_bm25 = {d['id']: d for d in all_bm25_results}.values()
            
        # 3. Hybrid Merge (RRF)
        merged_candidates = self._hybrid_merge(list(unique_vector), list(unique_bm25))
        
        # 4. Cross-Encoder Reranking
        final_results = self._rerank(query, merged_candidates, top_n=top_n)
        
        return final_results

# Singleton instance
rag_pipeline = None

def get_rag_pipeline():
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = HybridRAGPipeline()
    return rag_pipeline
