import json
import random
import os

random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/datasets")
OUTPUT_PATH = os.path.join(DATA_DIR, "intent_training_v2.jsonl")

# Target counts
CLASS_TARGETS = {
    "RTI_Central": 300,
    "RTI_State": 300,
    "RTI_FirstAppeal": 200,
    "Consumer_District": 300,
    "Consumer_RERA": 300,
    "Legal_Notice": 200,
    "Employment_Agreement": 150,
    "Police_FIR": 300,
    "Labour_Dispute": 300,
    "Domestic_Violence": 300,
    "Cheque_Bounce": 200,
    "Cybercrime": 200,
    "Scheme_Info": 200,
    "General_Legal_Advice": 300,
    "Fill_Document": 200,
    "Tenant_Landlord": 200,
    "Contract_Review": 150,
    "Chitchat": 150
}

# Dictionaries for entity replacement to create variety
ENTITIES = {
    "central_dept": ["PMO", "Ministry of Finance", "Railways", "Income Tax department", "UIDAI", "Passport office", "CBI", "NIA", "Ministry of Home Affairs", "UPSC", "CBSE"],
    "state_dept": ["municipal corporation", "state police", "RTO", "state education board", "ration card office", "state transport department", "water board", "electricity board", "BMC", "DDA"],
    "product_service": ["mobile phone", "laptop", "washing machine", "AC", "insurance claim", "courier", "broadband service", "flight ticket", "bank transaction", "medical service"],
    "party": ["neighbour", "employer", "seller", "landlord", "tenant", "builder", "business partner", "vendor", "contractor", "client"],
    "schemes": ["PM Awas Yojana", "Ayushman Bharat", "PM Kisan", "MGNREGA", "Mudra Yojana", "Sukanya Samriddhi", "Atal Pension", "Ujjwala Yojana", "Kisan Credit Card"]
}

# Base templates
TEMPLATES = {
    "RTI_Central": {
        "en": ["I want to file an RTI for {central_dept}", "how to get info from {central_dept}", "Draft an RTI for {central_dept}", "What is the RTI fee for {central_dept}?", "Can I file RTI online for {central_dept}?", "Procedure for RTI to {central_dept}"],
        "hinglish": ["Mujhe {central_dept} ke liye RTI dalna hai", "{central_dept} se info kaise nikalun RTI me", "RTI file karna hai {central_dept} me", "kya {central_dept} RTI ke under aata hai", "{central_dept} ki RTI fee kya hai"],
        "hindi": ["मुझे {central_dept} में RTI लगानी है", "{central_dept} से RTI कैसे माँगें", "{central_dept} का RTI ड्राफ्ट चाहिए", "क्या {central_dept} में ऑनलाइन RTI हो सकती है"]
    },
    "RTI_State": {
        "en": ["I want to file an RTI for {state_dept}", "how to get info from {state_dept}", "RTI application to {state_dept}", "Draft an RTI for {state_dept}", "RTI to {state_dept} regarding my application"],
        "hinglish": ["RTI for {state_dept}", "mujhe {state_dept} ki info chahiye RTI se", "RTI kaise kare {state_dept} me", "{state_dept} me RTI form submit karna hai", "{state_dept} complaint rti"],
        "hindi": ["{state_dept} से जानकारी के लिए RTI कैसे करें", "मुझे {state_dept} में RTI लगानी है", "{state_dept} का RTI फॉर्म कैसे भरें"]
    },
    "RTI_FirstAppeal": {
        "en": ["PIO did not reply to my RTI", "got incomplete information in RTI", "file first appeal RTI", "30 days passed no RTI reply", "how to draft RTI first appeal", "FAA RTI appeal format"],
        "hinglish": ["RTI ka reply nahi aaya 30 din ho gaye", "PIO ne wrong info di", "first appeal RTI kaise kare", "RTI appeal draft karna hai", "incomplete info in rti kya karu"],
        "hindi": ["RTI का जवाब नहीं आया", "RTI की पहली अपील कैसे करें", "30 दिन बाद RTI का जवाब नहीं मिला", "अधूरी जानकारी मिली RTI में"]
    },
    "Consumer_District": {
        "en": ["defective {product_service} complaint", "{product_service} service not provided after payment", "how to file consumer court case for {product_service}", "draft consumer complaint for {product_service}", "consumer forum {product_service} issue"],
        "hinglish": ["mera {product_service} kharab hai, consumer court jana hai", "{product_service} wale refund nahi de rahe", "consumer complaint draft karo {product_service} ki", "kaise file kare consumer case for {product_service}"],
        "hindi": ["{product_service} के लिए उपभोक्ता फोरम में शिकायत कैसे करें", "{product_service} खराब निकला, पैसे वापस नहीं मिल रहे", "उपभोक्ता न्यायालय में केस कैसे दर्ज करें"]
    },
    "Consumer_RERA": {
        "en": ["builder not giving possession", "RERA complaint against builder", "flat delayed 3 years", "how to file RERA case", "builder demanding extra money", "refund from builder under RERA"],
        "hinglish": ["builder possession nahi de raha", "RERA me complaint kaise kare", "flat 3 saal delay ho gaya", "builder refund nahi kar raha", "maha rera complaint procedure"],
        "hindi": ["बिल्डर घर का पजेशन नहीं दे रहा है", "रेरा में शिकायत कैसे करें", "फ्लैट 3 साल लेट है, पैसे वापस चाहिए", "बिल्डर के खिलाफ रेरा शिकायत"]
    },
    "Legal_Notice": {
        "en": ["draft legal notice to {party}", "send legal notice for issue with {party}", "how to send legal notice to {party}", "format of legal notice against {party}", "cost of sending legal notice to {party}"],
        "hinglish": ["mujhe {party} ko legal notice bhejna hai", "{party} ke against legal notice draft karo", "legal notice bhejne ka procedure for {party}", "kya main {party} ko legal notice de sakta hu"],
        "hindi": ["{party} को कानूनी नोटिस कैसे भेजें", "{party} के खिलाफ कानूनी नोटिस ड्राफ्ट करें", "वकील के जरिए {party} को नोटिस भेजना है"]
    },
    "Employment_Agreement": {
        "en": ["draft employment agreement", "NDA for my employee", "service contract template", "create offer letter for new joinee", "independent contractor agreement", "non compete clause drafting"],
        "hinglish": ["employment agreement banana hai", "apne employee ke liye NDA draft karo", "service contract kaise banaye", "offer letter ka format do", "contractor ke sath agreement"],
        "hindi": ["कर्मचारी के लिए एंप्लॉयमेंट एग्रीमेंट बनाएं", "NDA का ड्राफ्ट तैयार करें", "जॉब ऑफर लेटर का फॉर्मेट चाहिए", "सर्विस कॉन्ट्रैक्ट कैसे बनता है"]
    },
    "Police_FIR": {
        "en": ["how to file FIR", "police refused to register FIR", "zero FIR meaning", "can I file e-FIR online?", "police not taking my complaint", "what to do if FIR is not registered"],
        "hinglish": ["FIR kaise darj kare", "police FIR nahi likh rahi kya karu", "online FIR kaise hoti hai", "zero FIR kya hota hai", "police station me complaint nahi le rahe"],
        "hindi": ["एफआईआर कैसे दर्ज करें", "पुलिस एफआईआर नहीं लिख रही है", "जीरो एफआईआर क्या होती है", "ऑनलाइन एफआईआर कैसे करें"]
    },
    "Labour_Dispute": {
        "en": ["company did not pay salary", "wrongful termination without notice", "PF not deposited by employer", "gratuity claim process", "POSH complaint at workplace", "labour court complaint for unpaid dues"],
        "hinglish": ["company ne salary nahi di", "mujhe bina notice nikal diya", "employer mera PF jama nahi kar raha", "gratuity kaise claim kare", "company ke khilaf labour court case"],
        "hindi": ["कंपनी ने मेरी सैलरी नहीं दी", "मुझे नौकरी से निकाल दिया गया है", "कंपनी पीएफ जमा नहीं कर रही है", "श्रम न्यायालय में शिकायत कैसे करें"]
    },
    "Domestic_Violence": {
        "en": ["husband is beating me", "in-laws are harassing for dowry", "how to get protection order DV Act", "domestic violence complaint procedure", "my husband threw me out of house"],
        "hinglish": ["pati maar peet karta hai", "sasural wale pareshan kar rahe hai", "DV act me protection kaise lu", "domestic violence case karna hai", "husband ne ghar se nikal diya"],
        "hindi": ["पति मुझे मारता पीटता है", "ससुराल वाले दहेज के लिए परेशान कर रहे हैं", "घरेलू हिंसा की शिकायत कैसे करें", "पति ने मुझे घर से निकाल दिया"]
    },
    "Cheque_Bounce": {
        "en": ["cheque bounced what to do", "138 NI Act notice format", "cheque dishonour complaint court", "legal notice for cheque bounce", "my friend's cheque bounced", "cheque return memo received"],
        "hinglish": ["cheque bounce ho gaya kya karu", "section 138 ni act notice draft", "bounce cheque case kaise kare", "paise wapas nahi diye cheque bounce"],
        "hindi": ["चेक बाउंस हो गया है, क्या करूँ", "चेक बाउंस का कानूनी नोटिस ड्राफ्ट करें", "निगोशिएबल इंस्ट्रूमेंट एक्ट 138 की शिकायत"]
    },
    "Cybercrime": {
        "en": ["online fraud kya karu", "someone hacked my account", "cybercrime complaint kaise kare", "money deducted from bank account fraud", "fake profile cyber stalking", "report cyber crime online"],
        "hinglish": ["online scam ho gaya mere sath", "bank account se paise kat gaye fraud", "cyber cell me complaint kaise kare", "mera instagram hack ho gaya", "online dhokhadhadhi"],
        "hindi": ["मेरे साथ ऑनलाइन फ्रॉड हुआ है", "मेरा बैंक अकाउंट हैक हो गया", "साइबर क्राइम की शिकायत कैसे करें", "ऑनलाइन ठगी का शिकार हुआ हूँ"]
    },
    "Scheme_Info": {
        "en": ["how to apply for {schemes}", "eligibility for {schemes}", "documents required for {schemes}", "benefits of {schemes}", "can I get money under {schemes}"],
        "hinglish": ["{schemes} ke liye apply kaise kare", "{schemes} ki kya eligibility hai", "{schemes} me apply karne ka process batao", "kya mujhe {schemes} milega"],
        "hindi": ["{schemes} के लिए आवेदन कैसे करें", "{schemes} की पात्रता क्या है", "{schemes} के क्या फायदे हैं", "मुझे {schemes} का लाभ कैसे मिलेगा"]
    },
    "General_Legal_Advice": {
        "en": ["kya mujhe bail milegi", "free lawyer kaise mile", "what are my legal rights", "difference between cognizable and non-cognizable offence", "anticipatory bail process", "is this action legal?"],
        "hinglish": ["kya police mujhe arrest kar sakti hai", "free legal aid kaise milti hai", "mujhe bail kaise milegi", "mere kanooni adhikar kya hai", "kya ye legal hai"],
        "hindi": ["क्या मुझे अग्रिम जमानत मिल सकती है", "मुफ्त कानूनी सहायता कैसे मिलेगी", "मेरे कानूनी अधिकार क्या हैं", "पुलिस अरेस्ट से कैसे बचें"]
    },
    "Fill_Document": {
        "en": ["fill this form", "I have uploaded a document please fill it", "complete this template", "can you fill the blanks in this pdf", "fill the rti form for me"],
        "hinglish": ["mera form bhar do", "maine document upload kiya hai isko fill karo", "ye template pura kardo", "is form me details daal do"],
        "hindi": ["यह फॉर्म भर दें", "मैंने एक डॉक्यूमेंट अपलोड किया है, इसे भर दें", "इस टेम्पलेट को पूरा करें", "खाली स्थान भरें"]
    },
    "Tenant_Landlord": {
        "en": ["landlord deposit wapas nahi kar raha", "eviction notice mila", "rent agreement banana hai", "tenant not paying rent", "landlord harassing me", "draft rent agreement"],
        "hinglish": ["makan malik deposit wapas nahi de raha", "kirayedar rent nahi de raha kya karu", "rent agreement draft karo", "landlord bina notice ghar khali karwa raha hai"],
        "hindi": ["मकान मालिक मेरा डिपॉजिट वापस नहीं कर रहा है", "किरायेदार किराया नहीं दे रहा है", "रेंट एग्रीमेंट बनवाना है", "मकान मालिक परेशान कर रहा है"]
    },
    "Contract_Review": {
        "en": ["review this contract", "is this clause legal", "explain this agreement", "find risky terms in this contract", "read my employment contract", "what does this clause mean"],
        "hinglish": ["is contract ko review karo", "kya ye clause legal hai", "is agreement me kya likha hai samjhao", "contract me koi problem toh nahi hai dekh ke batao"],
        "hindi": ["इस कॉन्ट्रैक्ट को चेक करें", "इस एग्रीमेंट का मतलब समझाएं", "क्या यह क्लॉज़ कानूनी रूप से सही है", "मेरे अनुबंध की समीक्षा करें"]
    },
    "Chitchat": {
        "en": ["hello", "who are you", "what can you do", "thank you", "good morning", "how can you help me", "are you ai or human", "thanks for the help", "goodbye"],
        "hinglish": ["kaise ho", "tum kya kar sakte ho", "tumhara kya kaam hai", "aap kon ho", "thanks yaar", "shukriya", "madad ke liye shukriya"],
        "hindi": ["नमस्ते", "आप कौन हैं", "आप क्या कर सकते हैं", "धन्यवाद", "आपका बहुत बहुत धन्यवाद", "शुभ प्रभात", "आप मेरी कैसे मदद कर सकते हैं"]
    }
}

def generate_samples(label, target_count, entity_key=None):
    samples = []
    
    # Mix distribution
    counts = {
        "en": int(target_count * 0.5),
        "hinglish": int(target_count * 0.3),
        "hindi": target_count - int(target_count * 0.5) - int(target_count * 0.3)
    }
    
    for lang, count in counts.items():
        base_templates = TEMPLATES[label][lang]
        if not base_templates:
            base_templates = TEMPLATES[label]["en"] # fallback
            
        for _ in range(count):
            template = random.choice(base_templates)
            
            # Format with entity if exists
            if entity_key and "{" + entity_key + "}" in template:
                entity_val = random.choice(ENTITIES[entity_key])
                text = template.replace("{" + entity_key + "}", entity_val)
            else:
                text = template
                
            # Random slight variations to prevent exact dupes
            if random.random() < 0.2:
                text = text + " ?" if not text.endswith("?") else text.replace("?", "")
            if random.random() < 0.2:
                text = text.lower()
                
            samples.append({"text": text.strip(), "label": label})
            
    return samples

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    all_samples = []
    
    # Define which entity key goes with which class
    class_entities = {
        "RTI_Central": "central_dept",
        "RTI_State": "state_dept",
        "Consumer_District": "product_service",
        "Legal_Notice": "party",
        "Scheme_Info": "schemes"
    }
    
    class_counts = {}
    
    for label, count in CLASS_TARGETS.items():
        entity_key = class_entities.get(label)
        samples = generate_samples(label, count, entity_key)
        all_samples.extend(samples)
        class_counts[label] = len(samples)
        
    # Shuffle the dataset
    random.shuffle(all_samples)
    
    # Write to file
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for sample in all_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            
    print("--- Generation Complete ---")
    for label, count in class_counts.items():
        print(f"{label}: {count} samples")
    print(f"\nTotal samples generated: {len(all_samples)}")
    print(f"Written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
