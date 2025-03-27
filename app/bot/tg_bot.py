from telegram import BotCommand, MenuButtonCommands, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ConversationHandler, \
    MessageHandler, filters, Application, CallbackContext, CallbackQueryHandler

from app.bot.methods import start, gpt_start, gpt_conversation, gpt_end, AWAITING_MESSAGE
from config import TG_BOT_API_KEY
from openapi_client import OpenAIClient
from utils import load_messages, load_images


async def random(update: Update, context: CallbackContext) -> None:
    openai_client = OpenAIClient()
    fact_prompt = load_messages("random_prompt")
    python_fact = await openai_client.ask(user_msg="", system_prompt=fact_prompt)

    # Step 2: Select a random image from the resources folder
    image_file = load_images("random_facts.png")

    # Step 3: Create inline keyboard buttons
    keyboard = [
        [InlineKeyboardButton("🔄 Another Fact", callback_data="random")],
        [InlineKeyboardButton("🏠 End", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.message or update.callback_query.message

    # Step 4: Send the image if available
    await message.reply_photo(photo=image_file, caption=python_fact, reply_markup=reply_markup)


async def button_handler(update: Update, context: CallbackContext) -> None:
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data == "random":
        await random(update, context)  # Call the random fact function again
    elif query.data == "start":
        await start(update, context)  # Call the start function


app = Application.builder().token(TG_BOT_API_KEY).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("gpt", gpt_start)],
    states={AWAITING_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_conversation)]},
    fallbacks=[CommandHandler("exit", gpt_end)],
))
app.add_handler(CommandHandler("random", random))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()