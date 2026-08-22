import os
import json
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/datasets/intent_training.jsonl")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models/intent_classifier")
MODEL_NAME = "law-ai/InLegalBERT"

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted', zero_division=0)
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def train_model():
    print(f"Loading data from {DATA_FILE}")
    if not os.path.exists(DATA_FILE):
        print("Data file not found. Run download_datasets.py first.")
        return

    texts = []
    labels = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            texts.append(record["text"])
            labels.append(record["label"])

    print(f"Loaded {len(texts)} samples.")

    # Encode labels
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)
    num_labels = len(label_encoder.classes_)
    
    # Save the label mapping
    os.makedirs(MODEL_DIR, exist_ok=True)
    mapping = {int(k): str(v) for k, v in enumerate(label_encoder.classes_)}
    with open(os.path.join(MODEL_DIR, "label_mapping.json"), "w") as f:
        json.dump(mapping, f, indent=4)
        
    print(f"Classes ({num_labels}): {label_encoder.classes_}")

    # Split dataset
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, encoded_labels, test_size=0.2, random_state=42
    )

    # Load tokenizer
    print(f"Loading tokenizer: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def tokenize_data(texts, labels):
        encodings = tokenizer(texts, truncation=True, padding=True, max_length=128)
        dataset_dict = {
            'input_ids': encodings['input_ids'],
            'attention_mask': encodings['attention_mask'],
            'labels': labels.tolist()
        }
        return Dataset.from_dict(dataset_dict)

    train_dataset = tokenize_data(train_texts, train_labels)
    val_dataset = tokenize_data(val_texts, val_labels)

    # Load Model
    print("Loading InLegalBERT model with classification head...")
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, 
        num_labels=num_labels
    )

    # Training arguments
    # Using small epochs/batch size for quick hackathon iteration
    training_args = TrainingArguments(
        output_dir=MODEL_DIR,
        num_train_epochs=4,              # Increased to 4 epochs for better accuracy on larger dataset
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        warmup_steps=100,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )

    print("Starting training...")
    trainer.train()

    print("Evaluating...")
    results = trainer.evaluate()
    print(results)

    print(f"Saving final model to {MODEL_DIR}")
    trainer.save_model(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)
    
    print("Training complete! Model is ready to use for Intent Classification.")

if __name__ == "__main__":
    train_model()
