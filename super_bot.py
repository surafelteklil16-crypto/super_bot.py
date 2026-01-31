import os
import time
import logging
from pybit.unified_trading import HTTP
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# -----------------------------
# 2️⃣ Logging (logs ለ Koyeb)
# -----------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# -----------------------------
# 3️⃣ Environment Variables
# -----------------------------
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")

if not all([BYBIT_API_KEY, BYBIT_API_SECRET, TELEGRAM_TOKEN, TELEGRAM_ADMIN_ID]):
    raise ValueError("❌ Missing environment variables")

TELEGRAM_ADMIN_ID = int(TELEGRAM_ADMIN_ID)

# -----------------------------
# 4️⃣ Bybit Session
# -----------------------------
bybit = HTTP(
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
    testnet=False,  # True ካልፈለግክ real account
)

# -----------------------------
# 5️⃣ Telegram Commands
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TELEGRAM_ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized")
        return

    await update.message.reply_text(
        "✅ Super Bot Started\n\n"
        "/balance - Check Bybit balance\n"
        "/ping - Bot status"
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Bot is running")


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TELEGRAM_ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized")
        return

    try:
        result = bybit.get_wallet_balance(accountType="UNIFIED")
        usdt = result["result"]["list"][0]["totalWalletBalance"]

        await update.message.reply_text(f"💰 Wallet Balance: {usdt} USDT")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# -----------------------------
# 6️⃣ Main App
# -----------------------------
def main():
    logging.info("🚀 Starting Super Bot...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("balance", balance))

    logging.info("🤖 Bot polling started")
    app.run_polling()


# -----------------------------
# 7️⃣ Run
# -----------------------------
if __name__ == "__main__":
    main()
