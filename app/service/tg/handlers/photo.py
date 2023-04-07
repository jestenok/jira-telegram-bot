from telegram import Update


async def photo(update: Update, _) -> None:
    await update.message.reply_text("Иди в пизду со своими фотокарточками")
