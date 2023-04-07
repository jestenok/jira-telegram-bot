from aiohttp import web

from remote.handlers.tg import telegram_handle
from remote.handlers.jira import jira_handle
from remote.handlers.health import health_handle


def create_routes(token):
    routes = [web.post(f'/{token}/', telegram_handle),
              web.post(f'/{token}/jira/tasks/', jira_handle),
              web.get(f'/{token}/health/', health_handle)]
    return routes
