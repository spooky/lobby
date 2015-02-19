import logging
from itertools import groupby
from PyQt5.QtCore import QObject, QVariant, QUrl, QCoreApplication, pyqtProperty, pyqtSignal, pyqtSlot

from models import Map
from session.GameSession import GameSession
from widgets import Application
from .adapters import ListModelFor


class GameViewModel(QObject):

    def __init__(self, source=None, map_lookup={}, mod_lookup={}, parent=None):
        super().__init__(parent)
        self._map_lookup = map_lookup
        self._mod_lookup = mod_lookup

        if not source:
            return

        self._id = source.get('id')
        game_map = self.get_map(source)
        self._map_preview_small = QUrl(game_map.preview_small)
        self._map_preview_big = QUrl(game_map.preview_big)
        self._map_name = game_map.name
        self._title = source.get('Title')
        self._host = source['host'].get('username') if 'host' in source.keys() else None
        self._featured_mod, self._mods = self.get_mods(source.get('GameMods') or [])
        self._slots = source['GameOption'].get('Slots', 0) if 'GameOption' in source.keys() else 0
        self._player_count = len(source.get('PlayerOption') or [])
        self._teams_arrangement = self.get_teams_arrangement(source)
        self._balance = 0

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

    id_changed = pyqtSignal(int)

    @pyqtProperty(int, notify=id_changed)
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        self.id_changed.emit(value)

    map_preview_small_changed = pyqtSignal(QUrl)

    @pyqtProperty(QUrl, notify=map_preview_small_changed)
    def map_preview_small(self):
        return self._map_preview_small

    @map_preview_small.setter
    def map_preview_small(self, value):
        self._map_preview_small = value
        self.map_preview_small_changed.emit(value)

    map_preview_big_changed = pyqtSignal(QUrl)

    @pyqtProperty(QUrl, notify=map_preview_big_changed)
    def map_preview_big(self):
        return self._map_preview_big

    @map_preview_big.setter
    def map_preview_big(self, value):
        self._map_preview_big = value
        self.map_preview_big_changed.emit(value)

    map_name_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=map_name_changed)
    def map_name(self):
        return self._map_name

    @map_name.setter
    def map_name(self, value):
        self._map_name = value
        self.map_name_changed.emit(value)

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

    featured_mod_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=featured_mod_changed)
    def featured_mod(self):
        return self._featured_mod

    @featured_mod.setter
    def featured_mod(self, value):
        self._featured_mod = value
        self.featured_mod_changed.emit(value)

    mods_changed = pyqtSignal(QVariant)

    @pyqtProperty(QVariant, notify=mods_changed)
    def mods(self):
        return self._mods

    @mods.setter
    def mods(self, value):
        self._mods = value
        self.mods_changed.emit(value)

    slots_changed = pyqtSignal(int)

    @pyqtProperty(int, notify=slots_changed)
    def slots(self):
        return self._slots

    @slots.setter
    def slots(self, value):
        self._slots = value
        self.slots_changed.emit(value)

    player_count_changed = pyqtSignal(int)

    @pyqtProperty(int, notify=player_count_changed)
    def player_count(self):
        return self._player_count

    @player_count.setter
    def player_count(self, value):
        self._player_count = value
        self.player_count_changed.emit(value)

    teams_arrangement_changed = pyqtSignal(QVariant)

    @pyqtProperty(QVariant, notify=teams_arrangement_changed)
    def teams_arrangement(self):
        return self._teams_arrangement

    @teams_arrangement.setter
    def teams_arrangement(self, value):
        self._teams_arrangement = value
        self.teams_arrangement_changed.emit(value)

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


class ModSelectionViewModel(QObject):

    def __init__(self, name='', uid='', selected=False, parent=None):
        super().__init__(parent)
        self._name = name
        self._uid = uid
        self._selected = selected

    name_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=name_changed)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit(value)

    uid_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=uid_changed)
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value
        self.uid_changed.emit(value)

    selected_changed = pyqtSignal(bool)

    @pyqtProperty(bool, notify=selected_changed)
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.selected_changed.emit(value)


class ModSelectionListModel(ListModelFor(ModSelectionViewModel)):

    def get_selected_ids(self):
        return [item.uid for item in self._items if item.selected]


class GamesViewModel(QObject):
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

        self._games = GameListModel()
        self._title = None
        self._private = False
        self._featured = None
        self._map_code = None
        self._mods = ModSelectionListModel()

        self._mods.append(ModSelectionViewModel('mod 1', '1', True))
        self._mods.append(ModSelectionViewModel('mod 2', '2', False))
        self._mods.append(ModSelectionViewModel('mod 3', '3', False))

    games_changed = pyqtSignal(GameListModel)

    @pyqtProperty(GameListModel, notify=games_changed)
    def games(self):
        return self._games

    @games.setter
    def games(self, value):
        self._games = value
        self.games_changed.emit(value)

    title_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=title_changed)
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_changed.emit(value)

    private_changed = pyqtSignal(bool)

    @pyqtProperty(bool, notify=private_changed)
    def private(self):
        return self._private

    @private.setter
    def private(self, value):
        self._private = value
        self.private_changed.emit(value)

    featured_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=featured_changed)
    def featured(self):
        return self._featured

    @featured.setter
    def featured(self, value):
        self._featured = value
        self.featured_changed.emit(value)

    map_code_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=map_code_changed)
    def map_code(self):
        return self._map_code

    @map_code.setter
    def map_code(self, value):
        self._map_code = value
        self.map_code_changed.emit(value)

    mods_changed = pyqtSignal(ModSelectionListModel)

    @pyqtProperty(ModSelectionListModel, notify=mods_changed)
    def mods(self):
        return self._mods

    @mods.setter
    def mods(self, value):
        self._mods = value
        self.mods_changed.emit(value)

    @pyqtSlot()
    def on_savePreset(self):
        self.log.debug('TODO: save preset')

    @pyqtSlot()
    def on_hostGame(self):
        self.log.debug('hosting with options: {}, {}, {}, {}, mods: {}'.format(self.title, 'locked' if self.private else 'open', self.featured, self.map_code, self.mods.get_selected_ids()))
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
        game.setMap(self.map_code)
        game.setLocalPlayer(session.user, session.user_id)

        # game.start()

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
