import os
import uuid
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# vaqtinchalik storage
user_files = {}

# 🎛️ START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 Music Remover Bot\nAudio yuboring (mp3/wav)"
    )

# 🎵 AUDIO QABUL
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏳ Processing...")

    file = await update.message.audio.get_file()
    file_id = str(uuid.uuid4())

    input_path = f"{file_id}.mp3"
    await file.download_to_drive(input_path)

    # 🎧 DEMUCS ishlatish (system command)
    os.system(f"demucs --two-stems=vocals {input_path}")

    folder = f"separated/htdemucs/{file_id}"
    vocals = f"{folder}/vocals.wav"
    instrumental = f"{folder}/no_vocals.wav"

    user_files[file_id] = {
        "vocals": vocals,
        "inst": instrumental
    }

    keyboard = [
        [
            InlineKeyboardButton("🎤 Vocals", callback_data=f"vocals|{file_id}"),
            InlineKeyboardButton("🎧 Instrumental", callback_data=f"inst|{file_id}")
        ]
    ]

    await msg.edit_text(
        "✅ Tayyor! Qaysi kerak?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🎛️ BUTTON HANDLER
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, file_id = query.data.split("|")

    if file_id not in user_files:
        await query.message.reply_text("❌ File topilmadi")
        return

    path = user_files[file_id][action]

    await query.message.reply_audio(audio=open(path, "rb"))

    # 🗑 tozalash
    try:
        os.remove(path)
    except:
        pass

# ▶️ RUN
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    app.add_handler(CallbackQueryHandler(buttons))

    app.run_polling()
