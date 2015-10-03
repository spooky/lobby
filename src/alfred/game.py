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


# yyy... ehh...
gameViewModel = GameViewModel()
