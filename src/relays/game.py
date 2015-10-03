import asyncio


class GameClient(object):

    def __init__(self):
        super().__init__()
        self.server = server_factory()

    def subscribeOnNewGame(self, callback):
        self.server.onNewGame = callback

    @asyncio.coroutine
    def host(self, game):
        result = yield from self.server.requestHost(game)
        return result

    @asyncio.coroutine
    def join(self, game):
        result = yield from self.server.requestJoin(game)
        return result


class GameServer(object):

    @asyncio.coroutine
    def requestHost(self, game):
        future = asyncio.Future()
        future.set_result(True)
        return future

    @asyncio.coroutine
    def requestJoin(self, game):
        future = asyncio.Future()
        future.set_result(True)
        return future

    def onNewGame(self, game):
        pass

    def newGame(self, game):
        self.onNewGame(game)


def server_factory():
    # return GameServer()
    import alfred.game
    return alfred.game.gameViewModel
