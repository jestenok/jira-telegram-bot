from aiohttp import web
from service.tg.bot import app_tg
from telegram import Update


async def telegram_handle(request):
    json = await request.json()
    update = Update.de_json(json, app_tg.bot)

    await app_tg.process_update(update)

    return web.Response()
