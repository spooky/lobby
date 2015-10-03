import asyncio


class GameClient(object):

    def __init__(self):
        super().__init__()
        self.server = server_factory()

    def subscribeForNewGame(self, callback):
        self.server.newGame = callback

    def subscribeForGameUpdate(self, callback):
        self.server.updateGame = callback

    @asyncio.coroutine
    def host(self, game):
        result = yield from self.server.requestHost(game)
        return result

    @asyncio.coroutine
    def join(self, id):
        result = yield from self.server.requestJoin(id)
        return result


class GameServer(object):

    @asyncio.coroutine
    def requestHost(self, game):
        future = asyncio.Future()
        future.set_result(True)

        self.processGame(game)
        self.newGame(game)

        return future

    @asyncio.coroutine
    def requestJoin(self, id):
        future = asyncio.Future()
        future.set_result(True)

        # TODO: this should 'fetch' a game by id, update it's status (teams), then call
        # self.updateGame(updatedGame)

        return future

    def newGame(self, game):
        ''' A callback hook for the client to get notified about a new game '''
        pass

    def updateGame(self, game):
        ''' A callback hook for the client to get notified about a game state change '''
        pass

    def processGame(self, game):
        ''' Verify if all game params are correct and calculate the ones that client can't '''
        pass


def server_factory():
    # return GameServer()
    import alfred.game
    return alfred.game.gameViewModel
