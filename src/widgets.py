import logging
import re
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQuick import QQuickItem

import settings
from utils.async import async_slot
from view_models.chrome import MainWindowViewModel, LoginViewModel
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

        self.windowModel = MainWindowViewModel(parent=self)

        self.loginModel = LoginViewModel(self.client, self.user, self.password, self.remember, parent=self)
        self.loginModel.panel_visible = not self.remember

        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty('windowModel', self.windowModel)
        self.engine.rootContext().setContextProperty('loginModel', self.loginModel)
        self.engine.quit.connect(parent.quit)
        self.engine.load(QUrl.fromLocalFile('ui/Chrome.qml'))

        self.view_manager = ViewManager(self.engine.rootContext(), self.windowModel, parent=self)
        self.window = self.engine.rootObjects()[0]

        # wire up logging console
        self.console = self.window.findChild(QQuickItem, 'console')
        parent.log_changed.connect(self._log)

        # set content view
        self.view_manager.load_view('games', self.client.server_context)

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


class ViewManager(QObject):

    def __init__(self, context, windowViewModeModel, parent=None):
        super().__init__(parent)
        self._context = context
        self._window = windowViewModeModel
        self._cache = dict()

    def get_view(self, name, *args, **kwargs):
        '''
        Works on a convention. The view requires 2 thins:
        1) the ui file which should be the camel cased .qml file in the ui directory. Path should be relative to Chrome.qml
        2) the view model which should be a class in the view_models module
        '''

        if name not in self._cache:
            n = self._convert_name(name)
            vm_name = '{}ViewModel'.format(n)
            # equivalent of from view_models import <part>
            vm = __import__('view_models.'+name, globals(), locals(), [vm_name], 0)
            self._cache[name] = ('{}.qml'.format(n), (getattr(vm, vm_name))(*args, parent=self, **kwargs))

        return self._cache[name]

    def load_view(self, name, *args, **kwargs):
        view_path, view_model = self.get_view(name, *args, **kwargs)
        self._window.currentView = view_path
        self._context.setContextProperty('contentModel', view_model)

    def _convert_name(self, name):
        return re.sub('([_\s]?)([A-Z]?[a-z]+)', lambda m: m.group(2).title(), name)
