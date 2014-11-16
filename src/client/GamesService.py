from session.IRESTService import IRESTService

from client import GAMES_SERVICE_URL

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
    def OpenGame(port, game_params):
        return IRESTService._post(GAMES_SERVICE_URL + "/open", { 'port': port, 'game_params': game_params })