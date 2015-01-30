import functools
import asyncio


def async_slot(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.async(f(*args, **kwargs))

    return wrapper
