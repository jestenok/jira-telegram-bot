from telegram import Update
from storage.models import User


def callback_query(update: Update, _):
    u = User.get_user_from_update(update)

    issue_id, status_id = update.callback_query.data.split('/')

    jira = u.jira_session()
    jira.transition_issue(issue_id, status_id)
