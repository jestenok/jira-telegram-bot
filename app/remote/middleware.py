import logging
from aiohttp.web import middleware
import json


@middleware
async def log_middleware(request, handler):
    data = await request.json()

    j = json.dumps(data, indent=4, sort_keys=True)

    info = f'''method: {request.method}, url: {request.url}, json: {j}'''

    logging.info(info)

    response = await handler(request)
    return response
