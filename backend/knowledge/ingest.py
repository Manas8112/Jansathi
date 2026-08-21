import os
import json
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag.chroma_store import add_documents

def ingest_json_data(filepath: str, collection_name: str = "jansaathi_legal_kb"):
    """
    Reads a JSON file containing legal data, splits the text, and ingests it into ChromaDB.
    Expected JSON format: 
    [
        {"title": "Act Name", "text": "Full text of act", "source": "official_url", "type": "law"},
        ...
    ]
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # We use a character text splitter with a sensible chunk size for legal text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    documents = []
    metadatas = []
    ids = []

    for item in data:
        title = item.get("title", "Unknown")
        text = item.get("text", "")
        doc_type = item.get("type", "unknown")
        source = item.get("source", "unknown")

        if not text:
            continue

        chunks = text_splitter.split_text(text)
        
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({
                "title": title,
                "type": doc_type,
                "source": source,
                "chunk_index": i
            })
            ids.append(str(uuid.uuid4()))

    if documents:
        print(f"Ingesting {len(documents)} chunks from {filepath}...")
        add_documents(collection_name, documents, metadatas, ids)
    else:
        print("No valid documents found to ingest.")

if __name__ == "__main__":
    # Example usage:
    # python -m knowledge.ingest
    sample_data_path = os.path.join(os.path.dirname(__file__), "../data/datasets/sample_laws.json")
    ingest_json_data(sample_data_path)
