import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from spleeter.separator import Separator

# AI model
separator = Separator('spleeter:2stems')  # vocals + instrumental

BOT_TOKEN = "YOUR_BOT_TOKEN"

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.audio.get_file()
    
    input_path = "input.mp3"
    output_dir = "output"

    await file.download_to_drive(input_path)

    # AI ajratish
    separator.separate_to_file(input_path, output_dir)

    # Natija path
    base = os.path.splitext(os.path.basename(input_path))[0]
    vocal_path = f"{output_dir}/{base}/vocals.wav"
    inst_path = f"{output_dir}/{base}/accompaniment.wav"

    # Foydalanuvchiga yuborish
    await update.message.reply_audio(audio=open(vocal_path, 'rb'), caption="Vocals")
    await update.message.reply_audio(audio=open(inst_path, 'rb'), caption="Instrumental")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.AUDIO, handle_audio))

app.run_polling()
