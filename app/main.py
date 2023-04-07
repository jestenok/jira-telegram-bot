import httpx

from settings import init_db, TOKEN, USE_WEBHOOK, HOSTNAME
from aiohttp import web
from remote.router import create_routes
from remote.middleware import log_middleware
import logging
from service.tg.bot import app_tg


if __name__ == '__main__':
    init_db()
    logging.info('DB initialized')

    if USE_WEBHOOK:
        httpx.get(f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={HOSTNAME}/{TOKEN}/')
        logging.info('Webhook set')

        app = web.Application()
        app.add_routes(create_routes(TOKEN))
        app.middlewares.append(log_middleware)

        web.run_app(app,
                    access_log=None,
                    port=8080)
    else:
        httpx.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook?url={HOSTNAME}/{TOKEN}/')
        logging.info('Webhook deleted')

        app_tg.run_polling()
