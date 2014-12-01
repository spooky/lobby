import json

data = json.loads('{"id": 93, "host": {"ip": "89.64.254.67", "port": 6112, "username": "spooky"}, "GameOption": {"Timeouts": "3", "NavalExpansionsAllowed": "4", "Score": "no", "LandExpansionsAllowed": "5", "Victory": "demoralization", "TeamLock": "locked", "AutoTeams": "pvsi", "CheatMult": "2.2", "AllowObservers": 0, "RankedGame": "Off", "PrebuiltUnits": "Off", "ScenarioFile": "/maps/scmp_009/scmp_009_scenario.lua", "OmniCheat": "on", "ShareUnitCap": "allies", "RandomMap": "Off", "FogOfWar": "explored", "UnitCap": "1000", "CivilianAlliance": "enemy", "Slots": 8, "TeamSpawn": "random", "CheatsEnabled": "false", "BuildMult": "2.0", "Share": "yes", "TMLRandom": "0", "NoRushOption": "Off", "GameSpeed": "adjustable"}, "GameState": "Lobby", "PlayerOption": {"1": {"PlayerName": "spooky", "RC": "ffffffff", "DEV": 0, "OwnerID": "3", "Country": "world", "Team": 0, "MEAN": 1000, "NG": 0, "Ready": 0, "Civilian": 0, "ArmyColor": 3, "COUNTRY": "world", "Faction": 3, "Human": 1, "AIPersonality": "", "PlayerColor": 3, "StartSpot": 1, "PL": 1000}}, "Title": "test", "GameMods": ["921bdf63-c14a-1415-a758-42d1c231e4f4"]}')


def test_GameViewModel_get_map():
    from view_models.games import GameViewModel
    assert GameViewModel.get_map(data) == 'scmp_009'


def test_GameViewModel_get_player_count():
    from view_models.games import GameViewModel
    assert GameViewModel.get_player_count(data) == 1
