from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from bot_logic import get_bot_reply
import os

TOKEN = os.getenv("8320510931:AAE3xWEStU_G1mEzmonQdydKSbO-hlG2aqM")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = get_bot_reply(update.message.text)
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Telegram Bot sudah berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
