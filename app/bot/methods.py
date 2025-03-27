from telegram import Update, BotCommand, MenuButtonCommands
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler

from openapi_client import OpenAIClient
from utils import load_messages

AWAITING_MESSAGE = 1

# start menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = load_messages("menu")
    bot = context.bot

    await bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("random", "Any random fact about python"),
        BotCommand("gpt", "Chat with GPT"),
        BotCommand("exit", "Exit GPT mode"),
    ])

    # await bot.set_chat_menu_button(update.effective_chat.id, MenuButtonCommands())
    # await update.message.reply_text(text)
    await bot.set_chat_menu_button(update.effective_chat.id, MenuButtonCommands())
    await update.effective_chat.send_message(text)


# GPT chat
async def gpt_start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Write your question: ")
    return AWAITING_MESSAGE


async def gpt_conversation(update: Update, context: CallbackContext) -> int:
    user_msg = update.message.text
    response = await OpenAIClient().ask(user_msg=user_msg)
    await update.message.reply_text(response)
    return AWAITING_MESSAGE


async def gpt_end(update: Update, context: CallbackContext) -> int:
    menu_text = load_messages("menu")
    await update.message.reply_text(f"The GPT conversation has ended!\n\n{menu_text}")
    return ConversationHandler.END