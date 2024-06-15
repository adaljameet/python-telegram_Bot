import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import qrcode
from io import BytesIO

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the command handler function for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Send me any text and I will generate a QR code for you.')

# Define the message handler function for generating QR codes
async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    bio = BytesIO()
    bio.name = 'image.png'
    img.save(bio, 'PNG')
    bio.seek(0)

    await update.message.reply_photo(photo=bio, caption=f'QR code for: {text}')

# Define the main function to set up the bot
def main() -> None:
    # Replace 'YOUR_API_KEY_HERE' with your actual API key
    application = ApplicationBuilder().token("7225332376:AAEcBGj0Zv8hE2Zht_DbXxgGZiYwzili3o4").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr))

    application.run_polling()

if __name__ == '__main__':
    main()

