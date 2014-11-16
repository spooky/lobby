import settings
from .IRESTService import IRESTService


class AuthService(IRESTService):
    @staticmethod
    def Register(email, username, password):
        # FIXME Sheeo Password hashing
        postData = {'email': email,
                    'username': username,
                    'password': password}

        return IRESTService._post(settings.AUTH_SERVICE_URL + "/register", postData)

    @staticmethod
    def Login(username, password):
        # FIXME Sheeo Password hashing
        postData = {'username': username,
                    'password': password}

        return IRESTService._post(settings.AUTH_SERVICE_URL + "/login", postData)
