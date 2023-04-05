import logging
from aiohttp.web import middleware


@middleware
async def log_middleware(request, handler):
    data = await request.json()

    info = f'''{request.method}: {request.url} json: {data}'''

    logging.info(info)

    response = await handler(request)
    return response
