import logging
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQuick import QQuickItem

import settings
from utils.async import async_slot
from view_models import MainWindowViewModel, LoginViewModel, GamesViewModel
from session.Client import Client


LOG_BUFFER_SIZE = 1000


class Application(QGuiApplication):
    log_changed = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.setWindowIcon(QIcon('ui/icons/faf.ico'))
        except AttributeError:
            pass
        self.session = None

    def start(self):
        self.mainWindow = MainWindow(self)
        self.mainWindow.show()

    def log(self, msg):
        self.log_changed.emit(msg)


class MainWindow(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)
        self._read_settings()

        self.client = Client(app=Application.instance(), parent=self)

        if self.remember:
            self._autologin()

        self.model = MainWindowViewModel(parent=self)

        self.loginModel = LoginViewModel(self.client, self.user, self.password, self.remember, parent=self)
        self.loginModel.panel_visible = not self.remember

        self.gamesModel = GamesViewModel(self.client.server_context, parent=self)

        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty('windowModel', self.model)
        self.engine.rootContext().setContextProperty('loginModel', self.loginModel)
        self.engine.rootContext().setContextProperty('contentModel', self.gamesModel)
        self.engine.quit.connect(parent.quit)
        self.engine.load(QUrl.fromLocalFile('ui/Chrome.qml'))

        self.window = self.engine.rootObjects()[0]

        # wire up logging console
        self.console = self.window.findChild(QQuickItem, 'console')
        parent.log_changed.connect(self._log)

    def show(self):
        self.window.show()

    def _read_settings(self):
        stored = settings.get()
        stored.beginGroup('login')

        self.user = stored.value('user')
        self.password = stored.value('password')
        self.remember = stored.value('remember') == 'true'

        stored.endGroup()

    @async_slot
    def _autologin(self):
        try:
            self.log.info('logging in (auto)...')
            self.loginModel.logged_in = yield from self.client.login(self.user, self.password)
            self.log.debug('autologin result: {}'.format(self.loginModel.logged_in))
        except Exception as e:
            self.log.error('autologin failed. {}'.format(e))

    @pyqtSlot(str)
    def _log(self, msg):
        # replace with collections.deque binding(ish)?
        if self.console.property('lineCount') == LOG_BUFFER_SIZE:
            line_end = self.console.property('text').find('\n') + 1
            self.console.remove(0, line_end)

        self.console.append(msg)
