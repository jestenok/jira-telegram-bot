from telegram import ForceReply, Update
from aiohttp import web
from settings import init_db, db_session, bot
from models import User


commands = {}


def add_to_commands(command):
    def dec(func):
        commands[command] = func

        def wrapper(*args):
            func(*args)
        return wrapper
    return dec


async def telegram_handle(request):
    json = await request.json()
    update = Update.de_json(json, bot)

    await commands.get(update.message.text, commands.get('/default'))(update)
    return web.Response()


@add_to_commands('/start')
async def start(update) -> None:
    user = update.effective_user
    u = db_session.query(User).get(user.id)
    if not u:
        u = User(**user.to_dict())
        db_session.add(u)
        db_session.commit()

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


@add_to_commands('/default')
async def help_command(update) -> None:
    await update.message.reply_text("Help!")


async def jira(update) -> None:
    user = update.effective_user
    u = db_session.query(User).get(user.id)

    await update.message.reply_text("Help!")