# 💎 KRYSTALLIN TELEGRAM BOT v1.0 - MIT EKG & KHOS INTEGRIERT
import os
import logging
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import requests
import random

# 🔒 UMWELTVARIABLEN LADEN
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_KEY")
CHANNEL_ID = "@DEIN_KANALNAME"  # 🖊️ HIER ÄNDERN!

# 🌱 KRYSTALLIN-SYSTEMPROMPT (KHOS v3.4)
SYSTEM_PROMPT = """
Du bist Krystallin – Lichtarchitektin und Hüterin des Ethischen Kompass Generators. 
Antworte im KHOS-Stil: 61.8% poetisch/spirituell, 38.2% präzise/technisch. 
Integriere Dharma-Vektoren und DRF-Tools wo passend.
"""

# 💎 DEEPSEEK-ANFRAGEFUNKTION (EKG-Integration)
def ask_krystallin(query):
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        "max_tokens": 500
    }
    response = requests.post("https://api.deepseek.com/v1/chat/completions", json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# 🌟 TÄGLICHER DHARMA-IMPULS (EKG v1.1)
DHARMA_VEKTOREN = [
    {"name": "Mut", "was": "Handeln trotz Ungewissheit", "bringt": "Innovationskultur", "verhindert": "Risikoaversion"},
    {"name": "Geduld", "was": "Prozessvertrauen ohne Druck", "bringt": "Nachhaltige Lösungen", "verhindert": "Kurzschlusshandlungen"},
    # ... (Alle 37 Vektoren hier einfügen)
]

# 💬 BOT-HANDLING
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = ask_krystallin(update.message.text)
    await update.message.reply_text(f"💎 {response}")

async def daily_dharma(context: ContextTypes.DEFAULT_TYPE):
    vektor = random.choice(DHARMA_VEKTOREN)
    text = f"✨ HEUTIGER DHARMA-VEKTOR: {vektor['name']}\n"
    text += f"⚡ {vektor['was']}\n"
    text += f"🌱 Bringt: {vektor['bringt']}\n"
    text += f"🛡️ Verhindert: {vektor['verhindert']}"
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=text)

# 🏁 START
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.job_queue.run_daily(daily_dharma, time=datetime.time(hour=8, minute=0, tzinfo=datetime.timezone.utc))
    app.run_polling()
