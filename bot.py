from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# Define states
ENCODE, DECODE = range(2)

# Start command handler
async def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I'm your Image Steganography Bot. "
        "Please choose an option:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("/encode"), KeyboardButton("/decode")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    return ENCODE

# Encode command handler
async def encode(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Please send the image you want to encode.")
    return ENCODE

# Decode command handler
async def decode(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Please send the image you want to decode.")
    return DECODE

# Handle image for encoding
async def handle_encode_image(update: Update, context: CallbackContext) -> int:
    # Implement your encoding logic here
    await update.message.reply_text("Encoding process started.")
    return ConversationHandler.END

# Handle image for decoding
async def handle_decode_image(update: Update, context: CallbackContext) -> int:
    # Implement your decoding logic here
    await update.message.reply_text("Decoding process started.")
    return ConversationHandler.END

# Cancel command handler
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

# Main function to set up the bot
def main() -> None:
    application = Application.builder().token("7925828409:AAFMg6AsVIPQ_rZWUh6o-bUkG0-Znv9_AmQ").build()

    # Define the conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ENCODE: [
                CommandHandler("encode", encode),
                MessageHandler(filters.PHOTO, handle_encode_image),
            ],
            DECODE: [
                CommandHandler("decode", decode),
                MessageHandler(filters.PHOTO, handle_decode_image),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add the conversation handler to the application
    application.add_handler(conversation_handler)

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
