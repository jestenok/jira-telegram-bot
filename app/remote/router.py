from aiohttp import web

from remote.handlers.tg import telegram_handle
from remote.handlers.jira import jira_handle
from remote.handlers.health import health_handle

from .middleware import log_middleware

from app import TOKEN


def add_routes(app: web.Application):
    app.middlewares.append(log_middleware)

    app.add_routes([web.post(f'/{TOKEN}/', telegram_handle),
                    web.post(f'/{TOKEN}/jira/tasks/', jira_handle),
                    web.get(f'/{TOKEN}/health/', health_handle)])
    return app
