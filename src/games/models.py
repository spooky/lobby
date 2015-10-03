from PyQt5.QtCore import QObject


class Game(QObject):

    def __init__(self, id=None, mapCode=None, title=None, host=None, featuredMod=None, mods=None, slots=None, players=None, teams=None, balance=None, parent=None, private=None):
        super().__init__(parent)

        self.id = id
        self.mapCode = mapCode
        self.title = title
        self.host = host
        self.featuredMod = featuredMod
        self.mods = mods
        self.slots = slots
        self.players = players
        self.teams = teams
        self.balance = balance
        self.private = private

    def __str__(self):
        return self.__dict__.__str__()


class Preset(QObject):

    def __init__(self, name=None, featuredUid=None, mapCode=None, mods=None, private=False, parent=None):
        super().__init__(parent)

        self.name = name
        self.featuredUid = featuredUid
        self.mapCode = mapCode
        self.mods = mods
        self.private = private

    def __str__(self):
        return self.__dict__.__str__()
