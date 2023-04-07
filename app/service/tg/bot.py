from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from service.tg.handlers.commands import start, jira
from service.tg.handlers.photo import photo
from service.tg.handlers.text import text
from service.tg.handlers.callback import callback_query
from service.tg.handlers.reply import reply

from settings import TOKEN
import asyncio


def create_app(token):
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('jira', jira))

    app.add_handler(CallbackQueryHandler(callback_query))

    app.add_handler(MessageHandler(filters.PHOTO, photo))
    app.add_handler(MessageHandler(filters.REPLY, reply))
    app.add_handler(MessageHandler(filters.TEXT, text))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.initialize())

    return app


app_tg = create_app(TOKEN)
