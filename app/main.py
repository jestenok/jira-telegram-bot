from aiohttp import web
from app import create_app


if __name__ == '__main__':
    web.run_app(create_app(),
                access_log=None,
                port=8080)
