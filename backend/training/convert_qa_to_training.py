import json
import os
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/datasets")
QA_CORPUS_PATH = os.path.join(DATA_DIR, "legal_qa_corpus.json")
BNS_PATH = os.path.join(DATA_DIR, "bns_2023_sections.json")
TRAINING_JSONL = os.path.join(DATA_DIR, "intent_training.jsonl")

CATEGORY_MAPPING = {
    "RTI Act": "RTI",
    "Consumer Protection Act": "Consumer Complaint",
    "RERA Act": "Consumer Complaint",
    "Domestic Violence Act": "Domestic Violence",
    "IT Act cybercrime": "Cybercrime",
    "BNS 2023 criminal law": "Legal Advice",
    "Labour law": "Legal Advice",
    "Tenant/Landlord": "Legal Advice",
    "NI Act cheque bounce": "Legal Advice",
    "General rights": "Legal Advice"
}

def main():
    new_samples = []

    # Process legal_qa_corpus.json
    if os.path.exists(QA_CORPUS_PATH):
        with open(QA_CORPUS_PATH, "r", encoding="utf-8") as f:
            qa_data = json.load(f)
            
        for entry in qa_data:
            question = entry.get("question", "").strip()
            answer = entry.get("answer", "").strip()
            category = entry.get("category", "")
            
            label = CATEGORY_MAPPING.get(category, "Legal Advice")
            
            if question:
                new_samples.append({"text": question, "label": label})
                
            if answer:
                # Get first sentence
                first_sentence = re.split(r'(?<=[.!?])\s+', answer)[0].strip()
                if first_sentence:
                    new_samples.append({"text": first_sentence, "label": label})
    else:
        print(f"Warning: QA corpus not found at {QA_CORPUS_PATH}")

    # Process bns_2023_sections.json
    if os.path.exists(BNS_PATH):
        with open(BNS_PATH, "r", encoding="utf-8") as f:
            bns_data = json.load(f)
            
        for entry in bns_data:
            title = entry.get("title", "").strip()
            description = entry.get("description", "").strip()
            
            if title and description:
                text = f"{title}: {description}"
                new_samples.append({"text": text, "label": "Legal Advice"})
    else:
        print(f"Warning: BNS sections not found at {BNS_PATH}")

    # Append to intent_training.jsonl
    if not new_samples:
        print("No new training samples generated.")
    else:
        os.makedirs(os.path.dirname(TRAINING_JSONL), exist_ok=True)
        with open(TRAINING_JSONL, "a", encoding="utf-8") as f:
            for sample in new_samples:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
                
        # Count total lines
        with open(TRAINING_JSONL, "r", encoding="utf-8") as f:
            total_lines = sum(1 for _ in f)
            
        print(f"Added {len(new_samples)} new training samples. Total file now has {total_lines} lines.")

if __name__ == "__main__":
    main()
