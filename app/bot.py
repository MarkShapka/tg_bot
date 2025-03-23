from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from config import TG_BOT_API_KEY
from utils import load_messages


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = load_messages("menu")
    await update.message.reply_text(text)

app = ApplicationBuilder().token(TG_BOT_API_KEY).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()