import logging
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QVariant, QCoreApplication
from PyQt5.QtQml import qmlRegisterType

import settings
from utils.async import asyncSlot
from .adapters import NotifyablePropertyObject, ListModelFor, notifyableProperty


class TaskStatusViewModel(NotifyablePropertyObject):

    ''' View model for reporting a running task '''

    text = notifyableProperty(str)
    indefinite = notifyableProperty(bool)
    progress = notifyableProperty(float)
    running = notifyableProperty(bool)
    success = notifyableProperty(bool)

    def __init__(self, text='', indefinite=True, progress=0.0, running=False):
        super().__init__()

        self.text = text
        self.indefinite = indefinite
        self.progress = progress
        self.running = running

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exctype, excval, exctb):
        if exctype:
            self.cancel()
        else:
            self.done()

    def start(self):
        self.running = True
        self.progress = 0.0

    def done(self):
        self.running = False
        self.success = True

    def cancel(self):
        self.running = False
        self.success = False

    def update(self, progress):
        self.progress = progress

qmlRegisterType(TaskStatusViewModel)


class TaskListModel(ListModelFor(TaskStatusViewModel)):

    ''' View model for a list of running tasks '''

    summary = notifyableProperty(TaskStatusViewModel)

    def __init__(self):
        super().__init__()
        self.summary = TaskStatusViewModel()

    def __updateSummary(self):
        if len(self._items) == 1:
            only = self._items[0]
            self.summary.text = only.text
            self.summary.indefinite = only.indefinite
            self.summary.progress = only.progress
        else:
            self.summary.text = QCoreApplication.translate('TaskListModel', '{} tasks'.format(len(self._items)))
            self.summary.indefinite = True

        self.summary.running = len(self._items) > 0

    def __bubbleChangeEvents(self, item):
        idx = self._items.index(item)

        def emitDataChanged():
            self.dataChanged.emit(self.index(idx), self.index(idx))
            self.__updateSummary()

        item.running_changed.connect(emitDataChanged)
        item.text_changed.connect(emitDataChanged)
        item.indefinite_changed.connect(emitDataChanged)
        item.progress_changed.connect(emitDataChanged)
        item.success_changed.connect(emitDataChanged)

    def append(self, item):
        super().append(item)

        def onRunningChanged(running):
            if not running:
                item.running_changed.disconnect(onRunningChanged)
                self.remove(item)

        item.running_changed.connect(onRunningChanged)
        self.__bubbleChangeEvents(item)
        self.__updateSummary()

    def remove(self, item):
        super().remove(item)
        self.__updateSummary()

qmlRegisterType(TaskListModel)


class MainWindowViewModel(NotifyablePropertyObject):
    label = notifyableProperty(str)
    registeredViews = notifyableProperty(QVariant)
    currentView = notifyableProperty(str)
    taskList = notifyableProperty(TaskListModel)
    taskSummary = notifyableProperty(TaskStatusViewModel)

    switchView = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = settings.VERSION
        self.registeredViews = list()
        self.currentView = None
        self.taskList = TaskListModel()

        # This is a workaround for QT nested view model problem.
        # Other option would be to wire up property change signals
        # to all emit also an 'object' signal but that's more code and seems lest robust
        self.taskSummary = self.taskList.summary


class LoginViewModel(NotifyablePropertyObject):
    user = notifyableProperty(str)
    password = notifyableProperty(str)
    remember = notifyableProperty(bool)
    loggedin = notifyableProperty(bool)
    panelVisible = notifyableProperty(bool)

    login = pyqtSignal(str, str, bool)
    logout = pyqtSignal()

    def __init__(self, app, client, user=None, password=None, remember=None, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.login.connect(self.onLogin)
        self.logout.connect(self.onLogout)

        self.app = app
        self.client = client
        self.user = user
        self.password = password
        self.remember = remember or False
        self.loggedin = False
        self.panelVisible = False

    @asyncSlot
    def autologin(self):
        try:
            self.log.info('logging in (auto)...')
            with self.app.report(QCoreApplication.translate('LoginViewModel', 'logging in')):
                self.loggedin = yield from self.client.login(self.user, self.password)

            self.log.debug('autologin result: {}'.format(self.loggedin))
        except Exception as e:
            self.log.error('autologin failed. {}'.format(e))

    @asyncSlot
    @pyqtSlot(str, str, bool)
    def onLogin(self, user, password, remember):
        try:
            self.log.info('logging in...')
            with self.app.report(QCoreApplication.translate('LoginViewModel', 'logging in')):

                import hashlib
                pass_hash = hashlib.sha256(password.encode()).hexdigest()

                self.loggedin = yield from self.client.login(user, pass_hash)
                self.panelVisible = not self.loggedin

                self.storeCredentials(user, pass_hash, remember)

            self.log.debug('login successful? {}'.format(self.loggedin))
        except Exception as ex:
            self.log.warn('login failed: {}'.format(ex))

    @asyncSlot
    @pyqtSlot()
    def onLogout(self):
        try:
            self.log.info('logging out...')
            with self.app.report(QCoreApplication.translate('LoginViewModel', 'logging out')):
                self.loggedin = not (yield from self.client.logout(self.user))

            self.log.debug('logout successful? {}'.format(not self.loggedin))
        except Exception as ex:
            self.log.warn('logout failed: {}'.format(ex))

    def storeCredentials(self, user, password, remember):
        s = settings.get()
        s.beginGroup('login')

        s.setValue('user', user)
        s.setValue('password', password)
        s.setValue('remember', remember)

        s.endGroup()

    def readCredentials(self):
        stored = settings.get()
        stored.beginGroup('login')

        self.user = stored.value('user')
        self.password = stored.value('password')
        self.remember = stored.value('remember') == 'true'

        stored.endGroup()
