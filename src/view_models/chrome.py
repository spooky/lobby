import logging
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot

from utils.async import async_slot


class MainWindowViewModel(QObject):  # TODO: use MetaClass(ish) model to handle notifyable properties?

    def __init__(self, parent=None):
        super().__init__(parent)

        self._label = 'FA Forever v.dev'

        self._taskRunning = False  # wether to show the task indicator
        self._taskStatusText = None  # text to show while task is running
        self._taskStatusIsIndefinite = True  # wether to hide the progress bar progress bar progress value - makes sense only if taskStatusIsIndefinite == True
        self._taskStatusProgress = 0

        self._currentView = None

    @pyqtProperty(str, constant=True)
    def label(self):
        return self._label

    @label.setter
    def label(self, text):
        self._label = text

    taskRunning_changed = pyqtSignal(bool)

    @pyqtProperty(bool, notify=taskRunning_changed)
    def taskRunning(self):
        return self._taskRunning

    @taskRunning.setter
    def taskRunning(self, value):
        self._taskRunning = value
        self.taskRunning_changed.emit(value)

    taskStatusText_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=taskStatusText_changed)
    def taskStatusText(self):
        return self._taskStatusText

    @taskStatusText.setter
    def taskStatusText(self, value):
        self._taskStatusText = value
        self.taskStatusText_changed.emit(value)

    taskStatusIsIndefinite_changed = pyqtSignal(bool)

    @pyqtProperty(bool, notify=taskStatusIsIndefinite_changed)
    def taskStatusIsIndefinite(self):
        return self._taskStatusIsIndefinite

    @taskStatusIsIndefinite.setter
    def taskStatusIsIndefinite(self, value):
        self._taskStatusIsIndefinite = value
        self.taskStatusIsIndefinite_changed.emit(value)

    taskStatusProgress_changed = pyqtSignal(float)

    @pyqtProperty(float, notify=taskStatusProgress_changed)
    def taskStatusProgress(self):
        return self._taskStatusProgress

    @taskStatusProgress.setter
    def taskStatusProgress(self, value):
        self._taskStatusProgress = value
        self.taskStatusProgress_changed.emit(value)

    def setTaskStatus(self, text, indefinite=True):
        self.taskStatusText = text
        self.taskStatusProgress = 0.0
        self.taskStatusIsIndefinite = indefinite
        self.taskRunning = True

    def clearTaskStatus(self):
        self.taskRunning = False
        self.taskStatusIsIndefinite = True
        self.taskStatusText = None
        self.taskStatusProgress = 0.0

    currentView_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=currentView_changed)
    def currentView(self):
        return self._currentView

    @currentView.setter
    def currentView(self, value):
        self._currentView = value
        self.currentView_changed.emit(value)


class LoginViewModel(QObject):
    login = pyqtSignal(str, str, bool)
    logout = pyqtSignal()

    def __init__(self, client, user, password, remember, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.login.connect(self.on_login)
        self.logout.connect(self.on_logout)
        self.client = client
        self._user = user
        self._password = password
        self._remember = remember
        self._logged_in = False
        self._panel_visible = False

    user_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=user_changed)
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value
        self.user_changed.emit(value)

    password_changed = pyqtSignal(str)

    @pyqtProperty(str, notify=password_changed)
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
        self.password_changed.emit(value)

    remember_changed = pyqtSignal(bool)

    @pyqtProperty(bool, notify=remember_changed)
    def remember(self):
        return self._remember

    @remember.setter
    def remember(self, value):
        self._remember = value
        self.remember_changed.emit(value)

    logged_in_changed = pyqtSignal(bool)

    @pyqtProperty(bool, notify=logged_in_changed)
    def logged_in(self):
        return self._logged_in

    @logged_in.setter
    def logged_in(self, value):
        self._logged_in = value
        self.logged_in_changed.emit(value)

    panel_visible_changed = pyqtSignal(bool)

    @pyqtProperty(bool, notify=panel_visible_changed)
    def panel_visible(self):
        return self._panel_visible

    @panel_visible.setter
    def panel_visible(self, value):
        self._panel_visible = value
        self.panel_visible_changed.emit(value)

    @async_slot
    @pyqtSlot(str, str, bool)
    def on_login(self, user, password, remember):
        try:
            import hashlib
            pass_hash = hashlib.sha256(password.encode()).hexdigest()

            self.log.info('logging in...')
            self.logged_in = yield from self.client.login(user, pass_hash)
            self.panel_visible = not self.logged_in

            self._store_credentials(user, pass_hash, remember)

            self.log.debug('login successful? {}'.format(self.logged_in))

        except Exception as ex:
            self.log.warn('login failed: {}'.format(ex))

    @async_slot
    @pyqtSlot()
    def on_logout(self):
        try:
            self.log.info('logging out...')
            self.logged_in = not (yield from self.client.logout())

            self.log.debug('logout successful? {}'.format(not self.logged_in))

        except Exception as ex:
            self.log.warn('logout failed: {}'.format(ex))

    def _store_credentials(self, user, password, remember):
        # TODO: DRY (widgets.MainWindow._read_settings)
        import settings
        s = settings.get()
        s.beginGroup('login')

        s.setValue('user', user)
        s.setValue('password', password)
        s.setValue('remember', remember)

        s.endGroup()
