import asyncio
import logging
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from relays.auth import AuthServer
from view_models.adapters import NotifyablePropertyObject, notifyableProperty


class AuthViewModel(AuthServer, NotifyablePropertyObject):
    user = notifyableProperty(str)
    pending = notifyableProperty(bool)

    accept = pyqtSignal()
    reject = pyqtSignal()

    def __init__(self, client=None, server=None, parent=None):
        NotifyablePropertyObject.__init__(self, parent)

        self._future = None

        self.log = logging.getLogger(__name__)

        self.pending = False
        self.accept.connect(self.onAccept)
        self.reject.connect(self.onReject)

    def _getFutureDecision(self, user):
        self._future = asyncio.Future()
        self.user = user
        self.pending = True
        return self._future

    def _resolveDecision(self, value, action):
        if self._future:
            self._future.set_result(value)
            self.log.debug('{} user {}'.format(action, self.user))
            self._future = self.user = None
            self.pending = False

    @pyqtSlot()
    def onAccept(self):
        self._resolveDecision(True, 'accepted')

    @pyqtSlot()
    def onReject(self):
        self._resolveDecision(False, 'rejected')

    @asyncio.coroutine
    def request_login(self, user, password):
        return self._getFutureDecision(user)

    @asyncio.coroutine
    def request_logout(self, user):
        return self._getFutureDecision(user)

# yyy... ehh...
authViewModel = AuthViewModel()
