import logging
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QVariant, QCoreApplication
from PyQt5.QtQml import qmlRegisterType

import settings
from utils.async import async_slot
from .adapters import NotifyablePropertyObject, ListModelFor, notifyableProperty


class TaskStatusViewModel(NotifyablePropertyObject):

    ''' View model for reporting a running task '''

    running = notifyableProperty(bool)
    text = notifyableProperty(str)
    indefinite = notifyableProperty(bool)
    progress = notifyableProperty(float)
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
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

    def _update_summary(self):
        if len(self._items) == 1:
            only = self._items[0]
            self.summary.text = only.text
            self.summary.indefinite = only.indefinite
            self.summary.progress = only.progress
        else:
            self.summary.text = QCoreApplication.translate('TaskListModel', '{} tasks'.format(len(self._items)))
            self.summary.indefinite = True

        self.summary.running = len(self._items) > 0

    def append(self, item):
        super().append(item)

        def on_running_changed(running):
            if not running:
                item.running_changed.disconnect(on_running_changed)
                self.remove(item)

        item.running_changed.connect(on_running_changed)

        self._update_summary()

    def remove(self, item):
        super().remove(item)
        self._update_summary()

qmlRegisterType(TaskListModel)


class MainWindowViewModel(NotifyablePropertyObject):
    label = notifyableProperty(str)
    registeredViews = notifyableProperty(QVariant)
    currentView = notifyableProperty(str)
    task_list = notifyableProperty(TaskListModel)
    task_summary = notifyableProperty(TaskStatusViewModel)

    switchView = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = settings.VERSION
        self.registeredViews = list()
        self.currentView = None
        self.task_list = TaskListModel()

        # This is a workaround for QT nested view model problem.
        # Other option would be to wire up property change signals
        # to all emit also an 'object' signal but that's more code and seems lest robust
        self.task_summary = self.task_list.summary


class LoginViewModel(NotifyablePropertyObject):
    user = notifyableProperty(str)
    password = notifyableProperty(str)
    remember = notifyableProperty(bool)
    logged_in = notifyableProperty(bool)
    panel_visible = notifyableProperty(bool)

    login = pyqtSignal(str, str, bool)
    logout = pyqtSignal()

    def __init__(self, app, client, user=None, password=None, remember=None, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.login.connect(self.on_login)
        self.logout.connect(self.on_logout)

        self.app = app
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
            with self.app.report(QCoreApplication.translate('LoginViewModel', 'logging in')):
                self.logged_in = yield from self.client.login(self.user, self.password)

            self.log.debug('autologin result: {}'.format(self.logged_in))
        except Exception as e:
            self.log.error('autologin failed. {}'.format(e))

    @async_slot
    @pyqtSlot(str, str, bool)
    def on_login(self, user, password, remember):
        try:
            self.log.info('logging in...')
            with self.app.report(QCoreApplication.translate('LoginViewModel', 'logging in')):

                import hashlib
                pass_hash = hashlib.sha256(password.encode()).hexdigest()

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
            with self.app.report(QCoreApplication.translate('LoginViewModel', 'logging out')):
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
