from database import init_db, db_session, dotenv_path
from models import User
from dotenv import load_dotenv
import os
import asyncio
from telegram import ForceReply, Update, Bot
from aiohttp import web
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, Updater


load_dotenv(dotenv_path)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
commands = {}


def add_to_commands(command):
    def dec(func):
        commands[command] = func

        def wrapper(*args):
            func(*args)
        return wrapper
    return dec


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


async def telegram_handle(request):
    json = await request.json()
    update = Update.de_json(json, bot)

    await commands.get(update.message.text, commands.get('/default'))(update)
    # await bot.send_message(1021912706, "Пятух")
    return web.Response()


bot = Bot(TOKEN)
app = web.Application()
app.add_routes([web.post(f'/{TOKEN}/', telegram_handle)])


if __name__ == '__main__':
    web.run_app(app)

