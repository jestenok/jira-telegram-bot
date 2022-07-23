from settings import init_db, TOKEN
from commands import telegram_handle
from jira_webhook.jira import jira_handle

from aiohttp import web


app = web.Application()
app.add_routes([web.post(f'/{TOKEN}/', telegram_handle)])
app.add_routes([web.post(f'/jira/tasks/', jira_handle)])


if __name__ == '__main__':
    init_db()
    web.run_app(app)
