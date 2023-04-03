from jira_class import Issue
from aiohttp import web
from models import User
from settings import bot


async def jira_handle(request):
    json = await request.json()
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
            from_string = f'from <b>{issue.changelog[-1]["fromString"]}</b>' if issue.changelog[-1]["fromString"] else ''

            text = f"Task's {issue.changelog[-1]['field']} \n" \
                   f'<a href="http://jira.jestenok.com/browse/{issue.key}">{issue.summary}</a> \n' \
                   f'changed {from_string} \n'\
                   f'to <b>{issue.changelog[-1]["toString"]}</b> \n' \
                   f'by @{initiator_tg_username}'
        case _:
            return web.Response()

    await bot.send_message(assignee.id, text, parse_mode='HTML', reply_markup=issue.status_keyboard())
    if assignee != creator:
        await bot.send_message(creator.id, text, parse_mode='HTML', reply_markup=issue.status_keyboard())

    return web.Response()
