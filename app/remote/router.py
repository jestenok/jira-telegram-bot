from aiohttp import web

from remote.handlers.tg import telegram_handle
from remote.handlers.jira import jira_handle
from remote.handlers.health import health_handle


def create_routes(token):
    routes = [web.post(f'/jira-telegram-bot/{token}/', telegram_handle),
              web.post(f'/jira-telegram-bot/{token}/jira/tasks/', jira_handle),
              web.get(f'/jira-telegram-bot/{token}/health/', health_handle)]
    return routes
