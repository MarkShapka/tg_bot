from telegram import Update, BotCommand, MenuButtonCommands, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler

from openapi_client import OpenAIClient
from utils import load_messages, load_images

AWAITING_MESSAGE = 1


# start menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = load_messages("menu")
    bot = context.bot
    image_file = load_images("start_tg_bot.jpg")

    await bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("random", "Any random fact about python"),
        BotCommand("gpt", "Chat with GPT"),
        BotCommand("exit", "Exit GPT mode"),
    ])

    # await bot.set_chat_menu_button(update.effective_chat.id, MenuButtonCommands())
    # await update.message.reply_text(text)
    await bot.set_chat_menu_button(update.effective_chat.id, MenuButtonCommands())
    if update.message:
        await update.message.reply_photo(photo=image_file, caption=text)
    else:
        await update.effective_chat.send_photo(photo=image_file, caption=text)


# random fact query
async def random(update: Update, context: CallbackContext) -> None:
    openai_client = OpenAIClient()
    fact_prompt = load_messages("random_prompt")
    python_fact = await openai_client.ask(user_msg="", system_prompt=fact_prompt)

    image_file = load_images("random_facts.png")

    keyboard = [
        [InlineKeyboardButton("🔄 Хочу ще факт", callback_data="random")],
        [InlineKeyboardButton("🏠 Закінчити", callback_data="start")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.message or update.callback_query.message

    await message.reply_photo(photo=image_file, caption=python_fact, reply_markup=reply_markup)


# GPT chat
async def gpt_start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Write your question: ")
    return AWAITING_MESSAGE


async def gpt_conversation(update: Update, context: CallbackContext) -> int:
    user_msg = update.message.text

    keyboard = [
        [InlineKeyboardButton("🏠 Закінчити", callback_data="start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    response = await OpenAIClient().ask(user_msg=user_msg)

    message = update.message or update.callback_query.message

    await message.reply_text(text=response, reply_markup=reply_markup)
    return AWAITING_MESSAGE


async def gpt_end(update: Update, context: CallbackContext) -> int:
    menu_text = load_messages("menu")
    await update.message.reply_text(f"The GPT conversation has ended!\n\n{menu_text}")
    return ConversationHandler.END
