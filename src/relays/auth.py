import asyncio


class AuthClient(object):

    def __init__(self):
        super().__init__()
        self.server = server_factory()

    @asyncio.coroutine
    def login(self, user, password):
        result = yield from self.server.request_login(user, password)
        return result

    @asyncio.coroutine
    def logout(self, user):
        result = yield from self.server.request_logout(user)
        return result


class AuthServer(object):

    @asyncio.coroutine
    def request_login(self, user, password):
        future = asyncio.Future()
        future.set_result(True)
        return future

    @asyncio.coroutine
    def request_logout(self, user):
        future = asyncio.Future()
        future.set_result(True)
        return future


def server_factory():
    # return AuthServer()
    import alfred.auth
    return alfred.auth.authViewModel
