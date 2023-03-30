from settings import init_db
from aiohttp import web
from remote.router import new_app


if __name__ == '__main__':
    print('Starting server')
    init_db()
    print('DB initialized')
    web.run_app(new_app(),
                port=8080)
