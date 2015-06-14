from PyQt5.QtCore import QObject


class SampleItem(QObject):

    def __init__(self, foo=None, parent=None):
        super().__init__(parent)

        self.foo = foo

    def __str__(self):
        return self.__dict__.__str__()
