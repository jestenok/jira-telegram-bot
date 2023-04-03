from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from settings import bot


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
                 fields=None,
                 changelog=None,
                 summary=None,
                 key=None):
        self.fields = fields
        self.changelog = changelog
        self.summary = summary
        self.key = key

    @classmethod
    def de_json(cls, json):
        data = dict()

        data['fields'] = json['issue']['fields']

        if json.get('changelog'):
            data['changelog'] = json['changelog']['items']

        data['summary'] = data['fields']["summary"]
        data['key'] = json['issue']["key"]

        return cls(**data)

    def process_event(self,
                      event: str,
                      initiator: str,
                      assignee: str,
                      creator: str):
        match event:
            case 'jira:issue_created':
                text = f'Created task ' \
                       f'<a href="http://jira.jestenok.com/browse/{self.key}">{self.summary}</a> ' \
                       f'by @{initiator}'

            case 'jira:issue_updated':
                from_string = ''
                if self.changelog[-1]["fromString"]:
                    from_string = f'from <b>{self.changelog[-1]["fromString"]}</b>'

                text = f"Task's {self.changelog[-1]['field']} \n" \
                       f'<a href="http://jira.jestenok.com/browse/{self.key}">{self.summary}</a> \n' \
                       f'changed {from_string} \n' \
                       f'to <b>{self.changelog[-1]["toString"]}</b> \n' \
                       f'by @{initiator}'
            case _:
                return

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('Backlog', callback_data=f'{self.key}/11'),
             InlineKeyboardButton('Selected', callback_data=f'{self.key}/21')],
            [InlineKeyboardButton('In progress', callback_data=f'{self.key}/31'),
             InlineKeyboardButton('Done', callback_data=f'{self.key}/41')]
        ])

        await bot.send_message(assignee, text, parse_mode='HTML', reply_markup=keyboard)
        if assignee != creator:
            await bot.send_message(creator, text, parse_mode='HTML', reply_markup=keyboard)
