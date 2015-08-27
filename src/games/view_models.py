import logging
import json
from itertools import groupby
from PyQt5.QtCore import QVariant, QUrl, QCoreApplication, pyqtSignal, pyqtSlot

from models import Map, Mod
from widgets import Application
from view_models.adapters import ListModelFor, SelectionList, NotifyablePropertyObject, notifyableProperty

from .models import Preset


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
        self.featured_mod, self.mods = self.get_mods(source.get('GameMods') or [])
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
    presets = notifyableProperty(SelectionList)

    savePreset = pyqtSignal()
    hostGame = pyqtSignal()
    joinGame = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        app = Application.instance()

        self.savePreset.connect(self.on_savePreset)
        self.hostGame.connect(self.on_hostGame)
        self.joinGame.connect(self.on_joinGame)

        self.map_lookup = app.map_lookup
        self.mod_lookup = app.mod_lookup

        self.games = GameListModel()

        self.presets = SelectionList(item_name_extractor=lambda p: p.title)
        self._restore_presets()

        self.title = None
        self.private = False

        def get_name(x):
            return x.name

        self.featured = SelectionList(item_name_extractor=get_name)
        self.maps = SelectionList(item_name_extractor=get_name)
        self.mods = SelectionList(multiple=True, item_name_extractor=get_name)

        app.init_complete.connect(self.on_app_init_complete)

        # TODO: remove test data
        self.featured.append(Mod('uid-faf', 'Forged Alliance Forever'), selected=True)
        self.featured.append(Mod('uid-vanilla', 'Vanilla'))
        self.featured.append(Mod('uid-phantom', 'Phantom X'))
        self.featured.append(Mod('uid-nomads', 'The Nomads'))

    # TODO: async
    def _restore_presets(self):
        # TODO: path... should either have a fixed dir or search up until a point
        presets = json.load(open('../presets.json'))
        for preset in presets:
            self.presets.append(Preset(**preset))

    def on_app_init_complete(self):
        for m in sorted(self.map_lookup.values(), key=lambda m: m.name.lower()):
            self.maps.append(m)
        self.maps.setSelected(0)

        for m in sorted(self.mod_lookup.values(), key=lambda m: m.name.lower()):
            if not m.ui_only:
                self.mods.append(m)

        # TODO: remove test data
        import json
        data = json.loads('{"id":93,"host":{"ip":"89.64.254.67","port":6112,"username":"spooky"},"GameOption":{"Timeouts":"3","NavalExpansionsAllowed":"4","Score":"no","LandExpansionsAllowed":"5","Victory":"demoralization","TeamLock":"locked","AutoTeams":"pvsi","CheatMult":"2.2","AllowObservers":0,"RankedGame":"Off","PrebuiltUnits":"Off","ScenarioFile":"/maps/3v3 Sand Box v2a/3v3 Sand Box v2a_scenario.lua","OmniCheat":"on","ShareUnitCap":"allies","RandomMap":"Off","FogOfWar":"explored","UnitCap":"1000","CivilianAlliance":"enemy","Slots":6,"TeamSpawn":"random","CheatsEnabled":"false","BuildMult":"2.0","Share":"yes","TMLRandom":"0","NoRushOption":"Off","GameSpeed":"adjustable"},"GameState":"Lobby","PlayerOption":{"1":{"PlayerName":"crunchy","RC":"ffffffff","DEV":0,"OwnerID":"3","Country":"pl","Team":0,"MEAN":1000,"NG":0,"Ready":0,"Civilian":0,"ArmyColor":3,"COUNTRY":"pl","Faction":3,"Human":1,"AIPersonality":"","PlayerColor":3,"StartSpot":1,"PL":1000},"2":{"PlayerName":"creamy","RC":"ffffffff","DEV":0,"OwnerID":"3","Country":"dk","Team":0,"MEAN":100,"NG":0,"Ready":0,"Civilian":0,"ArmyColor":3,"COUNTRY":"dk","Faction":3,"Human":1,"AIPersonality":"","PlayerColor":3,"StartSpot":1,"PL":1000},"3":{"PlayerName":"cookie","RC":"ffffffff","DEV":0,"OwnerID":"3","Country":"fi","Team":1,"MEAN":1500,"NG":0,"Ready":0,"Civilian":0,"ArmyColor":3,"COUNTRY":"fi","Faction":3,"Human":1,"AIPersonality":"","PlayerColor":3,"StartSpot":1,"PL":1000}},"Title":"test","GameMods":["921bdf63-c14a-1415-a758-42d1c231e4f4", "EEFFA8C6-96D9-11E4-9DA1-460D1D5D46B0"]}')
        for i in range(1):
            g = GameViewModel(data, self.map_lookup, self.mod_lookup)
            self.games.append(g)

    # TODO: implement preset saving
    @pyqtSlot()
    def on_savePreset(self):
        try:
            # TODO: remove test data
            self.featured.setSelected(1)
            self.maps.setSelected(7)
            self.mods.setSelected(4)
            self.mods.setSelected(8)
            self.log.debug('changed settings')
        except Exception as e:
            self.log.error(e)

    @pyqtSlot()
    def on_hostGame(self):
        self.log.debug('hosting with options: {}, {}, {}, {}, mods: {}'.format(
            self.title,
            'locked' if self.private else 'open',
            self.featured.selected(),
            self.maps.selected(),
            [m.uid for m in self.mods.selected()]))

        Application.instance().report_indefinite(QCoreApplication.translate('GamesViewModel', 'hosting game'))
        session = QCoreApplication.instance().session
        if not session:
            # TODO: display 'not logged in' error
            return None
        # TODO: add game starting logic here

    @pyqtSlot(int)
    def on_joinGame(self, id):
        self.log.debug('joining: {}'.format(id))
        Application.instance().report_indefinite(QCoreApplication.translate('GamesViewModel', 'joining game'))

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
