from aiohttp import web


async def health_handle(_):
    return web.StreamResponse(status=200)
