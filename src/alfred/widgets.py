import logging

from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtQml import QQmlApplicationEngine

from relays import *
from .auth import authViewModel
from .game import gameViewModel


# ################################## TODO ################################### #
#                                                                             #
# TODO: featured mods                                                         #
# TODO: mods                                                                  #
# TODO: maps                                                                  #
# TODO: logging console                                                       #
#                                                                             #
# ########################################################################### #


class MainWindow(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.engine = QQmlApplicationEngine(self)
        self.engine.quit.connect(parent.quit)

        self.engine.rootContext().setContextProperty('auth', authViewModel)
        self.engine.rootContext().setContextProperty('game', gameViewModel)

        self.engine.load(QUrl.fromLocalFile('alfred/views/MainWindow.qml'))

        self.window = self.engine.rootObjects()[0]

    def show(self):
        self.window.show()
        self.log.debug('alfred up')
