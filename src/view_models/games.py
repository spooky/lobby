import logging
from itertools import groupby
from PyQt5.QtCore import QVariant, QUrl, QCoreApplication, pyqtSignal, pyqtSlot

from models import Map, Mod
from session.GameSession import GameSession
from widgets import Application
from .adapters import ListModelFor, SelectionList, NotifyablePropertyObject, notifyableProperty


class GameViewModel(NotifyablePropertyObject):

    ''' View model for game tile '''

    id = notifyableProperty(int)
    map_preview_small = notifyableProperty(QUrl)
    map_preview_big = notifyableProperty(QUrl)
    map_name = notifyableProperty(str)
    title = notifyableProperty(str)
    host = notifyableProperty(str)
    featured_mod = notifyableProperty(str)
    mods = notifyableProperty(QVariant)
    slots = notifyableProperty(int)
    player_count = notifyableProperty(int)
    teams_arrangement = notifyableProperty(QVariant)
    balance = notifyableProperty(int)

    def __init__(self, source=None, map_lookup=None, mod_lookup=None, parent=None):
        super().__init__(parent)
        self._map_lookup = map_lookup or {}
        self._mod_lookup = mod_lookup or {}

        if not source:
            return

        self.id = source.get('id')
        game_map = self.get_map(source)
        self.map_preview_small = QUrl(game_map.preview_small)
        self.map_preview_big = QUrl(game_map.preview_big)
        self.map_name = game_map.name
        self.title = source.get('Title')
        self.host = source['host'].get('username') if 'host' in source.keys() else None
        self.featured_mod, self._mods = self.get_mods(source.get('GameMods') or [])
        self.slots = source['GameOption'].get('Slots', 0) if 'GameOption' in source.keys() else 0
        self.player_count = len(source.get('PlayerOption') or [])
        self.teams_arrangement = self.get_teams_arrangement(source)
        self.balance = 0

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_map(self, source):
        try:
            scenario = source['GameOption']['ScenarioFile']
            return self._map_lookup[scenario.split('/')[2]]
        except KeyError:
            return Map()

    def get_mods(self, mods):
        names = []
        for m in mods:
            try:
                names.append(self._mod_lookup[m].name)
            except KeyError:
                names.append(QCoreApplication.translate('GamesViewModel', 'unknown'))

        return ('featured (todo)', sorted(names))  # (featured, other)

    @staticmethod
    def get_teams_arrangement(source):
        if 'PlayerOption' not in source.keys():
            return []

        teams = []
        players = source['PlayerOption']
        for gkey, group in groupby(sorted(players.items(), key=lambda x: str(x[1]['Team']) + x[0]), key=lambda x: x[1]['Team']):
            team = []
            for k, v in group:
                team.append({'name': v['PlayerName'], 'skill': v.get('MEAN'), 'cc': v['Country']})
            teams.append(team)

        return teams


class GameListModel(ListModelFor(GameViewModel)):

    ''' View model for a list of games '''

    def update(self, item):
        index = self._items.index(item)
        super().update(index, item)


class GamesViewModel(NotifyablePropertyObject):

    ''' Main view model for games screen '''

    games = notifyableProperty(GameListModel)
    presets = notifyableProperty(SelectionList)
    title = notifyableProperty(str)
    private = notifyableProperty(bool)
    featured = notifyableProperty(SelectionList)
    maps = notifyableProperty(SelectionList)
    mods = notifyableProperty(SelectionList)

    savePreset = pyqtSignal()
    hostGame = pyqtSignal()
    joinGame = pyqtSignal(int)

    def __init__(self, server_context, map_lookup, mod_lookup, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.savePreset.connect(self.on_savePreset)
        self.hostGame.connect(self.on_hostGame)
        self.joinGame.connect(self.on_joinGame)

        self.server_context = server_context
        self.server_context.eventReceived.connect(self.on_eventReceived)

        self.map_lookup = map_lookup
        self.mod_lookup = mod_lookup

        self.games = GameListModel()

        self.presets = SelectionList()  # TODO
        self.title = None
        self.private = False
        self.featured = SelectionList()
        self.maps = SelectionList()
        self.mods = SelectionList(multiple=True)

        Application.instance().init_complete.connect(self.on_app_init_complete)

        # test data
        self.featured.append(Mod('uid-faf', 'Forged Alliance Forever'), selected=True)
        self.featured.append(Mod('uid-vanilla', 'Vanilla'))
        self.featured.append(Mod('uid-phantom', 'Phantom X'))
        self.featured.append(Mod('uid-nomads', 'The Nomads'))

    def on_app_init_complete(self):
        for m in sorted(self.map_lookup.values(), key=lambda m: m.name.lower()):
            self.maps.append(m)

        for m in sorted(self.mod_lookup.values(), key=lambda m: m.name.lower()):
            if not m.ui_only:
                self.mods.append(m)

    @pyqtSlot()
    def on_savePreset(self):
        self.log.debug('TODO: save preset')

    @pyqtSlot()
    def on_hostGame(self):
        self.log.debug('hosting with options: {}, {}, {}, {}, mods: {}'.format(
            self.title,
            'locked' if self.private else 'open',
            self.featured.getSelected(),
            self.maps.getSelected(),
            [m.uid for m in self.mods.getSelected()]))

        Application.instance().report_indefinite(QCoreApplication.translate('GamesViewModel', 'hosting game'))
        session = QCoreApplication.instance().session
        if not session:
            # TODO: display 'not logged in' error
            return None
        game = GameSession(QCoreApplication.instance())
        game.setFAFConnection(self.server_context)
        game.finished.connect(lambda: Application.instance().end_report())

        game.addArg('showlog')
        game.addArg('mean', 1000)
        game.addArg('deviation', 0)
        game.addArg('windowed', 1024, 768)
        game.addArg('init', 'init_test.lua')

        game.setTitle(self.title)
        game.setMap(self.maps.getSelected().code)
        game.setLocalPlayer(session.user, session.user_id)

        game.start()

    @pyqtSlot(int)
    def on_joinGame(self, id):
        self.log.debug('joining: {}'.format(id))
        Application.instance().report_indefinite(QCoreApplication.translate('GamesViewModel', 'joining game'))

    @pyqtSlot(list, dict)
    def on_eventReceived(self, event_id, args):
        subs, cmd = event_id
        if subs != 'games':
            return

        getattr(self, 'on_'+cmd)(args)

    def on_opened(self, args):
        g = GameViewModel(args, self.map_lookup, self.mod_lookup)
        self.games.append(g)
        self.log.debug('added game id: {}'.format(g.id))

    def on_updated(self, args):
        g = GameViewModel(args, self.map_lookup, self.mod_lookup)
        self.games.update(g)
        self.log.debug('updated game id: {}'.format(g.id))

    def on_closed(self, args):
        g = GameViewModel(args, self.map_lookup, self.mod_lookup)
        self.games.remove(g)
        self.log.debug('closed game id: {}'.format(g.id))
