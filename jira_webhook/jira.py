from aiohttp import web
from models import User
from settings import bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


async def jira_handle(request):
    json = await request.json()
    print(json)
    issue = json['issue']

    jira_username = issue['fields']['assignee']['name'].lower()

    u = User.get_user_by_jira_username(jira_username)

    initiator = User.get_user_by_jira_username(json["user"]["name"])

    match json['webhookEvent']:
        case 'jira:issue_created':
            text = f'Создана задача ' \
                   f'<a href="http://jira.jestenok.com/browse/{issue["key"]}">{issue["fields"]["summary"]}</a> ' \
                   f'пользователем @{initiator.username}'
        case 'jira:issue_updated':
            task_changelog = json['changelog']['items'][-1]
            fromString = f' c {task_changelog["fromString"]}' if task_changelog["fromString"] else ''
            text = f'Статус задачи ' \
                   f'<a href="http://jira.jestenok.com/browse/{issue["key"]}">{issue["fields"]["summary"]}</a> ' \
                   f'изменен{fromString} на {task_changelog["toString"]} ' \
                   f'пользователем @{initiator.username}'
        case _:
            return web.Response()

    keyboard = [
        [InlineKeyboardButton('Backlog',     callback_data=f'{issue["key"]}/11'),
         InlineKeyboardButton('Selected',    callback_data=f'{issue["key"]}/21')],
        [InlineKeyboardButton('In progress', callback_data=f'{issue["key"]}/31'),
         InlineKeyboardButton('Done',        callback_data=f'{issue["key"]}/41')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_message(u.id, text, parse_mode='HTML', reply_markup=reply_markup)
    return web.Response()
