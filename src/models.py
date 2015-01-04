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

    def __init__(self, code=None, name=None, slots=0, description=None):
        self.code = code
        self.name = name or code
        self.slots = slots
        self.description = description

    def preview_url(self):
        return (None, None)  # (small, big or small)
