import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = ""

logging.basicConfig(level=logging.INFO)

# --- Шифрование в 16-ричную систему ---
def text_to_hex(text: str) -> str:
    return text.encode('utf-8').hex()

# --- Расшифровка ---
def hex_to_text(hex_str: str) -> str:
    try:
        return bytes.fromhex(hex_str).decode('utf-8')
    except:
        return "❌ Ошибка расшифровки. Проверь HEX-код."

# --- Обработка сообщений ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()

    # Проверяем — это HEX?
    if all(c in "0123456789abcdefABCDEF" for c in message):
        result = hex_to_text(message)
    else:
        result = text_to_hex(message)

    await update.message.reply_text(result)

# --- Старт ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Отправь текст — я его зашифрую.\n"
        "Отправь шифр — я расшифрую его обратно."
    )

# --- Запуск ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()