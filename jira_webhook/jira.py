from aiohttp import web
from models import User
from settings import bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


class Issue:
    __slots__ = (
        'event',
        'fields',
        'changelog',
        'summary',
        'key',
        'initiator_name',
        'creator_name',
        'assignee_name',
    )
    
    def __init__(self,
                 event=None,
                 fields=None,
                 changelog=None,
                 summary=None,
                 key=None,
                 initiator_name=None,
                 creator_name=None,
                 assignee_name=None):
        
        self.event = event
        self.fields = fields
        self.changelog = changelog
        self.summary = summary
        self.key = key
        self.initiator_name = initiator_name
        self.creator_name = creator_name
        self.assignee_name = assignee_name

    @classmethod
    def de_json(cls, json):
        data = dict()

        data['event'] = json['webhookEvent']

        data['fields'] = json['issue']['fields']

        if json.get('changelog'):
            data['changelog'] = json['changelog']['items']

        data['summary'] = data['fields']["summary"]
        data['key'] = json['issue']["key"]

        data['initiator_name'] = json["user"]["name"]
        data['creator_name'] = data['fields']['creator']['name']
        data['assignee_name'] = data['fields']['assignee']['name']
        
        return cls(**data)

    def status_keyboard(self):
        keyboard = [
            [InlineKeyboardButton('Backlog', callback_data=f'{self.key}/11'),
             InlineKeyboardButton('Selected', callback_data=f'{self.key}/21')],
            [InlineKeyboardButton('In progress', callback_data=f'{self.key}/31'),
             InlineKeyboardButton('Done', callback_data=f'{self.key}/41')]
        ]
        return InlineKeyboardMarkup(keyboard)

    def handler(self):
        pass


async def jira_handle(request):
    json = await request.json()
    print(json)
    issue = Issue.de_json(json)

    initiator = User.get_user_by_jira_username(issue.initiator_name)
    initiator_tg_username = initiator.username if initiator else issue.initiator_name

    assignee = User.get_user_by_jira_username(issue.assignee_name)
    creator = User.get_user_by_jira_username(issue.creator_name)

    match issue.event:
        case 'jira:issue_created':
            text = f'Created task ' \
                   f'<a href="http://jira.jestenok.com/browse/{issue.key}">{issue.summary}</a> ' \
                   f'by @{initiator_tg_username}'
        case 'jira:issue_updated':
            fromString = f'from <b>{issue.changelog[-1]["fromString"]}</b>' if issue.changelog[-1]["fromString"] else ''

            text = f"Task's {issue.changelog[-1]['field']} \n" \
                   f'<a href="http://jira.jestenok.com/browse/{issue.key}">{issue.summary}</a> \n' \
                   f'changed {fromString} \n'\
                   f'to <b>{issue.changelog[-1]["toString"]}</b> \n' \
                   f'by @{initiator_tg_username}'
        case _:
            return web.Response()

    await bot.send_message(assignee.id, text, parse_mode='HTML', reply_markup=issue.status_keyboard())
    if assignee != creator:
        await bot.send_message(creator.id, text, parse_mode='HTML', reply_markup=issue.status_keyboard())

    return web.Response()
