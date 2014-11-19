__all__ = ['Client']

import logging
import json
import asyncio

from PyQt5.QtCore import QObject

import settings
from utils import rest


class Client(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

    @asyncio.coroutine
    def login(self, user, password):
        url = '{}/login'.format(settings.AUTH_SERVICE_URL)

        data = json.dumps({'username': user, 'password': password}).encode()

        body = yield from rest.post(url, data=data)

        self.session_id = body['session_id']
        self.user_id = body['user_id']
        self.email = body['email']

        return body['success']

    @asyncio.coroutine
    def logout(self):
        url = '{}/logout'.format(settings.AUTH_SERVICE_URL)

        self.session_id = None
        self.user_id = None
        self.email = None

        return True

    @asyncio.coroutine
    def get_games(self):
        url = '{}/games/current'.format(settings.FAF_SERVICE_URL)

        body = yield from rest.get(url)

        return body
