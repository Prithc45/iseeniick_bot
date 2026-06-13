import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN")
YOUR_USER_ID = int(os.environ.get("YOUR_USER_ID"))
GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")

# Flask keep-alive
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive"

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

async def send_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != YOUR_USER_ID:
        await update.message.reply_text("Unauthorized.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /send your message here")
        return
    message = " ".join(context.args)
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
    await update.message.reply_text("✅ Sent!")

async def relay_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != YOUR_USER_ID:
        return
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=update.message.text)
    await update.message.reply_text("✅ Sent!")

Thread(target=run_flask).start()

bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("send", send_command))
bot_app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, relay_message))

print("Bot running...")
bot_app.run_polling()
