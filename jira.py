from aiohttp import web


async def jira_handle(request):
    json = await request.json()

    print(json)
    return web.Response()
