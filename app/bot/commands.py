from telegram import Update, BotCommand, MenuButtonCommands, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler

from openapi_client import OpenAIClient
from utils import load_messages, load_images, MessageType


# start menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = load_messages("menu")
    bot = context.bot
    image_file = load_images("start_tg_bot.jpg")

    await bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("random", "Any random fact about python"),
        BotCommand("gpt", "Chat with GPT"),
        BotCommand("talk", "Conversation with a celebrity"),
        BotCommand("quiz", "Questions"),
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
    await update.message.reply_text("Write your question to GPT: ")
    return MessageType.GPT_CHAT.value


async def gpt_conversation(update: Update, context: CallbackContext) -> int:
    user_msg = update.message.text
    print(user_msg)
    system_prompt = context.user_data.get("celebrity", load_messages("gpt_prompt"))

    keyboard = [
        [InlineKeyboardButton("🏠 Закінчити", callback_data="start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    response = await OpenAIClient().ask(user_msg=user_msg, system_prompt=system_prompt)

    message = update.message or update.callback_query.message

    await message.reply_text(text=response, reply_markup=reply_markup)
    return MessageType.GPT_CHAT.value


async def gpt_end(update: Update, context: CallbackContext) -> int:
    menu_text = load_messages("menu")
    await update.message.reply_text(f"The GPT conversation has ended!\n\n{menu_text}")
    return ConversationHandler.END


# Talk with a celebrity
async def talk(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("ANGELINA JOLIE", callback_data="jolie")],
        [InlineKeyboardButton("DWAYNE JOHNSON", callback_data="johnson")],
        [InlineKeyboardButton("MARK WAHLBERG", callback_data="wahlberg")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    title_for_select = "Select a celebrity from the list:"
    await update.message.reply_text(text=title_for_select, reply_markup=reply_markup)
    return MessageType.SET_CELEBRITY.value


async def set_celebrity(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    celebrity_map = {
        "jolie": load_messages("person_1_prompt"),
        "johnson": load_messages("person_2_prompt"),
        "wahlberg": load_messages("person_3_prompt")
    }

    context.user_data["celebrity"] = celebrity_map.get(query.data, load_messages("gpt_prompt"))

    await query.message.reply_text(
        f"✅ You've selected *{query.data.capitalize()}*!\nNow, type a message to chat with them."
    )

    return MessageType.GPT_CHAT.value
