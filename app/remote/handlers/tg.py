from aiohttp import web
from settings import bot
from telegram import Update
from service import tg


async def telegram_handle(request):
    json = await request.json()
    update = Update.de_json(json, bot)

    if getattr(update, 'callback_query'):
        tg.events.callback_query(update)

    elif update.message.photo:
        await tg.events.photo_message(update)

    elif update.message.text[0] == '/':
        await tg.events.text_message(update)

    elif getattr(update.message, 'reply_to_message'):
        await tg.events.reply_to_message(update)

    elif update.message.text:
        await tg.events.text_message(update)

    return web.Response()
