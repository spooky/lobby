import asyncio
import json
import logging
from itertools import groupby
from PyQt5.QtCore import QVariant, QUrl, QCoreApplication, pyqtSignal, pyqtSlot

from models import Map, Mod
from utils.async import asyncSlot
from widgets import Application
from view_models.adapters import ListModelFor, SelectionList, NotifyablePropertyObject, notifyableProperty

from .models import Preset


class GameViewModel(NotifyablePropertyObject):

    ''' View model for game tile '''

    id = notifyableProperty(int)
    mapPreviewSmall = notifyableProperty(QUrl)
    mapPreviewBig = notifyableProperty(QUrl)
    mapName = notifyableProperty(str)
    title = notifyableProperty(str)
    host = notifyableProperty(str)
    featuredMod = notifyableProperty(str)
    mods = notifyableProperty(QVariant)
    slots = notifyableProperty(int)
    playerCount = notifyableProperty(int)
    teamsArrangement = notifyableProperty(QVariant)
    balance = notifyableProperty(int)

    def __init__(self, source=None, mapLookup=None, modLookup=None, parent=None):
        super().__init__(parent)
        self._mapLookup = mapLookup or {}
        self._modLookup = modLookup or {}

        if not source:
            return

        self.id = source.get('id')
        gameMap = self.getMap(source)
        self.mapPreviewSmall = QUrl(gameMap.previewSmall)
        self.mapPreviewBig = QUrl(gameMap.previewBig)
        self.mapName = gameMap.name
        self.title = source.get('Title')
        self.host = source['host'].get('username') if 'host' in source.keys() else None
        self.featuredMod, self.mods = self.getMods(source.get('GameMods') or [])
        self.slots = source['GameOption'].get('Slots', 0) if 'GameOption' in source.keys() else 0
        self.playerCount = len(source.get('PlayerOption') or [])
        self.teamsArrangement = self.getTeamsArrangement(source)
        self.balance = 0

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def getMap(self, source):
        try:
            scenario = source['GameOption']['ScenarioFile']
            return self._mapLookup[scenario.split('/')[2]]
        except KeyError:
            return Map()

    def getMods(self, mods):
        names = []
        for m in mods:
            try:
                names.append(self._modLookup[m].name)
            except KeyError:
                names.append(QCoreApplication.translate('GamesViewModel', 'unknown'))

        return ('featured (todo)', sorted(names))  # (featured, other)

    @staticmethod
    def getTeamsArrangement(source):
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

        self.app = Application.instance()

        self.savePreset.connect(self.onSavePreset)
        self.hostGame.connect(self.onHostGame)
        self.joinGame.connect(self.onJoinGame)

        self.mapLookup = self.app.mapLookup
        self.modLookup = self.app.modLookup

        self.games = GameListModel()

        self.presets = SelectionList()
        self.__restorePresets()

        self.title = None
        self.private = False

        self.featured = SelectionList()
        self.maps = SelectionList()
        self.mods = SelectionList(multiple=True)

        self.app.initComplete.connect(self.onAppInitComplete)

        # TODO: remove test data
        self.featured.append(Mod('uid-faf', 'Forged Alliance Forever'), selected=True)
        self.featured.append(Mod('uid-vanilla', 'Vanilla'))
        self.featured.append(Mod('uid-phantom', 'Phantom X'))
        self.featured.append(Mod('uid-nomads', 'The Nomads'))

    # TODO: async
    def __restorePresets(self):
        # TODO: path... should either have a fixed dir or search up until a point
        presets = json.load(open('../presets.json'))
        for preset in presets:
            self.presets.append(Preset(**preset))

    def onAppInitComplete(self):
        for m in sorted(self.mapLookup.values(), key=lambda m: m.name.lower()):
            self.maps.append(m)
        self.maps.setSelected(0)

        for m in sorted(self.modLookup.values(), key=lambda m: m.name.lower()):
            if not m.uiOnly:
                self.mods.append(m)

        # TODO: remove test data
        import json
        data = json.loads('{"id":93,"host":{"ip":"89.64.254.67","port":6112,"username":"spooky"},"GameOption":{"Timeouts":"3","NavalExpansionsAllowed":"4","Score":"no","LandExpansionsAllowed":"5","Victory":"demoralization","TeamLock":"locked","AutoTeams":"pvsi","CheatMult":"2.2","AllowObservers":0,"RankedGame":"Off","PrebuiltUnits":"Off","ScenarioFile":"/maps/3v3 Sand Box v2a/3v3 Sand Box v2a_scenario.lua","OmniCheat":"on","ShareUnitCap":"allies","RandomMap":"Off","FogOfWar":"explored","UnitCap":"1000","CivilianAlliance":"enemy","Slots":6,"TeamSpawn":"random","CheatsEnabled":"false","BuildMult":"2.0","Share":"yes","TMLRandom":"0","NoRushOption":"Off","GameSpeed":"adjustable"},"GameState":"Lobby","PlayerOption":{"1":{"PlayerName":"crunchy","RC":"ffffffff","DEV":0,"OwnerID":"3","Country":"pl","Team":0,"MEAN":1000,"NG":0,"Ready":0,"Civilian":0,"ArmyColor":3,"COUNTRY":"pl","Faction":3,"Human":1,"AIPersonality":"","PlayerColor":3,"StartSpot":1,"PL":1000},"2":{"PlayerName":"creamy","RC":"ffffffff","DEV":0,"OwnerID":"3","Country":"dk","Team":0,"MEAN":100,"NG":0,"Ready":0,"Civilian":0,"ArmyColor":3,"COUNTRY":"dk","Faction":3,"Human":1,"AIPersonality":"","PlayerColor":3,"StartSpot":1,"PL":1000},"3":{"PlayerName":"cookie","RC":"ffffffff","DEV":0,"OwnerID":"3","Country":"fi","Team":1,"MEAN":1500,"NG":0,"Ready":0,"Civilian":0,"ArmyColor":3,"COUNTRY":"fi","Faction":3,"Human":1,"AIPersonality":"","PlayerColor":3,"StartSpot":1,"PL":1000}},"Title":"test","GameMods":["921bdf63-c14a-1415-a758-42d1c231e4f4", "EEFFA8C6-96D9-11E4-9DA1-460D1D5D46B0"]}')
        for i in range(1):
            g = GameViewModel(data, self.mapLookup, self.modLookup)
            self.games.append(g)

    # TODO: implement preset saving
    @pyqtSlot()
    def onSavePreset(self):
        try:
            # TODO: remove test data
            self.featured.setSelected(1)
            self.maps.setSelected(7)
            self.mods.setSelected(4)
            self.mods.setSelected(8)
            self.log.debug('changed settings')
        except Exception as e:
            self.log.error(e)

    @asyncSlot
    @pyqtSlot()
    def onHostGame(self):
        self.log.debug('hosting with options: {}, {}, {}, {}, mods: {}'.format(
            self.title,
            'locked' if self.private else 'open',
            self.featured.selected(),
            self.maps.selected(),
            [m.uid for m in self.mods.selected()]))

        with self.app.report(QCoreApplication.translate('GamesViewModel', 'hosting game')):
            # TODO: add game starting logic
            yield from asyncio.sleep(5)

    @asyncSlot
    @pyqtSlot(int)
    def onJoinGame(self, id):
        self.log.debug('joining: {}'.format(id))
        with self.app.report(QCoreApplication.translate('GamesViewModel', 'joining game')):
            # TODO: add game joining logic
            yield from asyncio.sleep(5)

    def onOpened(self, args):
        g = GameViewModel(args, self.mapLookup, self.modLookup)
        self.games.append(g)
        self.log.debug('added game id: {}'.format(g.id))

    def onUpdated(self, args):
        g = GameViewModel(args, self.mapLookup, self.modLookup)
        self.games.update(g)
        self.log.debug('updated game id: {}'.format(g.id))

    def onClosed(self, args):
        g = GameViewModel(args, self.mapLookup, self.modLookup)
        self.games.remove(g)
        self.log.debug('closed game id: {}'.format(g.id))
