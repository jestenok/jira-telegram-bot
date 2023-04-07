from telegram import Update
from settings import JIRA_AUTH_LINK
from storage.models import User


async def reply(update: Update, context=None):
    if len(update.message.reply_to_message.entities) == 0:
        return

    if update.message.reply_to_message.entities[0]['url'] == JIRA_AUTH_LINK:
        await process_jira_token(update, context)


async def process_jira_token(update: Update, _) -> None:
    u = User.get_user_from_update(update)

    if len(update.message.text) <= 15:
        await update.message.reply_text("Не название, а сам токен")
    elif not u.jira_session(update.message.text):
        await update.message.reply_text("Неверный токен доступа")
    else:
        await update.message.reply_text("Аккаунт jira успешно привязан")