from PyQt5.QtCore import QObject


class Preset(QObject):

    def __init__(self, title=None, featuredUid=None, mapCode=None, mods=None, private=False, parent=None):
        super().__init__(parent)

        self.title = title
        self.featuredUid = featuredUid
        self.mapCode = mapCode
        self.mods = mods
        self.private = private

    def __str__(self):
        return self.__dict__.__str__()
