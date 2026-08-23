import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState
from utils.llm_utils import strip_think
from langchain_core.messages import HumanMessage

MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models/intent_classifier")

# 1. Try to load the Local Fine-Tuned Model
local_model = None
local_tokenizer = None
label_mapping = {}

is_render = os.getenv("RENDER") == "true"

try:
    if not is_render and os.path.exists(MODEL_DIR) and os.path.exists(os.path.join(MODEL_DIR, "model.safetensors")):
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification

        print("[IntentRouter] Loading local fine-tuned model...")
        local_tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        local_model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        
        # Load label mapping
        mapping_path = os.path.join(MODEL_DIR, "label_mapping.json")
        if os.path.exists(mapping_path):
            with open(mapping_path, "r") as f:
                mapping = json.load(f)
                label_mapping = {int(k): v for k, v in mapping.items()}
        print(f"[IntentRouter] Local model loaded successfully. Classes: {list(label_mapping.values())}")
    else:
        print("[IntentRouter] Local model not found. Will use Groq fallback.")
except Exception as e:
    print(f"[IntentRouter] Failed to load local model: {e}. Will use Groq fallback.")


# 2. Set up the Groq Fallback
llm = ChatGroq(
    model=os.getenv("MODEL_CHEAP", "llama3-8b-8192"),
    temperature=0.0
)

intent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Indian legal intent classifier. Read the user's message IN THE CONTEXT of the recent conversation and classify their true intent into exactly ONE of these categories: 'RTI', 'Complaint', 'Draft Document', 'Legal Advice', 'Scheme Info', or 'General'. Return ONLY the category string.\n\nRecent Conversation History:\n{history}"),
    ("user", "{message}")
])

fallback_chain = intent_prompt | llm


def intent_router_node(state: AgentState):
    """
    Analyzes the latest user message to determine their legal intent.
    Uses local fine-tuned model first, falls back to LLM API.
    """
    messages = state.get("messages", [])
    if not messages:
         return {"user_intent": "General", "next_action": "respond"}
         
    latest_message = messages[-1].content
    intent = None
    
    # Attempt 1: Local Model Inference
    if local_model and local_tokenizer and label_mapping:
        try:
            inputs = local_tokenizer(latest_message, return_tensors="pt", truncation=True, padding=True, max_length=128)
            with torch.no_grad():
                outputs = local_model(**inputs)
            
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence, predicted_class_id = torch.max(probs, dim=-1)
            
            if confidence.item() > 0.80:
                intent = label_mapping.get(predicted_class_id.item())
                print(f"[IntentRouter] Local model predicted: {intent} (Confidence: {confidence.item():.2f})")
            else:
                print(f"[IntentRouter] Local model uncertain (Confidence: {confidence.item():.2f}). Falling back to Groq.")
                intent = None
        except Exception as e:
            print(f"[IntentRouter] Local inference failed: {e}. Falling back to Groq.")
            intent = None
            
    # Attempt 2: Groq Fallback
    if not intent:
        history_str = ""
        if len(messages) > 1:
            for m in messages[-5:-1]:
                role = "User" if isinstance(m, HumanMessage) else "JanSaathi"
                # Truncate long AI messages in history
                content = m.content[:300] + "..." if len(m.content) > 300 else m.content
                history_str += f"{role}: {content}\n"
                
        response = fallback_chain.invoke({"message": latest_message, "history": history_str})
        raw_intent = response.content.strip()
        intent = strip_think(raw_intent)
        print(f"[IntentRouter] Groq fallback predicted: {intent}")
    
    # Normalize intent string
    intent_clean = "General"
    for valid_intent in ["RTI", "Complaint", "Draft Document", "Legal Advice", "Scheme Info", "General"]:
        if valid_intent.lower() in str(intent).lower():
            intent_clean = valid_intent
            break
    
    # Simple routing logic based on intent
    if intent_clean in ["RTI", "Complaint", "Draft Document"]:
        next_action = "draft_document"
    elif intent_clean in ["Legal Advice", "Scheme Info"]:
        next_action = "retrieve_context"
    else:
        next_action = "general_chat"
        
    return {"user_intent": intent_clean, "next_action": next_action}

