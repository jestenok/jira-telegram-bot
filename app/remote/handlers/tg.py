from aiohttp import web
from settings import bot
from telegram import Update
from service. import events


async def telegram_handle(request):
    json = await request.json()
    update = Update.de_json(json, bot)

    if getattr(update, 'callback_query'):
        events.callback_query(update)

    elif update.message.photo:
        await events.photo_message(update)

    elif update.message.text[0] == '/':
        await events.text_message(update)

    elif getattr(update.message, 'reply_to_message'):
        await events.reply_to_message(update)

    elif update.message.text:
        await events.text_message(update)

    return web.Response()
