from telegram import ForceReply, Update
from models import User
from settings import JIRA_AUTH_LINK


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


async def reply_to_message(update):
    u = User.get_user_from_update(update)

    if len(update.message.reply_to_message.entities) == 0:
        return

    if update.message.reply_to_message.entities[0]['url'] == JIRA_AUTH_LINK:
        if len(update.message.text) <= 15:
            await update.message.reply_text("Не название, а сам токен")
        elif not u.jira_session(update.message.text):
            await update.message.reply_text("Неверный токен доступа")
        else:
            await update.message.reply_text("Аккаунт jira успешно привязан")
