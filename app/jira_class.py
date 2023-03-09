from telegram import InlineKeyboardButton, InlineKeyboardMarkup


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

