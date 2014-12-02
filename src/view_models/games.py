import logging
from PyQt5.QtCore import QObject, QCoreApplication, pyqtProperty, pyqtSignal, pyqtSlot

from session.GameSession import GameSession
from .adapters import ListModelFor


class GameViewModel(QObject):

    def __init__(self, source=None, parent=None):
        super().__init__(parent)
        if not source:
            return

        self._id = source.get('id')
        self._map = self.get_map(source)
        self._title = source.get('Title')
        self._host = source['host'].get('username') if 'host' in source.keys() else None
        self._slots = source['GameOption'].get('Slots', 0) if 'GameOption' in source.keys() else 0
        self._players = self.get_player_count(source)
        self._balance = 0
        # TODO
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

    id_changed = pyqtSignal(int)

    @pyqtProperty(int, notify=id_changed)
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        self.id_changed.emit(value)

    map_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=map_changed)
    def map(self):
        return self._map

    @map.setter
    def map(self, value):
        self._map = value
        self.map_changed.emit(value)

    title_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=title_changed)
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_changed.emit(value)

    host_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=host_changed)
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value
        self.host_changed.emit(value)

    slots_changed = pyqtSignal(int)

    @pyqtProperty(int, notify=slots_changed)
    def slots(self):
        return self._slots

    @slots.setter
    def slots(self, value):
        self._slots = value
        self.slots_changed.emit(value)

    players_changed = pyqtSignal(int)

    @pyqtProperty(int, notify=players_changed)
    def players(self):
        return self._players

    @players.setter
    def players(self, value):
        self._players = value
        self.players_changed.emit(value)

    balance_changed = pyqtSignal(int)

    @pyqtProperty(int, notify=balance_changed)
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value
        self.balance_changed.emit(value)


class GameListModel(ListModelFor(GameViewModel)):

    def update(self, item):
        index = self._items.index(item)
        super().update(index, item)


class GamesViewModel(QObject):
    hostGame = pyqtSignal()
    joinGame = pyqtSignal(int)

    def __init__(self, server_context, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.hostGame.connect(self.on_hostGame)
        self.joinGame.connect(self.on_joinGame)

        self.server_context = server_context
        self.server_context.eventReceived.connect(self.on_eventReceived)

        self._games = GameListModel()

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

    @pyqtSlot(GameViewModel)
    def on_joinGame(self, id):
        self.log.debug('joining: {}'.format(id))

    @pyqtSlot(list, dict)
    def on_eventReceived(self, event_id, args):
        subs, cmd = event_id
        if subs != 'games':
            return

        getattr(self, 'on_'+cmd)(args)

    def on_opened(self, args):
        g = GameViewModel(args)
        self.games.append(g)
        self.log.debug('added game id: {}'.format(g.id))

    def on_updated(self, args):
        g = GameViewModel(args)
        self.games.update(g)
        self.log.debug('updated game id: {}'.format(g.id))

    def on_closed(self, args):
        g = GameViewModel(args)
        self.games.remove(g)
        self.log.debug('closed game id: {}'.format(g.id))
