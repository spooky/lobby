import sys
from PyQt5.QtCore import QObject, pyqtSignal


class ServerContextStub(QObject):
    eventReceived = pyqtSignal(list, object)

    def __init__(self, parent=None):
        super().__init__(parent)


def test_ViewManager_convert_name():
    from widgets import ViewManager

    vm = ViewManager(None, None)

    assert vm._convert_name('games') == 'Games'
    assert vm._convert_name('_find_games') == 'FindGames'
    assert vm._convert_name('find_games') == 'FindGames'
    assert vm._convert_name('FindGames') == 'FindGames'


def test_ViewManager_get_view_on_games_view():
    from widgets import Application, ViewManager
    from view_models.games import GamesViewModel

    app = Application(sys.argv)  # could be done better, but this is 'just' a test
    app.start()
    vm = ViewManager(None, None)
    storage_stub = {}
    path, view_model = vm.get_view('games', ServerContextStub(), storage_stub, storage_stub)

    assert path == 'Games'
    assert type(view_model) is GamesViewModel
