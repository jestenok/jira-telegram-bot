from aiohttp import web
from models import User
from settings import bot


async def jira_handle(request):
    json = await request.json()
    print(json)
    issue_fields = json['issue']['fields']
    jira_username = issue_fields['assignee']['name'].lower()

    u = User.get_user_by_jira_username(jira_username)

    task_status = json['changelog']['items'][-1]
    await bot.send_message(u.id,
                           f'Статус задачи '
                           f'<a href="http://jira.jestenok.com/browse/{json["issue"]["key"]}">{issue_fields["summary"]}</a>'
                           f' изменен c {task_status["fromString"]} на {task_status["toString"]}',
                           parse_mode='HTML')

    return web.Response()
