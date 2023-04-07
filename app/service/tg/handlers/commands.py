from storage.models import User
from settings import JIRA_AUTH_LINK
from telegram import ForceReply
from telegram import Update


async def start(update: Update, _) -> None:
    u = User.get_user_from_update(update)
    await update.message.reply_html(rf"Hi {u}!")
    await jira(update, _)


async def jira(update: Update, _) -> None:
    jira_auth = f'Необходимо перейти по ' \
                f'<a href="{JIRA_AUTH_LINK}">ссылке</a>, ' \
                f'создать токен доступа (без ограничения по времени) и прислать ответом на сообщение'

    await update.message.reply_html(jira_auth,
                                    reply_markup=ForceReply(selective=True))


async def not_found(update: Update, _) -> None:
    await update.message.reply_text("Команда не найдена")
