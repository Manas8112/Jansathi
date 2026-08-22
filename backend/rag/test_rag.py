import os
from rag.pipeline import get_rag_pipeline

def run_tests():
    pipeline = get_rag_pipeline()
    
    test_queries = [
        "How to file RTI application",
        "consumer complaint for defective product",
        "maternity leave rules for women employees"
    ]
    
    print("====================================")
    print("Testing Hybrid RAG Pipeline")
    print("====================================")
    
    for query in test_queries:
        print(f"\nQUERY: {query}")
        results = pipeline.retrieve(query, top_n=2)
        
        for i, res in enumerate(results, 1):
            title = res['metadata'].get('title', 'Unknown')
            print(f"\n  Result {i}: {title} (Score: {res.get('rerank_score', 0):.4f})")
            print(f"  Content snippet: {res['content'][:150]}...")
            
if __name__ == "__main__":
    run_tests()
