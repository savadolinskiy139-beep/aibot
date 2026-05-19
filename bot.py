import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

TOKEN = "8801939949:AAGjzr-oMwrsjD7G4pRGFItt9HsjFIqhIN0"
GROQ_API_KEY = "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"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь текст 🚀"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    await update.message.chat.send_action("typing")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "Ты AI-помощник."
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=15
    )

    ai_text = response.json()["choices"][0]["message"]["content"]

    await update.message.reply_text(ai_text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

print("Бот работает...")

app.run_polling()
