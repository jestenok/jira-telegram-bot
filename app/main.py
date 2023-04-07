from aiohttp import web
from remote.router import add_routes
from app import init_db
import logging


if __name__ == '__main__':
    logging.info('Starting server')

    init_db()
    logging.info('DB initialized')

    app = web.Application()
    add_routes(app)
    web.run_app(app,
                access_log=None,
                port=8080)
