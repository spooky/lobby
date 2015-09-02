import asyncio
import logging
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from view_models.adapters import NotifyablePropertyObject, notifyableProperty
import relays.auth


class AuthViewModel(relays.auth.AuthMediator, NotifyablePropertyObject):
    user = notifyableProperty(str)
    pending = notifyableProperty(bool)

    accept = pyqtSignal()
    reject = pyqtSignal()

    def __init__(self, client=None, server=None, parent=None):
        NotifyablePropertyObject.__init__(self, parent)
        relays.auth.AuthMediator.__init__(self)

        self._future = None

        self.log = logging.getLogger(__name__)

        self.pending = False
        self.accept.connect(self.on_accept)
        self.reject.connect(self.on_reject)

    def _get_future_decision(self, user):
        self._future = asyncio.Future()
        self.user = user
        self.pending = True
        return self._future

    def _resolve_decision(self, value, action):
        if self._future:
            self._future.set_result(value)
            self.log.debug('{} user {}'.format(action, self.user))
            self._future = self.user = None
            self.pending = False

    @pyqtSlot()
    def on_accept(self):
        self._resolve_decision(True, 'accepted')

    @pyqtSlot()
    def on_reject(self):
        self._resolve_decision(False, 'rejected')

    @asyncio.coroutine
    def login(self, user, password):
        decision = yield from self._get_future_decision(user)
        return (yield from self.server.login(user, password, success=decision))

    @asyncio.coroutine
    def logout(self, user):
        decision = yield from self._get_future_decision(user)
        return (yield from self.server.logout(user, success=decision))

# yyy... ehh...
auth_view_model = AuthViewModel()
