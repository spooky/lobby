import logging
import os
import re
import asyncio
from collections import OrderedDict
from PyQt5.QtCore import QObject, QCoreApplication, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQuick import QQuickItem

import settings
import factories
import relays.auth
from utils.async import async_slot
from view_models.chrome import MainWindowViewModel, LoginViewModel

# TODO: clean up/utilize the relative imports in qml files


class Application(QGuiApplication):
    log_changed = pyqtSignal(str)
    init_complete = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.setWindowIcon(QIcon('ui/icons/faf.ico'))
        except AttributeError:  # setWindowIcon is available on windows only
            pass

        self.session = None
        self.map_lookup = {}
        self.mod_lookup = {}

    @asyncio.coroutine
    def __init_map_lookup(self):
        local = yield from factories.local_map_lookup(settings.get_map_dirs())
        self.map_lookup.update(local)

    @asyncio.coroutine
    def __init_mod_lookup(self):
        local = yield from factories.local_mod_lookup(settings.get_mod_dirs())
        self.mod_lookup.update(local)

    @async_slot
    def start(self):
        logger = logging.getLogger(__name__)
        try:
            self.mainWindow = MainWindow(self)
            self.mainWindow.show()
        except Exception as e:
            logger.critical('Error during init: {}'.format(e))
            self.quit()
        else:
            self.report_indefinite(QCoreApplication.translate('Application', 'loading maps'))
            yield from self.__init_map_lookup()
            self.report_indefinite(QCoreApplication.translate('Application', 'loading mods'))
            yield from self.__init_mod_lookup()
        finally:
            logger.debug('Init complete')
            self.init_complete.emit()
            self.end_report()

    # Required for QtHandler to propagate log messages to client 'console'
    def log(self, msg):
        self.log_changed.emit(msg)

    def report(self, msg, progress=0.0):
        self.mainWindow.windowModel.setTaskStatus(msg, progress, False)

    def report_indefinite(self, msg):
        self.mainWindow.windowModel.setTaskStatus(msg, indefinite=True)

    def end_report(self):
        self.mainWindow.windowModel.clearTaskStatus()


class MainWindow(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        app = Application.instance()

        self.windowModel = MainWindowViewModel(parent=self)
        self.windowModel.switchView.connect(self._on_switchView)

        self.loginModel = LoginViewModel(relays.auth.create_auth_client(), parent=self)
        self.loginModel.read_credentials()
        self.loginModel.panel_visible = not self.loginModel.remember
        if self.loginModel.remember:
            self.loginModel.autologin()

        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty('windowModel', self.windowModel)
        self.engine.rootContext().setContextProperty('loginModel', self.loginModel)
        self.engine.quit.connect(parent.quit)
        self.engine.load(QUrl.fromLocalFile('ui/Chrome.qml'))

        self.view_manager = ViewManager(self.engine.rootContext(), self.windowModel, parent=self)
        first = self._register_views(settings.MODULES, app)
        self.view_manager.load_view(first)

        self.window = self.engine.rootObjects()[0]

        # wire up logging console
        self.console = self.window.findChild(QQuickItem, 'console')
        parent.log_changed.connect(self._on_log_changed)

    def show(self):
        if not self.windowModel.currentView:
            raise Exception('currentView not set')

        self.window.show()
        self.log.debug('Client up')

    def _register_views(self, views, app):
        for view in views:
            self.view_manager.register_view(view)

        # TODO need nicer solution - would be nice if the list was notifyable
        self.windowModel.registeredViews = list(self.view_manager.get_views())

        return views[0]

    @pyqtSlot(str)
    def _on_switchView(self, name):
        self.view_manager.load_view(name)

    @pyqtSlot(str)
    def _on_log_changed(self, msg):
        # replace with collections.deque binding(ish)?
        if self.console.property('lineCount') == settings.LOG_BUFFER_SIZE:
            line_end = self.console.property('text').find('\n') + 1
            self.console.remove(0, line_end)

        self.console.append(msg)


class ViewManager(QObject):

    def __init__(self, context, windowViewModel, parent=None):
        super().__init__(parent)
        self._context = context
        self._window = windowViewModel
        self._views = OrderedDict()

    def register_view(self, name, *args, **kwargs):
        '''
        Works on a convention. The view requires 2 thins:
        1) the ui file which should be the camel cased .qml file in the ui directory. Path should be relative to Chrome.qml
        2) the view model which should be a class in the view_models module
        '''
        if self._views.get(name):
            raise Exception('{} already registered'.format(name))

        n = self._convert_name(name)
        vm_name = '{}ViewModel'.format(n)
        # equivalent of from <name>.view_models import <vm_name>
        vm = __import__(name+'.view_models', globals(), locals(), [vm_name], 0)
        self._views[name] = (n, (getattr(vm, vm_name))(*args, parent=self, **kwargs))

    def get_view(self, name):
        return self._views[name]

    def load_view(self, name):
        view_name, view_model = self.get_view(name)
        self._context.setContextProperty('contentModel', view_model)
        self._window.currentView = os.path.join('..', name, 'views', view_name)

    def get_views(self):
        return self._views

    def _convert_name(self, name):
        return re.sub('([_\s]?)([A-Z]?[a-z]+)', lambda m: m.group(2).title(), name)
