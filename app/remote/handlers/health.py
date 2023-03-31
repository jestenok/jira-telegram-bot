from aiohttp import web


async def health_handle(request):
    return web.StreamResponse(status=200)
