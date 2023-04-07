from settings import init_db, TOKEN
from aiohttp import web
from remote.router import create_routes
from remote.middleware import log_middleware
import logging

if __name__ == '__main__':
    logging.info('Starting server')

    init_db()
    logging.info('DB initialized')

    app = web.Application()
    app.add_routes(create_routes(TOKEN))
    app.middlewares.append(log_middleware)

    web.run_app(app,
                access_log=None,
                port=8080)
