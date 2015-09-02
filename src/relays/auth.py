import asyncio
from models import Session


class AuthServer(object):

    def __init__(self):
        super().__init__()
        self._session = 0

    def _user_id(self, user):
        if not user:
            return None

        import hashlib
        return hashlib.sha1(user.encode()).hexdigest()

    def _session_id(self):
        id = self._session
        self._session += 1
        return id

    @asyncio.coroutine
    def login(self, user, password, success=None):
        # Session(user, self._user_id(user), '{}@example.org'.format(user), self._session_id() if success else None)
        future = asyncio.Future()
        future.set_result(success is True)
        return future

    @asyncio.coroutine
    def logout(self, user, success=None):
        future = asyncio.Future()
        future.set_result(success is True)
        return future


class AuthMediator(object):

    def __init__(self):
        self.client = None
        self.server = None

    @asyncio.coroutine
    def login(self, user, password):
        return (yield from self.server.login(user, password, success=True))

    @asyncio.coroutine
    def logout(self, user):
        return (yield from self.server.logout(user, success=True))


class AuthClient(object):

    def __init__(self, mediator):
        self.mediator = mediator

    @asyncio.coroutine
    def login(self, user, password):
        return (yield from self.mediator.login(user, password))

    @asyncio.coroutine
    def logout(self, user):
        return (yield from self.mediator.logout(user))


def create_auth_client():
    # mediator = AuthMediator()
    import alfred.auth
    mediator = alfred.auth.auth_view_model
    mediator.server = AuthServer()
    mediator.client = AuthClient(mediator)

    return mediator.client
