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

# ── /send file ───────────────────────────────────────────────

async def send_file_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != YOUR_USER_ID:
        await update.message.reply_text("Unauthorized.")
        return

    msg = update.message
    caption = msg.caption or ""

    # Strip /send from caption if present
    if caption.lower().startswith("/send"):
        caption = caption[5:].strip()

    if msg.photo:
        file_id = msg.photo[-1].file_id
        await context.bot.send_photo(chat_id=GROUP_CHAT_ID, photo=file_id, caption=caption)
        await msg.reply_text("✅ Photo sent!")

    elif msg.video:
        file_id = msg.video.file_id
        await context.bot.send_video(chat_id=GROUP_CHAT_ID, video=file_id, caption=caption)
        await msg.reply_text("✅ Video sent!")

    elif msg.document:
        file_id = msg.document.file_id
        await context.bot.send_document(chat_id=GROUP_CHAT_ID, document=file_id, caption=caption)
        await msg.reply_text("✅ File sent!")

    elif msg.audio:
        file_id = msg.audio.file_id
        await context.bot.send_audio(chat_id=GROUP_CHAT_ID, audio=file_id, caption=caption)
        await msg.reply_text("✅ Audio sent!")

    elif msg.voice:
        file_id = msg.voice.file_id
        await context.bot.send_voice(chat_id=GROUP_CHAT_ID, voice=file_id)
        await msg.reply_text("✅ Voice sent!")

    elif msg.sticker:
        file_id = msg.sticker.file_id
        await context.bot.send_sticker(chat_id=GROUP_CHAT_ID, sticker=file_id)
        await msg.reply_text("✅ Sticker sent!")

    else:
        await msg.reply_text("No file detected. Use /send text for messages.")

# ── Start ────────────────────────────────────────────────────

Thread(target=run_flask).start()

bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("send", send_command))
bot_app.add_handler(MessageHandler(
    filters.StatusUpdate.NEW_CHAT_MEMBERS,
    welcome
))
bot_app.add_handler(MessageHandler(
    filters.ChatType.PRIVATE & (
        filters.PHOTO | filters.VIDEO |
        filters.Document.ALL | filters.AUDIO |
        filters.VOICE | filters.Sticker.ALL
    ),
    send_file_command
))

print("Bot running...")
bot_app.run_polling()
