from PyQt5.QtCore import QObject


class Map(QObject):

    def __init__(self, code=None, name=None, description=None, version=None, slots=0, size=[0, 0], previewSmall=None, previewBig=None, parent=None):
        super().__init__(parent)

        self.code = code
        self.name = name or code
        self.description = description
        self.version = version
        self.slots = slots
        self.size = size
        self.previewSmall = previewSmall
        self.previewBig = previewBig

    def __str__(self):
        return {'code': self.code, 'version': self.version}.__str__()

    def __lt__(self, other):
        return self.name < other.name


class Mod(QObject):
    FEATURED = []

    def __init__(self, uid=None, name=None, description=None, author=None, version=None, icon=None, uiOnly=False, conflicts=None, parent=None):
        super().__init__(parent)

        self.uid = uid
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.icon = icon
        self.uiOnly = uiOnly
        self.conflicts = conflicts or []

    def __str__(self):
        return {'uid': self.uid, 'name': self.name, 'version': self.version}.__str__()

    def __le__(self, other):
        return self.name <= other.name

    def conflictsWith(self, other):
        return len(set(self.conflicts).intersection(other)) > 0
