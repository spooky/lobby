
from IRESTService import IRESTService

GAMES_SERVICE_URL = "http://localhost:8080/games"

class GamesService(IRESTService):
    @staticmethod
    def Current():
        return IRESTService._get(GAMES_SERVICE_URL + "/current")

    @staticmethod
    def Info(game_id):
        return IRESTService._get(GAMES_SERVICE_URL + "/%d/info" % game_id)

    @staticmethod
    def LiveReplay(game_id):
        return IRESTService._get(GAMES_SERVICE_URL + "/%d/livereplay" % game_id)

    @staticmethod
    def OpenGame(game_params):
        return IRESTService._post(GAMES_SERVICE_URL + "/open", game_params)