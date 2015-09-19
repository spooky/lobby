import asyncio
import logging
from PyQt5.QtCore import QCoreApplication, pyqtSignal, pyqtSlot

from utils.async import asyncSlot
from widgets import Application
from view_models.adapters import ListModelFor, NotifyablePropertyObject, notifyableProperty

from .models import SampleItem


class SampleListViewModel(ListModelFor(SampleItem)):

    ''' View model for a list of sample items '''

    def __init__(self, parent=None):
        super().__init__()
        self.log = logging.getLogger(__name__)

    def act(self):
        self.log.debug('acting')


class SampleViewModel(NotifyablePropertyObject):
    # properties
    items = notifyableProperty(SampleListViewModel)
    # signals
    doingThings = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logging.getLogger(__name__)

        self.items = SampleListViewModel()

        self.doingThings.connect(self.on_doingThings)

    @asyncSlot
    @pyqtSlot()
    def on_doingThings(self):
        self.log.debug('doing things...')
        with Application.instance().report(QCoreApplication.translate('SampleViewModel', 'doing things')):
            yield from asyncio.sleep(5)
