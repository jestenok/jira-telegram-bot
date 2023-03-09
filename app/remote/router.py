from aiohttp import web
from remote.handlers.tg import telegram_handle
from remote.handlers.jira import jira_handle
from settings import TOKEN


def new_app():
    app = web.Application()
    app.add_routes([web.post(f'/{TOKEN}/', telegram_handle)])
    app.add_routes([web.post(f'/jira/tasks/', jira_handle)])
    app.add_routes([web.get(f'/test/', test)])
    #
    return app


def test(r):
    return web.Response()