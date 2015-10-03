import logging
import json

from PyQt5.QtCore import pyqtSignal, pyqtSlot

from relays.game import GameServer
from games.models import Game
from view_models.adapters import NotifyablePropertyObject, notifyableProperty
from .factories import gameFactory


class GameViewModel(GameServer, NotifyablePropertyObject):
    gameJson = notifyableProperty(str)

    create = pyqtSignal(str)
    generate = pyqtSignal()

    def __init__(self, client=None, server=None, parent=None):
        NotifyablePropertyObject.__init__(self, parent)

        self.log = logging.getLogger(__name__)
        self.generateGame = gameFactory()

        self.create.connect(self.onCreate)
        self.generate.connect(self.onGenerate)

        self.__games = 0

    @pyqtSlot(str)
    def onCreate(self, gameJson):
        if not gameJson:
            return

        g = json.loads(gameJson)
        try:
            newGame = Game(**g)
            self.newGame(newGame)
        except:
            self.log.error('invalid game json')

    @pyqtSlot()
    def onGenerate(self):
        game = self.generateGame()
        self.gameJson = json.dumps(game.__dict__)
        self.newGame(game)

    def __generateGameId(self):
        self.__games += 1
        return self.__games

    def processGame(self, game):
        game.id = game.id or self.__generateGameId()
        game.host = game.host or 'that guy'
        game.players = game.players or 1
        game.teams = game.teams or [[{'name': game.host, 'cc': 'pl', 'skill': 1000}]]
        game.balance = game.balance or 70


# yyy... ehh...
gameViewModel = GameViewModel()
