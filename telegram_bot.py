import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

from bot_logic import get_bot_reply
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# =============================
# LOGGING
# =============================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

# =============================
# ENV VAR
# =============================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN belum diset")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY belum diset")

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# =============================
# GROQ INIT
# =============================
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.3
)

conversation_history = {}

# =============================
# /START
# =============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    conversation_history[chat_id] = []
    await update.message.reply_text(
        "Halo 👋 Saya Chatbot Zaky Fadillah Desain 🎨\n"
        "Silakan tanya atau pesan jasa desain 😊"
    )

# =============================
# MESSAGE HANDLER
# =============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    if chat_id not in conversation_history:
        conversation_history[chat_id] = []

    reply = get_bot_reply(user_text)

    # Jika FAQ tidak cocok → Groq AI
    if "belum memahami" in reply.lower() or "tidak mengerti" in reply.lower():
        try:
            history_text = ""
            for h in conversation_history[chat_id][-3:]:
                history_text += f"User: {h['user']}\nBot: {h['bot']}\n"

            prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    """
Kamu adalah admin Zaky Fadillah Desain.
Tugasmu:
1. Tangkap jasa desain (logo, banner, feed IG, dll).
2. Jika user ingin pesan, minta detail & WhatsApp.
3. Jawab harga, layanan, dan jam kerja.
4. Gunakan bahasa santai & ramah.
5. Fokus hanya pada Zaky Fadillah Desain.
"""
                ),
                ("human", "{history}\nUser: {input}")
            ])

            chain = prompt | llm
            ai_response = chain.invoke({
                "input": user_text,
                "history": history_text
            })
            reply = ai_response.content

        except Exception as e:
            logging.error("Groq error: %s", e)
            reply = "Maaf kak 🙏 sistem sedang sibuk. Coba lagi sebentar ya 😊"

    conversation_history[chat_id].append({
        "user": user_text,
        "bot": reply
    })

    await update.message.reply_text(reply)

# =============================
# MAIN
# =============================
def main():
    print("🤖 Bot Zaky Fadillah Desain sedang dijalankan...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
