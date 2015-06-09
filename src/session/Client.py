import logging
import asyncio

from PyQt5.QtCore import QObject

from models import Session

__all__ = ['Client']


class Client(QObject):

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)
        self.app = app

    @asyncio.coroutine
    def login(self, user, password):
        body = {'user_id': 1, 'email': 'user@example.com', 'session_id': 123}
        session = Session(user=user, user_id=body['user_id'], email=body['email'], id=body['session_id'])
        self.app.session = session

        return True

    @asyncio.coroutine
    def logout(self):
        self.app.session = None

        return True
