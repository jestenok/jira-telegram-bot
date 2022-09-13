from aiohttp import web
from app.commands import telegram_handle
from app.jira import jira_handle
from app.settings import TOKEN


def new_app():
    app = web.Application()
    app.add_routes([web.post(f'/{TOKEN}/', telegram_handle)])
    app.add_routes([web.post(f'/jira/tasks/', jira_handle)])

    return app