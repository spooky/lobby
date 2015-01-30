import logging
import json
import asyncio

from PyQt5.QtCore import QObject

import settings
from models import Session
from session.LobbyServerContext import LobbyServerContext
from utils import rest

__all__ = ['Client']


class Client(QObject):

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)
        self.app = app

        self.server_context = LobbyServerContext('ws://{}:{}/notify/ws'.format(settings.LOBBY_HOST, settings.LOBBY_PORT), app)
        self.server_context.reconnected.connect(self._on_context_reconnected)
        self.server_context.eventReceived.connect(self._on_context_eventReceived)
        self.server_context.messageReceived.connect(self._on_context_messageReceived)
        self.server_context.start()

    @asyncio.coroutine
    def login(self, user, password):
        url = '{}/login'.format(settings.AUTH_SERVICE_URL)

        data = json.dumps({'username': user, 'password': password}).encode()
        body = yield from rest.post(url, data=data)
        session = Session(user=user, user_id=body['user_id'], email=body['email'], id=body['session_id'])

        # NOTE: move?
        if body['success']:
            self.app.session = session
            self.server_context.sendMessage('auth', 'login', session.id)

        return body['success']

    @asyncio.coroutine
    def logout(self):
        # NOTE: logout url disabled for some reason... waiting for more info
        # url = '{}/logout'.format(settings.AUTH_SERVICE_URL)

        # body = yield from rest.post(url)
        # self.log.debug(body)

        # NOTE: move?
        self.app.session = None

        return True

    @asyncio.coroutine
    def get_games(self):
        url = '{}/games/current'.format(settings.FAF_SERVICE_URL)

        body = yield from rest.get(url)

        return body

    def _on_context_reconnected(self):
        self.server_context.sendNotify('subscribe', 'games')

    def _on_context_eventReceived(self, event_id, args):
        self.log.debug('server event received: {}, args: {}'.format(event_id, args))

    def _on_context_messageReceived(self, subsystem, command, args):
        self.log.debug('server message received. subsystem: {}, command: {}, args: {}'.format(subsystem, command, args))
