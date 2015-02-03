import json

data = json.loads('{"id": 93, "host": {"ip": "89.64.254.67", "port": 6112, "username": "spooky"}, "GameOption": {"Timeouts": "3", "NavalExpansionsAllowed": "4", "Score": "no", "LandExpansionsAllowed": "5", "Victory": "demoralization", "TeamLock": "locked", "AutoTeams": "pvsi", "CheatMult": "2.2", "AllowObservers": 0, "RankedGame": "Off", "PrebuiltUnits": "Off", "ScenarioFile": "/maps/scmp_009/scmp_009_scenario.lua", "OmniCheat": "on", "ShareUnitCap": "allies", "RandomMap": "Off", "FogOfWar": "explored", "UnitCap": "1000", "CivilianAlliance": "enemy", "Slots": 8, "TeamSpawn": "random", "CheatsEnabled": "false", "BuildMult": "2.0", "Share": "yes", "TMLRandom": "0", "NoRushOption": "Off", "GameSpeed": "adjustable"}, "GameState": "Lobby", "PlayerOption": {"1": {"PlayerName": "spooky", "RC": "ffffffff", "DEV": 0, "OwnerID": "3", "Country": "world", "Team": 0, "MEAN": 1000, "NG": 0, "Ready": 0, "Civilian": 0, "ArmyColor": 3, "COUNTRY": "world", "Faction": 3, "Human": 1, "AIPersonality": "", "PlayerColor": 3, "StartSpot": 1, "PL": 1000}}, "Title": "test", "GameMods": ["921bdf63-c14a-1415-a758-42d1c231e4f4"]}')


def test_GameViewModel_get_teams_arrangement():
    from view_models.games import GameViewModel

    teams = GameViewModel.get_teams_arrangement(data)
    expected = [[{'name': 'spooky', 'skill': 1000, 'cc': 'world'}]]

    assert teams == expected


def test_test_GameViewModel_data():
    from models import Map
    from view_models.games import GameViewModel

    map_lookup = {'scmp_009': Map(code='scmp_009', name="Seton's")}
    g = GameViewModel(data, map_lookup=map_lookup)
    assert g.id == 93
    assert g.map_name == "Seton's"
    # assert g.map == 'url_to_preview'
    assert g.title == 'test'
    assert g.host == 'spooky'
    # assert g.featured_mod == 'FAF'
    # assert g.mods == []
    assert g.slots == 8
    assert g.player_count == 1
    assert g.balance == 0


def test_GameViewModel_equality():
    from view_models.games import GameViewModel

    g1 = GameViewModel(dict(id=1, Title='title'))
    g2 = GameViewModel(dict(id=1, Title='other title'))

    assert g1 == g2


def test_GameViewModel_inequality():
    from view_models.games import GameViewModel

    g1 = GameViewModel(dict(id=1, Title='title'))
    g2 = GameViewModel(dict(id=2, Title='other title'))

    assert g1 != g2


def test_GameViewModel_list_check():
    from view_models.games import GameViewModel

    g1 = GameViewModel(dict(id=1, Title='title'))
    g2 = GameViewModel(dict(id=1, Title='other title'))

    assert g1 in [g2]
