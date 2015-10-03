def test_test_GameViewModel_data():
    from models import Map
    from games.models import Game
    from games.view_models import GameViewModel

    mapLookup = {'scmp_009': Map(code='scmp_009', name="Seton's", slots=8)}
    game = Game(id=93, title='test', host='spooky', players=1, balance=0, mapCode='scmp_009')
    g = GameViewModel(game, mapLookup=mapLookup)
    assert g.id == 93
    assert g.mapName == "Seton's"
    # assert g.map == 'url_to_preview'
    assert g.title == 'test'
    assert g.host == 'spooky'
    # assert g.featuredMod == 'FAF'
    # assert g.mods == []
    assert g.slots == 8
    assert g.players == 1
    assert g.balance == 0


def test_GameViewModel_equality():
    from games.models import Game
    from games.view_models import GameViewModel

    g1 = GameViewModel(Game(id=1, title='title'))
    g2 = GameViewModel(Game(id=1, title='other title'))

    assert g1 == g2


def test_GameViewModel_inequality():
    from games.models import Game
    from games.view_models import GameViewModel

    g1 = GameViewModel(Game(id=1, title='title'))
    g2 = GameViewModel(Game(id=2, title='other title'))

    assert g1 != g2


def test_GameViewModel_list_check():
    from games.models import Game
    from games.view_models import GameViewModel

    g1 = GameViewModel(Game(id=1, title='title'))
    g2 = GameViewModel(Game(id=1, title='other title'))

    assert g1 in [g2]
