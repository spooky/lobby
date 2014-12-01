import logging
from PyQt5.QtCore import QObject, QCoreApplication, pyqtProperty, pyqtSignal, pyqtSlot

from session.GameSession import GameSession


class GamesViewModel(QObject):
    hostGame = pyqtSignal()

    def __init__(self, server_context, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.hostGame.connect(self.on_hostGame)

        self.server_context = server_context
        self.server_context.eventReceived.connect(self.on_eventReceived)

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
        pass  # no value in this...

    def on_updated(self, args):
        g = GameViewModel(args)
        self.log.debug('updating game id: {}'.format(g.id))

    def on_closed(self, args):
        g = GameViewModel(args)
        self.log.debug('closed game id: {}'.format(g.id))


class GameViewModel(QObject):

    def __init__(self, source, parent=None):
        super().__init__(parent)
        self.id = source['id']
        self.map = self.get_map(source)
        self.title = source['Title']
        self.host = source['host']['username']
        self.slots = source['GameOption']['Slots']
        self.players = self.get_player_count(source)
        # TODO
        self.balance = 0.0
        self.featured = None
        self.mods = []

    @staticmethod
    def get_map(source):
        scenario = source['GameOption']['ScenarioFile']
        return scenario.split('/')[2]

    @staticmethod
    def get_player_count(source):
        return len(source['PlayerOption'])
