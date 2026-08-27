import json
import random
import os

random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/datasets")
OUTPUT_PATH = os.path.join(DATA_DIR, "intent_training_v2.jsonl")

politicians = [
    "Narendra Modi", "Rahul Gandhi", "Arvind Kejriwal", "Amit Shah", "Yogi Adityanath",
    "Mamata Banerjee", "Priyanka Gandhi", "Smriti Irani", "Nirmala Sitharaman", "Rajnath Singh",
    "S Jaishankar", "Draupadi Murmu", "Jagdeep Dhankhar", "DY Chandrachud",
    "the Prime Minister", "the Chief Minister", "the Governor", "the MLA", "the MP"
]

posts = [
    "Prime Minister of India", "Chief Justice", "President of India", "current CBI director",
    "head of SEBI", "Attorney General", "RBI governor", "governor of Maharashtra",
    "Chief Minister of Delhi", "Finance Minister", "Home Minister"
]

parties = [
    "BJP", "Congress", "AAP", "NDA coalition", "INDIA alliance", "UPA",
    "Lok Sabha", "Rajya Sabha", "the Speaker of Lok Sabha", "the role of the Governor",
    "TMC", "Shiv Sena", "BSP", "Samajwadi Party"
]

institutions = [
    "Supreme Court", "High Court", "CBI", "ED", "NHRC", "CAG",
    "Election Commission", "SEBI", "RBI", "UIDAI", "NIA", "district court"
]

cat_a_en_templates = ["who is {pol}?", "tell me about {pol}", "what does {pol} do?", "is {pol} a minister?"]
cat_a_hinglish_templates = ["kaun hai {pol}?", "{pol} kaun hai?", "{pol} ke baare mein batao", "{pol} kya karte hain?"]
cat_a_hi_templates = ["mujhe {pol} ke baare me janna hai", "{pol} koun hai", "kya {pol} neta hai", "{pol} ka kaam kya hai"]

cat_b_en_templates = ["who is the {post}?", "tell me who is the {post}", "current {post} name"]
cat_b_hinglish_templates = ["{post} kaun hai abhi?", "current {post} kaun hai?", "{post} ka naam kya hai"]
cat_b_hi_templates = ["abhi ka {post} koun hai", "humaara {post} koun hai", "kya aapko {post} pata hai"]

cat_c_en_templates = ["what is {party}?", "what does {party} stand for?", "explain {party}", "how many MPs are in {party}?"]
cat_c_hinglish_templates = ["{party} kya hai?", "{party} ke baare mein batao", "{party} ka matlab kya hai"]
cat_c_hi_templates = ["mujhe {party} ke baare me bataiye", "{party} ke neta koun hai", "kya hai {party}"]

cat_d_en_templates = ["what is the {inst}?", "what does the {inst} do?", "explain the role of {inst}"]
cat_d_hinglish_templates = ["{inst} kya karta hai?", "{inst} ke baare mein batao", "{inst} kya hai?"]
cat_d_hi_templates = ["{inst} kya hota hai", "{inst} ka kya kaam hai", "mujhe {inst} ke baare me bataiye"]


def gen_samples(templates_en, templates_hinglish, templates_hi, entities, total=100):
    samples = []
    
    # 50% en, 30% hinglish, 20% hindi
    target_en = int(total * 0.5)
    target_hinglish = int(total * 0.3)
    target_hi = total - target_en - target_hinglish
    
    def fill(count, tmpl_list):
        res = []
        for _ in range(count):
            t = random.choice(tmpl_list)
            e = random.choice(entities)
            # Find the placeholder
            ph = ""
            if "{pol}" in t: ph = "{pol}"
            elif "{post}" in t: ph = "{post}"
            elif "{party}" in t: ph = "{party}"
            elif "{inst}" in t: ph = "{inst}"
            
            text = t.replace(ph, e) if ph else t
            
            if random.random() < 0.3:
                text = text.lower()
            if random.random() < 0.2:
                text = text.replace("?", "")
                
            res.append({"text": text.strip(), "label": "Civic_Info"})
        return res

    samples.extend(fill(target_en, templates_en))
    samples.extend(fill(target_hinglish, templates_hinglish))
    samples.extend(fill(target_hi, templates_hi))
    
    return samples

def main():
    cat_a = gen_samples(cat_a_en_templates, cat_a_hinglish_templates, cat_a_hi_templates, politicians, 100)
    cat_b = gen_samples(cat_b_en_templates, cat_b_hinglish_templates, cat_b_hi_templates, posts, 100)
    cat_c = gen_samples(cat_c_en_templates, cat_c_hinglish_templates, cat_c_hi_templates, parties, 100)
    cat_d = gen_samples(cat_d_en_templates, cat_d_hinglish_templates, cat_d_hi_templates, institutions, 100)
    
    all_samples = cat_a + cat_b + cat_c + cat_d
    random.shuffle(all_samples)
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
        for s in all_samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
            
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        lines = len(f.readlines())
        
    print(f"Added {len(all_samples)} Civic_Info samples. Total lines in intent_training_v2.jsonl: {lines}")

if __name__ == "__main__":
    main()
