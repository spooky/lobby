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
from utils.async import asyncSlot
from view_models.chrome import MainWindowViewModel, LoginViewModel, TaskStatusViewModel


class Application(QGuiApplication):
    logChanged = pyqtSignal(str)
    initComplete = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.setWindowIcon(QIcon('views/icons/faf.ico'))
        except AttributeError:  # setWindowIcon is available on windows only
            pass

        self.mapLookup = {}
        self.modLookup = {}

    @asyncio.coroutine
    def __initMapLookup(self):
        local = yield from factories.localMapLookup(settings.getMapDirs())
        self.mapLookup.update(local)

    @asyncio.coroutine
    def __initModLookup(self):
        local = yield from factories.localModLookup(settings.getModDirs())
        self.modLookup.update(local)

    @asyncio.coroutine
    def __queueTask(self, asyncCoroutine, text='', indefinite=True, progress=0.0, running=False):
        with self.report(text, indefinite, progress, running):
            yield from asyncCoroutine()

    @asyncSlot
    def start(self):
        logger = logging.getLogger(__name__)
        try:
            self.mainWindow = MainWindow(self)
            self.mainWindow.show()
        except Exception as e:
            logger.critical('error during init: {}'.format(e))
            self.quit()
        else:
            try:
                logger.info('loading maps')
                yield from self.__queueTask(self.__initMapLookup, QCoreApplication.translate('Application', 'loading maps'))
                logger.info('loading mods')
                yield from self.__queueTask(self.__initModLookup, QCoreApplication.translate('Application', 'loading mods'))
            except Exception as e:
                logger.error(e)
        finally:
            logger.debug('init complete')
            self.initComplete.emit()

    # Required for QtHandler to propagate log messages to client 'console'
    def log(self, msg):
        self.logChanged.emit(msg)

    def report(self, text='', indefinite=True, progress=0.0, running=False):
        status = TaskStatusViewModel(text, indefinite, progress, running)
        self.mainWindow.windowModel.taskList.append(status)
        return status


class MainWindow(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.app = Application.instance()

        self.windowModel = MainWindowViewModel(parent=self)
        self.windowModel.switchView.connect(self._onSwitchView)

        self.loginModel = LoginViewModel(self.app, parent=self)
        self.loginModel.readCredentials()
        self.loginModel.panelVisible = not self.loginModel.remember
        if self.loginModel.remember:
            self.loginModel.autologin()

        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty('windowModel', self.windowModel)
        self.engine.rootContext().setContextProperty('loginModel', self.loginModel)
        self.engine.quit.connect(parent.quit)
        self.engine.load(QUrl.fromLocalFile('views/Chrome.qml'))

        self.viewManager = ViewManager(self.engine.rootContext(), self.windowModel, parent=self)
        first = self._registerViews(settings.MODULES, self.app)
        self.viewManager.loadView(first)

        self.window = self.engine.rootObjects()[0]

        # wire up logging console
        self.console = self.window.findChild(QQuickItem, 'console')
        parent.logChanged.connect(self._onLogChanged)

    def show(self):
        if not self.windowModel.currentView:
            raise Exception('currentView not set')

        self.window.show()
        self.log.debug('client up')

    def _registerViews(self, views, app):
        for view in views:
            self.viewManager.registerView(view)

        # TODO need nicer solution - would be nice if the list was notifyable
        self.windowModel.registeredViews = list(self.viewManager.views)

        return views[0]

    @pyqtSlot(str)
    def _onSwitchView(self, name):
        self.viewManager.loadView(name)

    @pyqtSlot(str)
    def _onLogChanged(self, msg):
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

    def registerView(self, name, *args, **kwargs):
        '''
        Works on a convention. The view requires 2 thins:
        1) the ui file which should be the camel cased .qml file in the ui directory. Path should be relative to Chrome.qml
        2) the view model which should be a class in the view_models module
        '''
        if self._views.get(name):
            raise Exception('{} already registered'.format(name))

        n = self._convertName(name)
        vm_name = '{}ViewModel'.format(n)
        # equivalent of from <name>.view_models import <vm_name>
        vm = __import__(name + '.view_models', globals(), locals(), [vm_name], 0)
        self._views[name] = (n, (getattr(vm, vm_name))(*args, parent=self, **kwargs))

    def getView(self, name):
        return self._views[name]

    def loadView(self, name):
        viewName, viewModel = self.getView(name)
        self._context.setContextProperty('contentModel', viewModel)
        self._window.currentView = os.path.join('..', name, 'views', viewName)

    @property
    def views(self):
        return self._views

    def _convertName(self, name):
        return re.sub('([_\s]?)([A-Z]?[a-z]+)', lambda m: m.group(2).title(), name)
