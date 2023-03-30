from aiohttp import web
from settings import bot
from telegram import Update
from models import User
import commands


async def telegram_handle(request):
    json = await request.json()

    print('-'*15)
    print(json)
    print()

    update = Update.de_json(json, bot)

    callback_query = getattr(update, 'callback_query')
    if callback_query:
        u = User.get_user_from_update(update)

        issue_id, status_id = callback_query.data.split('/')

        jira = u.jira_session()
        jira.transition_issue(issue_id, status_id)

    elif update.message.text[0] == '/':
        match update.message.text.lower():
            case '/start':
                await commands.jira_account(update)
            case '/jira':
                await commands.jira_account(update)

    elif getattr(update.message, 'reply_to_message'):
        await commands.reply_to_message(update)

    else:
        await commands.text_message(update)

    return web.Response()
