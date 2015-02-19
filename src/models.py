from PyQt5.QtCore import QObject


class Session(QObject):

    def __init__(self, user=None, user_id=None, email=None, id=None, parent=None):
        super().__init__(parent)

        self.user = user
        self.user_id = user_id
        self.email = email
        self.id = id

    def __str__(self):
        return self.__dict__.__str__()


class Map(QObject):

    def __init__(self, code=None, name=None, description=None, version=None, slots=0, size=[0, 0], preview_small=None, preview_big=None, parent=None):
        super().__init__(parent)

        self.code = code
        self.name = name or code
        self.description = description
        self.version = version
        self.slots = slots
        self.size = size
        self.preview_small = preview_small
        self.preview_big = preview_big

    def __str__(self):
        return {'code': self.code, 'version': self.version}.__str__()


class Mod(QObject):
    FEATURED = []

    def __init__(self, uid=None, name=None, description=None, author=None, version=None, icon=None, ui_only=False, conflicts=[], parent=None):
        super().__init__(parent)

        self.uid = uid
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.icon = icon
        self.ui_only = ui_only
        self.conflicts = conflicts

    def __str__(self):
        return {'uid': self.uid, 'name': self.name, 'version': self.version}.__str__()

    def conflicts_with(self, other):
        return len(set(self.conflicts).intersection(other)) > 0
