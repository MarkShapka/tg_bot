from telegram import Update
from telegram.ext import CallbackContext

from bot.commands import random, start


async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "random":
        await random(update, context)
    elif query.data == "start":
        await start(update, context)