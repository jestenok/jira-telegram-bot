from telegram import ForceReply, Update
from aiohttp import web
from settings import jira, bot
from models import User


commands = {}


def add_to_commands(command):
    def dec(func):
        global commands
        commands[command] = func

        def wrapper(*args):
            func(*args)
        return wrapper
    return dec


async def telegram_handle(request):
    json = await request.json()
    print(json)
    update = Update.de_json(json, bot)

    callback_query = getattr(update, 'callback_query')
    if callback_query:
        issue_id, status_id = callback_query.data.split('/')
        jira.transition_issue(issue_id, status_id)
    else:
        await commands.get(update.message.text, commands.get('/default'))(update)
    return web.Response()


@add_to_commands('/start')
async def start(update) -> None:
    u = User.get_user_from_update(update)

    await update.message.reply_html(
        rf"Hi {u}!",
        reply_markup=ForceReply(selective=True),
    )


@add_to_commands('/default')
async def help_command(update) -> None:
    u = User.get_user_from_update(update)
    message = update.message

    if getattr(message, 'reply_to_message'):
        if getattr(message.reply_to_message, 'text') == 'Введите ваше имя пользователя в jira':
            u.edit(jira_username=message.text.lower())
            await update.message.reply_text("Аккаунт jira успешно привязан")


@add_to_commands('/jira')
async def jira_account(update) -> None:
    u = User.get_user_from_update(update)
    await update.message.reply_html("Введите ваше имя пользователя в jira",
                                    reply_markup=ForceReply(selective=True))
