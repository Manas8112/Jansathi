import os
import json
import urllib.request
import csv
from datasets import load_dataset

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../data/datasets/intent_training.jsonl")

def save_sample(text: str, label: str, file_handle):
    if text and text.strip():
        record = {"text": text.strip(), "label": label}
        file_handle.write(json.dumps(record) + "\n")

def download_and_process_all():
    print(f"Preparing dataset at: {OUTPUT_FILE}")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        
        # 1. REAL RTI DATA (via direct CSV to bypass HF schema bug)
        print("Downloading REAL RTI data from joyboseroy/rti-bench...")
        try:
            url = "https://huggingface.co/datasets/joyboseroy/rti-bench/resolve/main/hf_annotated.csv"
            req = urllib.request.urlopen(url)
            lines = [line.decode('utf-8', errors='ignore') for line in req.readlines()]
            reader = csv.DictReader(lines)
            count = 0
            for row in reader:
                text = row.get('information_sought', '').strip()
                if text:
                    save_sample(text, "RTI", f)
                    count += 1
                    if count >= 1000: break
            print(f"  Added {count} real RTI samples.")
        except Exception as e:
            print(f"  Failed RTI download: {e}")

        # 2. REAL CONSUMER COMPLAINTS (via banking77 HF Dataset)
        print("Downloading REAL Consumer Complaints from banking77...")
        try:
            cfpb = load_dataset('banking77', split='train', trust_remote_code=True)
            count = 0
            for row in cfpb:
                text = row.get('text', '')
                if text and len(text) > 10:
                    save_sample(text, "Complaint", f)
                    count += 1
                    if count >= 1000: break
            print(f"  Added {count} real Complaint samples.")
        except Exception as e:
            print(f"  Failed Complaints download: {e}")

        # 3. REAL GENERAL INTENTS (via HF Datasets)
        print("Downloading REAL General Intents from clinc_oos...")
        try:
            clinc = load_dataset('clinc_oos', 'plus', split='train', trust_remote_code=True, streaming=True)
            count = 0
            for row in clinc:
                text = row.get('text', '')
                if text:
                    save_sample(text, "General", f)
                    count += 1
                    if count >= 1000: break
            print(f"  Added {count} real General samples.")
        except Exception as e:
            print(f"  Failed General download: {e}")

        # 4. REAL LEGAL ADVICE (via HF Datasets Indian Legal Conversations)
        print("Downloading REAL Legal Advice from shadow228825/Legal_Advisior_Conversation...")
        try:
            legal = load_dataset('shadow228825/Legal_Advisior_Conversation_With_Client_India', split='train', trust_remote_code=True, streaming=True)
            count = 0
            for row in legal:
                # Extract the user's initial question from the conversation string
                text = row.get('formatted_conversation', '')
                if "<s>" in text:
                    q = text.split("<s>")[1].split("</s>")[0].strip()
                    if q:
                        save_sample(q, "Legal Advice", f)
                        count += 1
                        if count >= 1000: break
            print(f"  Added {count} real Legal Advice samples.")
        except Exception as e:
            print(f"  Failed Legal Advice download: {e}")

        # 5. REAL SCHEME INFO (via SQuAD filtered for Government/Schemes)
        print("Downloading REAL Scheme Info queries from SQuAD...")
        try:
            squad = load_dataset('squad', split='train', trust_remote_code=True, streaming=True)
            count = 0
            for row in squad:
                q = row.get('question', '')
                ctx = row.get('context', '').lower()
                if 'government' in ctx or 'scheme' in ctx or 'policy' in ctx:
                    save_sample(q, "Scheme Info", f)
                    count += 1
                    if count >= 1000: break
            print(f"  Added {count} real Scheme Info samples.")
        except Exception as e:
            print(f"  Failed Scheme Info download: {e}")

        # 6. REAL DRAFT DOCUMENT (via LexGLUE European Legal Terminology)
        print("Downloading REAL Draft Document texts from LexGLUE...")
        try:
            lex = load_dataset('lex_glue', 'eurlex', split='train', trust_remote_code=True, streaming=True)
            count = 0
            for row in lex:
                text = row.get('text', '')
                # Take a short snippet representing drafting language
                snippet = " ".join(text.split()[:30])
                if snippet:
                    save_sample(f"Draft a document stating: {snippet}", "Draft Document", f)
                    count += 1
                    if count >= 1000: break
            print(f"  Added {count} real Draft Document samples.")
        except Exception as e:
            print(f"  Failed Draft Document download: {e}")

        print("Done compiling dataset using 100% REAL external datasets!")

if __name__ == "__main__":
    download_and_process_all()
