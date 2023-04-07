from telegram import Update

from storage.models import User
from settings import JIRA_AUTH_LINK


def callback_query(update: Update, _):
    u = User.get_user_from_update(update)

    issue_id, status_id = update.callback_query.data.split('/')

    jira = u.jira_session()
    jira.transition_issue(issue_id, status_id)


async def reply_to_message(update: Update, context=None):
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


async def text_message(update: Update, _) -> None:
    await update.message.reply_text("Не понимаю, что ты от меня хочешь")


async def photo_message(update: Update, _) -> None:
    await update.message.reply_text("Иди в пизду со своими фотокарточками")



