import os
import json
import urllib.request
from datasets import load_dataset

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../data/datasets/intent_training.jsonl")

def save_sample(text: str, label: str, file_handle):
    if text and text.strip():
        record = {"text": text.strip(), "label": label}
        file_handle.write(json.dumps(record) + "\n")

def download_and_process_all():
    print(f"Preparing dataset at: {OUTPUT_FILE}")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # We use a JSONL file to append samples
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        
        # 1. RTI-Bench (Label: RTI)
        print("Downloading RTI-Bench...")
        try:
            rti_bench = load_dataset("joyboseroy/rti-bench", split="train")
            count = 0
            for row in rti_bench:
                text = row.get('fact', '') or row.get('text', '')
                if text:
                    save_sample(text, "RTI", f)
                    count += 1
                    if count >= 1000: break # Keep it balanced
            print(f"  Added {count} RTI samples.")
        except Exception as e:
            print(f"  Skipping RTI-bench: {e}")

        # 2. Grahak-Nyay (Label: Complaint)
        print("Downloading Grahak Nyay (Consumer Complaints)...")
        try:
            url = "https://raw.githubusercontent.com/ShreyGanatra/GrahakNyay/main/Data/NyayChat.json"
            req = urllib.request.urlopen(url)
            grahak_data = json.loads(req.read())
            count = 0
            for chat in grahak_data:
                # Get the first human query from the conversation
                if chat.get("conversations") and len(chat["conversations"]) > 0:
                    text = chat["conversations"][0].get("value", "")
                    if text:
                        save_sample(text, "Complaint", f)
                        count += 1
            print(f"  Added {count} Complaint samples.")
        except Exception as e:
            print(f"  Skipping Grahak Nyay: {e}")

        # 3. Legal Knowledge Base (Label: Legal Advice)
        print("Downloading Indian Legal Knowledge Base...")
        try:
            legal_kb = load_dataset("d-riti/Dataset-For-Indian-Legal-Knowledge-Base", split="train")
            count = 0
            for row in legal_kb:
                text = row.get("question", "")
                if text:
                    save_sample(text, "Legal Advice", f)
                    count += 1
                    if count >= 1000: break
            print(f"  Added {count} Legal Advice samples.")
        except Exception as e:
            print(f"  Skipping Legal KB: {e}")
            
        # 4. Synthesize Scheme Info and General (Hackathon shortcut)
        print("Adding synthetic Scheme & General samples...")
        schemes = [
            "Am I eligible for PM Kisan Samman Nidhi?",
            "How to apply for Ayushman Bharat yojana?",
            "What is the limit for Mudra loan?",
            "How to check PMAY rural status?"
        ] * 100 # Multiply for balance
        
        general = [
            "Hi there!",
            "Who are you?",
            "Can you help me?",
            "Good morning",
            "What is your name?"
        ] * 100
        
        for q in schemes: save_sample(q, "Scheme Info", f)
        for q in general: save_sample(q, "General", f)
        
        print("Done compiling dataset!")

if __name__ == "__main__":
    download_and_process_all()
