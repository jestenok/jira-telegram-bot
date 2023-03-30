from aiohttp import web
from remote.handlers.tg import telegram_handle
from remote.handlers.jira import jira_handle
from settings import TOKEN


def new_app():
    app = web.Application()
    app.add_routes([web.post(f'/{TOKEN}/', telegram_handle),
                    web.post('/jira/tasks/', jira_handle),
                    web.get('/health/', health)])
    return app


async def health():
    return web.StreamResponse(status=200)
