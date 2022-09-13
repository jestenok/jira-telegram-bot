from telegram import ForceReply, Update
from aiohttp import web
from app.settings import bot
from app.models import User
import static_text


async def telegram_handle(request):
    json = await request.json()
    print(json)
    update = Update.de_json(json, bot)

    callback_query = getattr(update, 'callback_query')
    if callback_query:
        u = User.get_user_from_update(update)

        issue_id, status_id = callback_query.data.split('/')

        jira = u.jira_session()
        jira.transition_issue(issue_id, status_id)
        return web.Response()

    if getattr(update.message, 'reply_to_message'):
        await reply_to_message(update)
        return web.Response()

    match update.message.text:
        case '/start':
            await start(update)
        case '/jira':
            await jira_account(update)

    return web.Response()


async def start(update) -> None:
    u = User.get_user_from_update(update)

    await update.message.reply_html(
        rf"Hi {u}!",
        reply_markup=ForceReply(selective=True),
    )


async def reply_to_message(update):
    u = User.get_user_from_update(update)

    if update.message.reply_to_message.entities[0]['url'] == static_text.jira_auth_link:
        if len(update.message.text) <= 15:
            await update.message.reply_text("Не название, а сам токен")
        elif not u.jira_session(update.message.text):
            await update.message.reply_text("Неверный токен доступа")
        else:
            await update.message.reply_text("Аккаунт jira успешно привязан")


async def jira_account(update) -> None:
    await update.message.reply_html(static_text.jira_auth,
                                    reply_markup=ForceReply(selective=True))
