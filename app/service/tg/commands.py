from storage.models import User
from settings import JIRA_AUTH_LINK
from telegram import Update
from telegram import ForceReply


async def process_commands(update: Update):
    match update.message.text.lower():
        case '/start':
            await jira_account(update)
        case '/jira':
            await jira_account(update)
        case _:
            await command_not_found(update)


async def start(update) -> None:
    u = User.get_user_from_update(update)

    await update.message.reply_html(
        rf"Hi {u}!",
        reply_markup=ForceReply(selective=True),
    )


async def jira_account(update) -> None:
    jira_auth = f'Необходимо перейти по ' \
                f'<a href="{JIRA_AUTH_LINK}">ссылке</a>, ' \
                f'создать токен доступа (без ограничения по времени) и прислать ответом на сообщение'

    await update.message.reply_html(jira_auth,
                                    reply_markup=ForceReply(selective=True))


async def command_not_found(update):
    await update.message.reply_text("Команда не найдена")
