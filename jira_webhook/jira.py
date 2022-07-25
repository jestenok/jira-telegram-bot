from aiohttp import web
from models import User
from settings import bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


class Issue:
    def __init__(self, json):
        self.event = json['webhookEvent']

        self.fields = json['issue']['fields']

        if json.get('changelog'):
            self.changelog = json['changelog']['items']

        self.summary = self.fields["summary"]
        self.key = json['issue']["key"]

        self.initiator_name = json["user"]["name"]
        self.creator_name = self.fields['creator']['name']
        self.assignee_name = self.fields['assignee']['name']

    # def initiator_tg_user(self):
    #     return User.get_user_by_jira_username(self.initiator_name)


async def jira_handle(request):
    json = await request.json()
    print(json)
    issue = Issue(json)

    initiator = User.get_user_by_jira_username(issue.initiator_name)
    initiator_username = initiator.username if initiator else issue.initiator_name

    assignee = User.get_user_by_jira_username(issue.assignee_name)
    creator = User.get_user_by_jira_username(issue.creator_name)

    match issue.event:
        case 'jira:issue_created':
            text = f'Создана задача ' \
                   f'<a href="http://jira.jestenok.com/browse/{issue.key}">{issue.summary}</a> ' \
                   f'пользователем @{initiator_username}'
        case 'jira:issue_updated':
            text = f'Статус задачи ' \
                   f'<a href="http://jira.jestenok.com/browse/{issue.key}">{issue.summary}</a> ' \
                   f'изменен{issue.changelog[-1]["fromString"]} на {issue.changelog[-1]["toString"]} ' \
                   f'пользователем @{initiator_username}'
        case _:
            return web.Response()

    keyboard = [
        [InlineKeyboardButton('Backlog',     callback_data=f'{issue.key}/11'),
         InlineKeyboardButton('Selected',    callback_data=f'{issue.key}/21')],
        [InlineKeyboardButton('In progress', callback_data=f'{issue.key}/31'),
         InlineKeyboardButton('Done',        callback_data=f'{issue.key}/41')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_message(assignee.id, text, parse_mode='HTML', reply_markup=reply_markup)
    if assignee != creator:
        await bot.send_message(creator.id, text, parse_mode='HTML', reply_markup=reply_markup)

    return web.Response()
