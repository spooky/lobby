import logging

from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtQml import QQmlApplicationEngine


# ################################## TODO ################################### #
#                                                                             #
# TODO: featured mods                                                         #
# TODO: maps                                                                  #
# TODO: mods                                                                  #
# TODO: login, logout                                                         #
# TODO: host game, join game                                                  #
# TODO: logging console                                                       #
#                                                                             #
# ########################################################################### #


class MainWindow(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.engine = QQmlApplicationEngine(self)
        self.engine.quit.connect(parent.quit)
        self.engine.load(QUrl.fromLocalFile('alfred/views/MainWindow.qml'))

        self.window = self.engine.rootObjects()[0]

    def show(self):
        self.window.show()
        self.log.debug('Alfred up')
