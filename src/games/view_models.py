import asyncio
import json
import logging
from PyQt5.QtCore import QVariant, QUrl, QCoreApplication, pyqtSignal, pyqtSlot

import relays.game
from models import Map
from utils.async import asyncSlot
from widgets import Application
from view_models.adapters import ListModelFor, SelectionList, NotifyablePropertyObject, notifyableProperty
from models import FeaturedMod
from .models import Game, Preset


class GameViewModel(NotifyablePropertyObject):

    ''' View model for game tile '''

    id = notifyableProperty(int)
    mapPreviewSmall = notifyableProperty(QUrl)
    mapPreviewBig = notifyableProperty(QUrl)
    mapName = notifyableProperty(str)
    title = notifyableProperty(str)
    host = notifyableProperty(str)
    featuredModName = notifyableProperty(str)
    mods = notifyableProperty(QVariant)
    slots = notifyableProperty(int)
    players = notifyableProperty(int)
    teams = notifyableProperty(QVariant)
    balance = notifyableProperty(int)

    def __init__(self, source=None, mapLookup=None, modLookup=None, parent=None):
        super().__init__(parent)
        self._mapLookup = mapLookup or {}
        self._modLookup = modLookup or {}

        if not source:
            return

        # TODO: fix this .... seems that I need a dict or a named tuple, not a class...
        for attr in ['id', 'title', 'host', 'players', 'teams', 'balance', 'private']:
            setattr(self, attr, getattr(source, attr))

        gameMap = self.__getMap(source.mapCode)
        self.mapPreviewSmall = QUrl(gameMap.previewSmall)
        self.mapPreviewBig = QUrl(gameMap.previewBig)
        self.mapName = gameMap.name
        self.slots = gameMap.slots

        self.featuredModName = self.__getFeaturedModName(source.featuredModUid)
        self.mods = sorted([self.__getModName(m) for m in source.mods]) if source.mods else []

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getMap(self, mapCode):
        try:
            return self._mapLookup[mapCode]
        except KeyError:
            return Map()

    def __getFeaturedModName(self, uid):
        try:
            return FeaturedMod.ALL[uid].name
        except KeyError:
            return QCoreApplication.translate('GamesViewModel', 'unknown')

    def __getModName(self, uid):
        try:
            return self._modLookup[uid].name
        except KeyError:
            return QCoreApplication.translate('GamesViewModel', 'unknown')


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
        self.client = relays.game.GameClient()
        self.client.subscribeForNewGame(self.__onNewGame)

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

        for uid, f in FeaturedMod.ALL.items():
            self.featured.append(f)
        # TODO
        self.featured[0].selected = True

    # TODO: async
    def __restorePresets(self):
        import settings

        try:
            presets = json.load(open(settings.PRESETS_PATH))
            for preset in presets:
                self.presets.append(Preset(**preset))
        except FileNotFoundError:
            pass

    def __createGameViewModel(self, game):
        return GameViewModel(game, self.mapLookup, self.modLookup)

    def __onNewGame(self, game):
        self.log.debug('new game: {}'.format(game))
        g = self.__createGameViewModel(game)
        self.games.append(g)

    @pyqtSlot()
    def onAppInitComplete(self):
        for m in sorted(self.mapLookup.values(), key=lambda m: m.name.lower()):
            self.maps.append(m)
        self.maps.setSelected(0)

        for m in sorted(self.modLookup.values(), key=lambda m: m.name.lower()):
            if not m.uiOnly:
                self.mods.append(m)

        self.app.initComplete.disconnect(self.onAppInitComplete)

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
        featuredMod = self.featured.selected()
        mods = [m.uid for m in self.mods.selected()]
        selectedMap = self.maps.selected()

        newGame = Game(title=self.title, private=self.private, featuredModUid=featuredMod.uid, mods=mods, mapCode=selectedMap.code)

        self.log.debug('hosting game: {}'.format(newGame))

        with self.app.report(QCoreApplication.translate('GamesViewModel', 'hosting game')):
            response = yield from self.client.host(newGame)
            self.log.debug('server response for host: {}'.format(response))
            # TODO: add game starting logic
            yield from asyncio.sleep(5)

    @asyncSlot
    @pyqtSlot(int)
    def onJoinGame(self, id):
        self.log.debug('joining: {}'.format(id))
        with self.app.report(QCoreApplication.translate('GamesViewModel', 'joining game')):
            response = yield from self.client.join(id)
            self.log.debug('server response for join: {}'.format(response))
            # TODO: add game joining logic
            yield from asyncio.sleep(5)
