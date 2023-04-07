from telegram.ext import Application, CommandHandler, MessageHandler, filters
from service.tg.commands import start, jira
from service.tg.handlers import text_message
from settings import TOKEN
import asyncio


def create_app(token):
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('jira', jira))

    app.add_handler(MessageHandler(filters.TEXT, text_message))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.initialize())

    return app


app_tg = create_app(TOKEN)
