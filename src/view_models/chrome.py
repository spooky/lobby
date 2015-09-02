import logging
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QVariant

import settings
from utils.async import async_slot
from .adapters import NotifyablePropertyObject, notifyableProperty


class MainWindowViewModel(NotifyablePropertyObject):
    label = notifyableProperty(str)
    taskRunning = notifyableProperty(bool)
    taskStatusText = notifyableProperty(str)
    taskStatusIsIndefinite = notifyableProperty(bool)
    taskStatusProgress = notifyableProperty(float)
    registeredViews = notifyableProperty(QVariant)
    currentView = notifyableProperty(str)

    switchView = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = settings.VERSION

        self.taskRunning = False  # wether to show the task indicator
        self.taskStatusText = None  # text to show while task is running
        self.taskStatusIsIndefinite = True  # wether to hide the progress bar progress bar progress value - makes sense only if taskStatusIsIndefinite == True
        self.taskStatusProgress = 0

        self.registeredViews = list()
        self.currentView = None

    def setTaskStatus(self, text, progress=0.0, indefinite=True):
        self.taskStatusText = text
        self.taskStatusProgress = progress
        self.taskStatusIsIndefinite = indefinite
        self.taskRunning = True

    def clearTaskStatus(self):
        self.taskRunning = False
        self.taskStatusIsIndefinite = True
        self.taskStatusText = None
        self.taskStatusProgress = 0.0


class LoginViewModel(NotifyablePropertyObject):
    user = notifyableProperty(str)
    password = notifyableProperty(str)
    remember = notifyableProperty(bool)
    logged_in = notifyableProperty(bool)
    panel_visible = notifyableProperty(bool)

    login = pyqtSignal(str, str, bool)
    logout = pyqtSignal()

    def __init__(self, client, user=None, password=None, remember=None, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.login.connect(self.on_login)
        self.logout.connect(self.on_logout)
        self.client = client
        self.user = user
        self.password = password
        self.remember = remember or False
        self.logged_in = False
        self.panel_visible = False

    @async_slot
    def autologin(self):
        try:
            self.log.info('logging in (auto)...')
            self.logged_in = yield from self.client.login(self.user, self.password)
            self.log.debug('autologin result: {}'.format(self.logged_in))
        except Exception as e:
            self.log.error('autologin failed. {}'.format(e))

    @async_slot
    @pyqtSlot(str, str, bool)
    def on_login(self, user, password, remember):
        try:
            import hashlib
            pass_hash = hashlib.sha256(password.encode()).hexdigest()

            self.log.info('logging in...')
            self.logged_in = yield from self.client.login(user, pass_hash)
            self.panel_visible = not self.logged_in

            self.store_credentials(user, pass_hash, remember)

            self.log.debug('login successful? {}'.format(self.logged_in))

        except Exception as ex:
            self.log.warn('login failed: {}'.format(ex))

    @async_slot
    @pyqtSlot()
    def on_logout(self):
        try:
            self.log.info('logging out...')
            self.logged_in = not (yield from self.client.logout(self.user))

            self.log.debug('logout successful? {}'.format(not self.logged_in))

        except Exception as ex:
            self.log.warn('logout failed: {}'.format(ex))

    def store_credentials(self, user, password, remember):
        s = settings.get()
        s.beginGroup('login')

        s.setValue('user', user)
        s.setValue('password', password)
        s.setValue('remember', remember)

        s.endGroup()

    def read_credentials(self):
        stored = settings.get()
        stored.beginGroup('login')

        self.user = stored.value('user')
        self.password = stored.value('password')
        self.remember = stored.value('remember') == 'true'

        stored.endGroup()
