from telegram import Update


async def text(update: Update, _) -> None:
    await update.message.reply_text("Не понимаю, что ты от меня хочешь")

