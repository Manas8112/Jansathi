import string

def detect_language(text: str) -> str:
    """Detects if the text is Hindi (hi), Hinglish (hinglish), or English (en)."""
    if not text:
        return "en"
        
    # Count characters in the Unicode Devanagari block (U+0900 to U+097F)
    devanagari_count = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    
    # If Devanagari characters are > 10% of total characters: return "hi" (Hindi)
    if devanagari_count > 0.1 * len(text):
        return "hi"
        
    # Common Hinglish words
    hinglish_words = {
        # Question words
        "kya", "kaise", "kaisa", "kaisi", "kyun", "kyunki", "kab", "kahan", "kaun", "kitna", "kitni",
        # Pronouns
        "mujhe", "mera", "meri", "mere", "hum", "aap", "tum", "tumh", "tumhara", "tumhari",
        "iska", "iski", "iske", "uska", "uski", "uske", "unka", "unki", "unke",
        "apna", "apni", "apne", "tera", "teri", "tere", "hamara", "hamari",
        # Verbs / verb forms
        "hai", "hain", "tha", "thi", "hoga", "hogi", "honge",
        "karo", "karta", "karti", "karte", "kiya", "kiye", "kiया",
        "chahiye", "milega", "milegi", "milenge", "dena", "lena",
        "raha", "rahi", "rahe", "hua", "hui", "hue", "gaya", "gayi", "gaye",
        "aana", "jaana", "batao", "bata", "samjho", "dekho",
        # Negation / affirmation
        "nahi", "nahin", "mat", "na", "haan", "bilkul", "zaroor", "theek", "sahi",
        # Common particles
        "bhi", "aur", "ya", "lekin", "magar", "toh", "phir", "sirf",
        "bas", "bahut", "thoda", "zyada", "bohot", "acha", "accha",
        # Location / time
        "yaha", "yahan", "wahan", "waha", "abhi", "kal", "aaj", "pehle", "baad",
        # Common nouns used in Hinglish queries
        "kaam", "kab", "pata", "matlab", "matlab", "mila", "baat", "cheez",
        "paisa", "rupay", "problem", "madad", "help", "zarurat",
        # Misc connectors
        "isliye", "agar", "jo", "jab", "tab", "warna", "sab", "dono",
    }
    
    # Remove punctuation and split into words
    cleaned_text = text.lower()
    for p in string.punctuation:
        cleaned_text = cleaned_text.replace(p, ' ')
        
    words = cleaned_text.split()
    
    # Count how many of these words appear in the text
    hinglish_count = sum(1 for word in words if word in hinglish_words)
    
    if hinglish_count >= 2:
        return "hinglish"
        
    return "en"

def get_language_instruction(lang_code: str) -> str:
    """Returns a string to inject into any system prompt based on language code."""
    if lang_code == "hi":
        return "IMPORTANT: The user is writing in Hindi. You MUST reply entirely in Hindi (Devanagari script). Use simple, clear Hindi that a common citizen can understand. Legal terms can stay in English."
    elif lang_code == "hinglish":
        return "IMPORTANT: The user is writing in Hinglish (Hindi-English mix). You MUST reply in Hinglish — use simple Hindi words mixed with English for legal terms. Do NOT reply in pure English."
    
    return ""
