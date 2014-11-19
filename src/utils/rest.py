import asyncio
import aiohttp


class ServerError(Exception):
    pass


@asyncio.coroutine
def request(*args, **kwargs):
    response = yield from aiohttp.request(*args, **kwargs)
    if not response.status < 400:
        error = None
        try:
            error = yield from response.json()
        except ValueError:
            error = yield from response.text()

        raise ServerError(error)

    return (yield from response.json())


@asyncio.coroutine
def get(url, *args, **kwargs):
    return request('GET', url, *args, **kwargs)


@asyncio.coroutine
def post(url, *args, **kwargs):
    headers = {'content-type': 'application/json'}
    return request('POST', url, headers=headers, *args, **kwargs)
