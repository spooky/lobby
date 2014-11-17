
from .IRESTService import IRESTService

from . import AUTH_SERVICE_URL

class AuthService(IRESTService):
    @staticmethod
    def Register(email, username, password):
        # FIXME Sheeo Password hashing
        postData = {'email': email,
                    'username': username,
                    'password': password}

        return IRESTService._post(AUTH_SERVICE_URL + "/register", postData)

    @staticmethod
    def Login(username, password):
        # FIXME Sheeo Password hashing
        postData = {'username': username,
                    'password': password}

        return IRESTService._post(AUTH_SERVICE_URL + "/login", postData)