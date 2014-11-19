import functools
import asyncio


def async_slot(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        asyncio.async(f(*args, **kwargs))

    return wrapper
