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
    model=os.getenv("MODEL_CHEAP", "openai/gpt-oss-20b"),
    temperature=0.0
)

intent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Indian legal intent classifier. Read the user's message IN THE CONTEXT of the recent conversation and classify their true intent into exactly ONE of these categories: 'RTI_Central', 'RTI_State', 'RTI_FirstAppeal', 'Police_FIR', 'General_Legal_Advice', 'Consumer_District', 'Consumer_RERA', 'Domestic_Violence', 'Cybercrime', 'Tenant_Landlord', 'Cheque_Bounce', 'Labour_Dispute', 'Legal_Notice', 'Employment_Agreement', 'Contract_Review', 'Fill_Document', 'Scheme_Info', 'Civic_Info', or 'Chitchat'. Return ONLY the category string.\n\nRecent Conversation History:\n{history}"),
    ("user", "{message}")
])

fallback_chain = intent_prompt | llm


def _is_off_topic(message: str) -> bool:
    msg_lower = message.lower().strip()
    civic_keywords = [
        "modi", "gandhi", "kejriwal", "yogi", "mamata", "rahul", "sonia",
        "pm", "cm", "minister", "mp", "mla", "governor", "president",
        "lok sabha", "rajya sabha", "parliament", "vidhan sabha",
        "judge", "justice", "court", "tribunal", "sebi", "rbi", "nhrc",
        "government", "govt", "ministry", "commission", "cbi", "ed", "police",
        "law", "act", "section", "rti", "fir", "complaint", "rights",
        "constitution", "bail", "arrest", "legal", "advocate", "lawyer",
        "scheme", "yojana", "policy", "budget", "welfare", "aadhar", "pan",
    ]
    for kw in civic_keywords:
        if kw in msg_lower:
            return False
    blocked_keywords = [
        "spiderman", "batman", "superman", "ironman", "avengers", "marvel",
        "harry potter", "pokemon", "naruto", "anime", "cartoon",
        "recipe", "cook", "biryani", "butter chicken", "pizza",
        "planet", "solar system", "galaxy", "dinosaur", "atom",
        "algebra", "calculus", "equation", "physics", "chemistry",
    ]
    for kw in blocked_keywords:
        if kw in msg_lower:
            return True
    return False


def intent_router_node(state: AgentState):
    """
    Analyzes the latest user message to determine their legal intent.
    Uses local fine-tuned model first, falls back to LLM API.
    """
    messages = state.get("messages", [])
    if not messages:
         return {"user_intent": "General", "next_action": "respond"}
         
    latest_message = messages[-1].content
    latest_message_lower = latest_message.lower()
    
    chitchat_patterns = [
        "kya kaam", "kya kar", "tumhara kaam", "aap kya", "aap kaise",
        "what do you do", "what can you do", "who are you", "what are you",
        "introduce yourself", "aap kaun", "tum kaun", "kaise madad",
        "kya help", "kya ho tum", "kya hai tum",
    ]
    for pattern in chitchat_patterns:
        if pattern in latest_message_lower:
            print(f"[IntentRouter] Short-circuit: chitchat/off-topic detected â€” '{latest_message[:50]}'")
            return {"user_intent": "General", "next_action": "general_chat"}

    words_in_query = latest_message_lower.split()
    who_patterns = ["who is", "who was", "what is", "tell me about",
                    "kaun hai", "kaun the", "kaun hain", "kon hai",
                    "batao", "ke baare mein", "ke bare mein"]
    if len(words_in_query) <= 8:
        for p in who_patterns:
            if p in latest_message_lower:
                # Only route to General if it's NOT a legal procedure question
                legal_procedure_words = [
                    "section", "rti", "fir", "act", "court",
                    "complaint", "penalty", "punish", "crime",
                    # Civic keywords â€” don't short-circuit these
                    "minister", "cm", "pm", "chief minister", "prime minister",
                    "mp", "mla", "governor", "president", "mayor",
                    "government", "govt", "party", "election", "parliament",
                    "scheme", "yojana", "policy", "commissioner", "judge", "justice"
                ]
                if not any(lw in latest_message_lower for lw in legal_procedure_words):
                    print(f"[IntentRouter] Short 'who is/what is' query â†’ routing to General.")
                    print(f"[IntentRouter] Short-circuit: 'who is' query â†’ General")
                    return {"user_intent": "General", "next_action": "general_chat"}

    if _is_off_topic(latest_message):
        print(f"[IntentRouter] Off-topic pre-check: BLOCKED '{latest_message[:50]}'")
        return {"user_intent": "Off-Topic", "next_action": "general_chat"}
        
    intent = None
    
    # Keyword override for filling documents (since local model wasn't trained on this intent)
    if "fill" in latest_message_lower and ("document" in latest_message_lower or "rti" in latest_message_lower or "notice" in latest_message_lower or "form" in latest_message_lower or "it" in latest_message_lower):
        intent = "Fill_Document"
        print(f"[IntentRouter] Keyword override predicted: {intent}")

    # Keyword override for Cheque Bounce
    if any(kw in latest_message_lower for kw in ["cheque bounce", "cheque bounced", "check bounce", "dishonoured cheque", "dishonored cheque", "bounced cheque", "negotiable instruments"]):
        intent = "Cheque_Bounce"
        print(f"[IntentRouter] Keyword override predicted: {intent}")

    # Keyword override for Domestic Violence
    if any(kw in latest_message_lower for kw in ["domestic violence", "husband beats", "husband hits", "marital abuse", "wife beating", "498a", "498-a", "pwdva"]):
        if not intent:
            intent = "Domestic_Violence"
            print(f"[IntentRouter] Keyword override predicted: {intent}")

    # Keyword override for Consumer complaints  
    if any(kw in latest_message_lower for kw in ["bought", "purchased", "defective product", "consumer forum", "refund refused", "warranty", "e-commerce", "online shopping", "amazon", "flipkart"]):
        if not intent:  # don't override if already set
            intent = "Consumer_District"
            print(f"[IntentRouter] Keyword override predicted: {intent}")

    # Keyword override for Cybercrime
    if any(kw in latest_message_lower for kw in ["online fraud", "cyber fraud", "otp fraud", "upi fraud", "phishing", "hacked", "morphed photo", "cybercrime", "ransomware"]):
        if not intent:
            intent = "Cybercrime"
            print(f"[IntentRouter] Keyword override predicted: {intent}")
    
    # Attempt 1: Local Model Inference
    if not intent and local_model and local_tokenizer and label_mapping:
        try:
            inputs = local_tokenizer(latest_message, return_tensors="pt", truncation=True, padding=True, max_length=128)
            with torch.no_grad():
                outputs = local_model(**inputs)
            
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence, predicted_class_id = torch.max(probs, dim=-1)
            
            # Lowered threshold to 0.40 because a 19-class model is highly confident even at 50%
            if confidence.item() > 0.40:
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
    valid_intents = [
        "RTI_Central", "RTI_State", "RTI_FirstAppeal", "Police_FIR",
        "General_Legal_Advice", "Consumer_District", "Consumer_RERA",
        "Domestic_Violence", "Cybercrime", "Tenant_Landlord", "Cheque_Bounce",
        "Labour_Dispute", "Legal_Notice", "Employment_Agreement", "Contract_Review",
        "Fill_Document", "Scheme_Info", "Civic_Info", "Chitchat", "Off-Topic"
    ]
    intent_clean = "Chitchat"
    for valid_intent in valid_intents:
        if valid_intent.lower() in str(intent).lower():
            intent_clean = valid_intent
            break

    drafting_intents = [
        "Fill_Document", "Legal_Notice", "RTI_Central", "RTI_State",
        "RTI_FirstAppeal", "Police_FIR", "Employment_Agreement", "Contract_Review"
    ]
    advice_intents = [
        "General_Legal_Advice", "Consumer_District", "Consumer_RERA",
        "Domestic_Violence", "Cybercrime", "Tenant_Landlord", "Cheque_Bounce",
        "Labour_Dispute", "Scheme_Info", "Civic_Info"
    ]

    if intent_clean in drafting_intents:
        next_action = "draft_document"
    elif intent_clean in advice_intents:
        next_action = "retrieve_context"
    else:
        next_action = "general_chat"

    print(f"[IntentRouter] FINAL â†’ Intent: {intent_clean} | Next: {next_action}")
    return {"user_intent": intent_clean, "next_action": next_action}

