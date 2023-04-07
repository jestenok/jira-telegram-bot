from storage.models import User
from settings import JIRA_AUTH_LINK
from telegram import ForceReply


async def start(update, _) -> None:
    u = User.get_user_from_update(update)
    await update.message.reply_html(rf"Hi {u}!")
    await jira(update, _)


async def jira(update, _) -> None:
    jira_auth = f'Необходимо перейти по ' \
                f'<a href="{JIRA_AUTH_LINK}">ссылке</a>, ' \
                f'создать токен доступа (без ограничения по времени) и прислать ответом на сообщение'

    await update.message.reply_html(jira_auth,
                                    reply_markup=ForceReply(selective=True))


async def not_found(update, _) -> None:
    await update.message.reply_text("Команда не найдена")
