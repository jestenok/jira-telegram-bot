from settings import init_db, TG_TOKEN, TG_USE_WEBHOOK

import logging
from service.tg.bot import app_tg

if TG_USE_WEBHOOK:
    from aiohttp import web
    from remote.router import create_routes
    from remote.middleware import log_middleware


if __name__ == '__main__':
    init_db()
    logging.info('DB initialized')

    if TG_USE_WEBHOOK:
        app = web.Application()
        app.add_routes(create_routes(TG_TOKEN))
        app.middlewares.append(log_middleware)

        web.run_app(app,
                    access_log=None,
                    port=8080)
    else:
        app_tg.run_polling()
