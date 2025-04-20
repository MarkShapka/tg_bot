from telegram.ext import CommandHandler, ConversationHandler, \
    MessageHandler, filters, Application, CallbackQueryHandler

from app.bot.commands import start, gpt_start, gpt_conversation, gpt_end, random, talk, set_celebrity
from bot.buttons import button_handler
from config import TG_BOT_API_KEY
from utils import MessageType

app = Application.builder().token(TG_BOT_API_KEY).build()
app.add_handler(CommandHandler("start", start))

app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("gpt", gpt_start)],
    states={MessageType.GPT_CHAT.value: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_conversation)
    ]
    },
    fallbacks=[CommandHandler("start", start)],
))

app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("talk", talk)],
    states={
        MessageType.SET_CELEBRITY.value: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, set_celebrity),
            # CallbackQueryHandler(set_celebrity),
        ],
        MessageType.GPT_CHAT.value: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_conversation),
            # CallbackQueryHandler(gpt_conversation),
            # CommandHandler("end", end_conversation)
        ],
    },
    # fallbacks=[CommandHandler("start", start)],
    fallbacks=[CommandHandler("start", start)]
))

app.add_handler(CommandHandler("random", random))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
