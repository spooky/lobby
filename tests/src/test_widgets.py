import sys


def test_ViewManager_convertName():
    from widgets import ViewManager

    vm = ViewManager(None, None)

    assert vm._convertName('games') == 'Games'
    assert vm._convertName('_find_games') == 'FindGames'
    assert vm._convertName('find_games') == 'FindGames'
    assert vm._convertName('FindGames') == 'FindGames'


def test_ViewManager_getView_on_games_view():
    from widgets import Application, ViewManager
    from games.view_models import GamesViewModel

    app = Application(sys.argv)

    vm = ViewManager(None, None)
    vm.registerView('games')
    path, view_model = vm.getView('games')

    assert path == 'Games'
    assert type(view_model) is GamesViewModel
