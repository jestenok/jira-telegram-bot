from settings import init_db, db_session, TOKEN
from commands import telegram_handle

from aiohttp import web


app = web.Application()
app.add_routes([web.post(f'/{TOKEN}/', telegram_handle)])


if __name__ == '__main__':
    web.run_app(app)
