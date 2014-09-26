import json

from PyQt4.QtCore import *

from PyQt4.QtNetwork import *

from client import networkAccessManager


AUTH_SERVICE_URL = "http://localhost:44343/do"


class AuthService:
    @staticmethod
    def Register(email, username, password):
        req = QNetworkRequest(QUrl(AUTH_SERVICE_URL + "/register"))
        req.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        # FIXME Sheeo Password hashing
        postData = {'email': email,
                    'username': username,
                    'password': password}

        return networkAccessManager.post(req, json.dumps(postData).encode())

    @staticmethod
    def Login(username, password):
        req = QNetworkRequest(QUrl(AUTH_SERVICE_URL + "/login"))
        req.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        # FIXME Sheeo Password hashing
        postData = {'username': username,
                    'password': password}

        return networkAccessManager.post(req, json.dumps(postData).encode())