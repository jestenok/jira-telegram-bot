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

from settings import TG_TOKEN, TG_HOST, TG_USE_WEBHOOK
import asyncio
import atexit


def create_app(token, use_webhook=False, host=None):
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('jira', jira))

    app.add_handler(CallbackQueryHandler(callback_query))

    app.add_handler(MessageHandler(filters.PHOTO, photo))
    app.add_handler(MessageHandler(filters.REPLY, reply))
    app.add_handler(MessageHandler(filters.TEXT, text))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.initialize())

    if use_webhook:
        loop.run_until_complete(app.bot.set_webhook(f'{host}/jira-telegram-bot/{token}/'))
        atexit.register(
            lambda: loop.run_until_complete(
                app.bot.delete_webhook(f'{TG_HOST}/{TG_TOKEN}/')))
    elif host:
        loop.run_until_complete(app.bot.delete_webhook(f'{host}/jira-telegram-bot/{token}/'))

    return app


app_tg = create_app(TG_TOKEN, TG_USE_WEBHOOK, TG_HOST)
