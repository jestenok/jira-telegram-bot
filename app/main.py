from settings import init_db, TOKEN, USE_WEBHOOK
from aiohttp import web
from remote.router import create_routes
from remote.middleware import log_middleware
import logging
from bot import app_tg


if __name__ == '__main__':
    init_db()
    logging.info('DB initialized')

    if USE_WEBHOOK:
        logging.info('Starting server')

        app = web.Application()
        app.add_routes(create_routes(TOKEN))
        app.middlewares.append(log_middleware)

        web.run_app(app,
                    access_log=None,
                    port=8080)
    else:
        logging.info('Starting pooling')
        app_tg.run_polling()
