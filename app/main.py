from settings import init_db
from aiohttp import web
from remote.router import new_app


if __name__ == '__main__':
    init_db()
    web.run_app(new_app(),
                port=8080)
