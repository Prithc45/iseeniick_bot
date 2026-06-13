import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
YOUR_USER_ID = int(os.environ.get("YOUR_USER_ID"))
GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")

# ── Flask keep-alive ─────────────────────────────────────────

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive"

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

# ── Welcome ──────────────────────────────────────────────────

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.first_name
        await update.message.reply_text(
            f"Hi {name} welcome to iseeniick's territory 😻, "
            f"feel free to utilise this group for your needs "
            f"and stay safe, stay tuned. Peace out ✨"
        )

# ── /send text ───────────────────────────────────────────────

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

# ── /send file (caption must start with /send) ───────────────

async def send_file_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != YOUR_USER_ID:
        await update.message.reply_text("Unauthorized.")
        return

    msg = update.message

    # Check caption starts with /send
    caption = msg.caption or ""
    if not caption.lower().startswith("/send"):
        await msg.reply_text(
            "To send a file, attach it and set caption to /send\n"
            "Example caption: /send check this out"
        )
        return

    # Strip /send from caption text
    clean_caption = caption[5:].strip()

    # copy_message handles ALL file types automatically
    await context.bot.copy_message(
        chat_id=GROUP_CHAT_ID,
        from_chat_id=msg.chat_id,
        message_id=msg.message_id,
        caption=clean_caption if clean_caption else None
    )
    await msg.reply_text("✅ Sent!")

# ── Start ─────────────────────────────────────────────────────

Thread(target=run_flask).start()

bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

bot_app.add_handler(CommandHandler("send", send_command))
bot_app.add_handler(MessageHandler(
    filters.StatusUpdate.NEW_CHAT_MEMBERS,
    welcome
))
bot_app.add_handler(MessageHandler(
    filters.PHOTO | filters.VIDEO |
    filters.Document.ALL | filters.AUDIO |
    filters.VOICE | filters.Sticker.ALL,
    send_file_command
))

print("Bot running...")
bot_app.run_polling()
