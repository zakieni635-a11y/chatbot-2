import json
from fuzzywuzzy import fuzz

# Load FAQ
with open("faq_toko.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# Daftar kata kasar
bad_words = ["bodoh", "anjing", "babi", "goblok", "bangsat", "brengsek"]

def get_bot_reply(user_text):
    user_text_lower = user_text.lower().strip()

    # Cek kata kasar dulu
    for word in bad_words:
        if word in user_text_lower:
            return "Mohon gunakan bahasa yang sopan ya 😇"

    # Fuzzy matching FAQ
    best_score = 0
    best_answer = None
    for item in faq_data:
        for keyword in item.get("keywords", []):
            score = fuzz.partial_ratio(user_text_lower, keyword.lower())
            if score > best_score:
                best_score = score
                best_answer = item.get("answer")

    # Threshold minimal untuk dianggap matching
    if best_score >= 60:
        return best_answer

    # Jika tidak ada yang cocok
    return "Maaf, saya tidak mengerti pertanyaan Anda. Silakan tanyakan hal lain."
