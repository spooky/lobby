# ViewManager
def test_convert_name():
    from widgets import ViewManager

    vm = ViewManager(None, None)

    assert vm._convert_name('games') == 'Games'
    assert vm._convert_name('_find_games') == 'FindGames'
    assert vm._convert_name('find_games') == 'FindGames'
    assert vm._convert_name('FindGames') == 'FindGames'


def test_get_view_on_games_view():
    from widgets import ViewManager
    from view_models import GamesViewModel

    vm = ViewManager(None, None)

    path, view_model = vm.get_view('games', None)

    assert path == 'Games.qml'
    assert type(view_model) is GamesViewModel
