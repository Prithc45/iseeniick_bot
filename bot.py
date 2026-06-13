from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7693632230:AAFYbxZrfXFzrTPsKHRtYVh4vE5EJT5xpZE" 
YOUR_USER_ID = 6199574762
GROUP_CHAT_ID = "@iseeniickbabyyyy"

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

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("send", send_command))
app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, relay_message))

print("Bot running...")
app.run_polling()