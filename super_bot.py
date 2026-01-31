import os
import threading
import telebot
from flask import Flask

# ================= ENV =================
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set")

bot = telebot.TeleBot(BOT_TOKEN)

# ================= FLASK APP =================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# ================= TELEGRAM BOT =================
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "👋 Bot is alive and running!")

def run_bot():
    bot.infinity_polling(skip_pending=True)

# ================= MAIN =================
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
