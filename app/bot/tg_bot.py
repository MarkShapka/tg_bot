from telegram.ext import CommandHandler, ConversationHandler, \
    MessageHandler, filters, Application, CallbackQueryHandler

from app.bot.methods import start, gpt_start, gpt_conversation, gpt_end, AWAITING_MESSAGE, random, button_handler
from config import TG_BOT_API_KEY

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
