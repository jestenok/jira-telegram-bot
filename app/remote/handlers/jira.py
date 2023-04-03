from service.jira.jira import Issue
from aiohttp import web
from storage.models import User


async def jira_handle(request):
    json = await request.json()
    issue = Issue.de_json(json)

    initiator = User.get_by_jira_username(json["user"]["name"])
    initiator_tg = initiator.username if initiator else json["user"]["name"]

    assignee = User.get_by_jira_username(json['fields']['assignee']['name'])
    creator = User.get_by_jira_username(json['fields']['creator']['name'])

    issue.process_event(json['webhookEvent'],
                        initiator_tg,
                        assignee.id,
                        creator.id)

    return web.Response()
