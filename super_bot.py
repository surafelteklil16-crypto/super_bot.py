import os
import threading
import time

from flask import Flask
import telebot

# =========================
# 1. ENVIRONMENT VARIABLES
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")        # Telegram Bot Token
ADMIN_ID = os.getenv("ADMIN_ID")          # Telegram Admin ID (number)

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

# =========================
# 2. TELEGRAM BOT SETUP
# =========================
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.reply_to(
        message,
        "✅ Bot is running on Koyeb (Free plan)\n\nSend any message."
    )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"📩 You said:\n{message.text}")

# =========================
# 3. BOT RUNNER (BACKGROUND)
# =========================
def start_bot():
    print("🤖 Telegram bot started...")
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print("Bot error:", e)
            time.sleep(5)

# =========================
# 4. FLASK WEB SERVER (FAKE WEB)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is alive and running!"

# =========================
# 5. MAIN ENTRY POINT
# =========================
if __name__ == "__main__":
    # Run Telegram bot in background thread
    threading.Thread(target=start_bot).start()

    # Run Flask web server (required by Koyeb Free)
    app.run(host="0.0.0.0", port=8000)
