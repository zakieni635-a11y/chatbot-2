import json
import os
from fuzzywuzzy import fuzz

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAQ_PATH = os.path.join(BASE_DIR, "faq_toko.json")

try:
    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
except Exception as e:
    print("Gagal load faq_toko.json:", e)
    faq_data = []

bad_words = ["bodoh", "anjing", "babi", "goblok", "bangsat", "brengsek"]

def get_bot_reply(user_text: str) -> str:
    if not user_text:
        return "Boleh tulis pertanyaannya ya 😊"

    text = user_text.lower().strip()

    for word in bad_words:
        if word in text:
            return "Mohon gunakan bahasa yang sopan ya 😇"

    best_score = 0
    best_answer = None

    for item in faq_data:
        for keyword in item.get("keywords", []):
            score = fuzz.partial_ratio(text, keyword.lower())
            if score > best_score:
                best_score = score
                best_answer = item.get("answer")

    if best_score >= 60 and best_answer:
        return best_answer

    return "Maaf, saya belum memahami pertanyaan kak 😊"
