from telegram import Update
from telegram.ext import CallbackContext

from bot.commands import random, start, set_celebrity


async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "random":
        await random(update, context)
    elif query.data == "start":
        await start(update, context)
    elif query.data in ["jolie", "johnson", "wahlberg"]:
        await set_celebrity(update, context)
