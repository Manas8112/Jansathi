import json
import os
import random
from collections import Counter
import numpy as np
import torch
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, f1_score
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/datasets")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models/intent_classifier_v2")

FILE_V1 = os.path.join(DATA_DIR, "intent_training.jsonl")
FILE_V2 = os.path.join(DATA_DIR, "intent_training_v2.jsonl")

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Label mapping for old data
    old_mapping = {
        "RTI": "RTI_Central",
        "Consumer Complaint": "Consumer_District",
        "Complaint": "Police_FIR",
        "Legal Advice": "General_Legal_Advice",
        "Fill Document": "Fill_Document",
        "Cybercrime": "Cybercrime",
        "Domestic Violence": "Domestic_Violence",
        "General": "Chitchat"
    }

    texts = []
    labels = []

    # Read V1
    if os.path.exists(FILE_V1):
        with open(FILE_V1, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                data = json.loads(line)
                old_label = data.get("label", "")
                new_label = old_mapping.get(old_label, "General_Legal_Advice")
                texts.append(data.get("text", ""))
                labels.append(new_label)
    else:
        print(f"Warning: {FILE_V1} not found.")
                
    # Read V2
    if os.path.exists(FILE_V2):
        with open(FILE_V2, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                data = json.loads(line)
                texts.append(data.get("text", ""))
                labels.append(data.get("label", ""))
    else:
        print(f"Warning: {FILE_V2} not found.")

    print("--- Per-class count ---")
    counts = Counter(labels)
    for k, v in counts.items():
        print(f"{k}: {v}")

    # Encode labels
    le = LabelEncoder()
    encoded_labels = le.fit_transform(labels)
    
    # Save mapping
    mapping_dict = {str(i): cls for i, cls in enumerate(le.classes_)}
    with open(os.path.join(MODEL_DIR, "label_mapping.json"), "w", encoding="utf-8") as f:
        json.dump(mapping_dict, f, indent=2)

    # Train/val split
    X_train, X_val, y_train, y_val = train_test_split(
        texts, encoded_labels, test_size=0.2, random_state=42, stratify=encoded_labels
    )

    # Tokenization
    model_name = "law-ai/InLegalBERT"
    print(f"\nLoading tokenizer and model ({model_name})...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    def tokenize(texts_list):
        return tokenizer(texts_list, padding=True, truncation=True, max_length=128)
        
    train_encodings = tokenize(X_train)
    val_encodings = tokenize(X_val)

    # Dataset formatting
    class CustomDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)

    train_dataset = CustomDataset(train_encodings, y_train)
    val_dataset = CustomDataset(val_encodings, y_val)

    def compute_metrics(pred):
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        macro_f1 = f1_score(labels, preds, average="macro", zero_division=0)
        return {"f1": macro_f1}

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(le.classes_))

    training_args = TrainingArguments(
        output_dir=MODEL_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        warmup_steps=300,
        weight_decay=0.01,
        learning_rate=2e-5,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_steps=50,
        report_to="none",
        use_cpu=True
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    import glob
    checkpoints = glob.glob(os.path.join(MODEL_DIR, "checkpoint-*"))
    latest_checkpoint = None
    if checkpoints:
        latest_checkpoint = max(checkpoints, key=os.path.getctime)
        print(f"\nResuming training from {latest_checkpoint}...")
    else:
        print("\nStarting training from scratch...")

    trainer.train(resume_from_checkpoint=latest_checkpoint)

    # Evaluation
    print("\nEvaluating on validation set...")
    predictions = trainer.predict(val_dataset)
    preds = predictions.predictions.argmax(-1)
    
    precision, recall, fscore, support = precision_recall_fscore_support(y_val, preds, average=None, zero_division=0)
    
    print("\n--- Validation F1 Scores ---")
    civic_info_f1 = 0.0
    for i, cls in enumerate(le.classes_):
        print(f"{cls}: {fscore[i]:.4f}")
        if cls == "Civic_Info":
            civic_info_f1 = fscore[i]
            
    overall_f1 = f1_score(y_val, preds, average="macro", zero_division=0)
    print(f"\nOverall Macro F1: {overall_f1:.4f}")

    # Save
    print("\nSaving final best model...")
    trainer.save_model(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)
    
    print("\nTraining complete. To activate: rename models/intent_classifier_v2 -> models/intent_classifier")
    print("after verifying Civic_Info F1 > 0.75 and overall F1 > 0.80")

if __name__ == "__main__":
    main()
