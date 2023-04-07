import logging
from aiohttp.web import middleware
import json


@middleware
async def log_middleware(request, handler):
    data = await request.json()
    j = json.dumps(data)
    info = f'''method: {request.method}, url: {request.url}, json: {j}'''

    logging.info(info)

    response = await handler(request)
    return response


def setup_middlewares(app):
    app.middlewares.append(log_middleware)
