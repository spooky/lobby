from PyQt5.QtCore import QObject


class Preset(QObject):

    def __init__(self, title=None, featured_uid=None, map_code=None, mods=None, private=False, parent=None):
        super().__init__(parent)

        self.title = title
        self.featured_uid = featured_uid
        self.map_code = map_code
        self.mods = mods
        self.private = private

    def __str__(self):
        return self.__dict__.__str__()
