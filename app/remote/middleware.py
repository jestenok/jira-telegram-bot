import json
from aiohttp.web import middleware


@middleware
async def log_middleware(request, handler):
    data = await request.json()

    print('-' * 30)
    print(request.url)
    print(json.dumps(data, indent=4))
    print()

    response = await handler(request)
    return response
