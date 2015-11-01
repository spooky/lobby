import json
import settings

from PyQt5.QtCore import QObject


class GameOptions(QObject):

    def __init__(self, title=None, featuredModUid=None, mapCode=None, mods=None, private=False, parent=None):
        super().__init__(parent)

        self.title = title
        self.featuredModUid = featuredModUid
        self.mapCode = mapCode
        self.mods = mods
        self.private = private

    def __str__(self):
        return self.__dict__.__str__()


class Game(GameOptions):

    def __init__(self, id=None, host=None, slots=None, players=None, teams=None, balance=None, **kwargs):
        super().__init__(**kwargs)

        self.id = id
        self.host = host
        self.slots = slots
        self.players = players  # TODO: remove, this info is stored indirectly in teams prop
        self.teams = teams
        self.balance = balance

    def __str__(self):
        return self.__dict__.__str__()


class Preset(GameOptions):

    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)

        self.name = name

    def __str__(self):
        return self.__dict__.__str__()


def load_presets():
    try:
        presets = json.load(open(settings.PRESETS_PATH))
        for preset in presets:
            yield Preset(**preset)
    except FileNotFoundError:
        pass


def save_presets(presets):
    with open(settings.PRESETS_PATH, 'w') as fp:
        json.dump([p.__dict__ for p in presets if p is not None], fp, indent=2)
