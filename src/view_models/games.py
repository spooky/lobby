import logging
from PyQt5.QtCore import Qt, QObject, QCoreApplication, QAbstractListModel, QModelIndex, pyqtProperty, pyqtSignal, pyqtSlot

from session.GameSession import GameSession


class GameViewModel(QObject):

    def __init__(self, source, parent=None):
        super().__init__(parent)
        self.id = source.get('id')
        self.map = self.get_map(source)
        self.title = source.get('Title')
        self.host = source['host'].get('username') if 'host' in source.keys() else None
        self.slots = source['GameOption'].get('Slots') if 'GameOption' in source.keys() else None
        self.players = self.get_player_count(source)
        # TODO
        self.balance = 0.0
        self.featured = None
        self.mods = []

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def get_map(source):
        try:
            scenario = source['GameOption']['ScenarioFile']
            return scenario.split('/')[2]
        except KeyError:
            return None

    @staticmethod
    def get_player_count(source):
        return len(source['PlayerOption']) if 'PlayerOption' in source.keys() else 0


class GameListModel(QAbstractListModel):  # QStandardItemModel?

    def __init__(self):
        super().__init__()
        self._items = list()

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            return self._items[index.row()]

        return None

    def insert_or_update(self, game):
        try:
            idx = self._items.index(game)  # searches by id
            self._items[idx] = game
            self.dataChanged.emit(self.index(idx), self.index(idx))
        except ValueError:
            count = self.rowCount()
            self.beginInsertRows(self.index(count), count, count)
            self._items.append(game)
            self.endInsertRows()

    def remove(self, game):
        count = self.rowCount()
        try:
            self.beginRemoveRows(self.index(count), count, count)
            self._items.remove(game)
            self.endRemoveRows()
        except ValueError:
            pass


class GamesViewModel(QObject):
    hostGame = pyqtSignal()

    def __init__(self, server_context, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.hostGame.connect(self.on_hostGame)

        self.server_context = server_context
        self.server_context.eventReceived.connect(self.on_eventReceived)

        self._games = GameListModel()
        self._games.insert_or_update(GameViewModel(dict(id=1, title='foo', players=99)))
        self._games.insert_or_update(GameViewModel(dict(id=2, title='bar', players=66)))

    games_changed = pyqtSignal(GameListModel)

    @pyqtProperty(GameListModel, notify=games_changed)
    def games(self):
        return self._games

    @games.setter
    def games(self, value):
        self._games = value
        self.games_changed.emit(value)

    @pyqtSlot()
    def on_hostGame(self):
        # TODO: report activity in status bar
        session = QCoreApplication.instance().session
        if not session:
            # TODO: display 'not logged' error
            return None
        game = GameSession(QCoreApplication.instance())
        game.setFAFConnection(self.server_context)

        game.addArg('showlog')
        game.addArg('mean', 1000)
        game.addArg('deviation', 0)
        game.addArg('windowed', 1024, 768)
        game.addArg('init', 'init_test.lua')

        game.setTitle('test')
        game.setMap('scmp_009')
        game.setLocalPlayer(session.user, session.user_id)

        game.start()

    @pyqtSlot(list, dict)
    def on_eventReceived(self, event_id, args):
        subs, cmd = event_id
        if subs != 'games':
            return

        getattr(self, 'on_'+cmd)(args)

    def on_opened(self, args):
        g = GameViewModel(args)
        self.games.insert_or_update(g)
        self.log.debug('added game id: {}'.format(g.id))

    def on_updated(self, args):
        g = GameViewModel(args)
        self.games.insert_or_update(g)
        self.log.debug('updated game id: {}'.format(g.id))

    def on_closed(self, args):
        g = GameViewModel(args)
        self.games.remove(g)
        self.log.debug('closed game id: {}'.format(g.id))
