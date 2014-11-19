import logging
from widgets import Application


class QtHandler(logging.Handler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = Application.instance()

    def emit(self, record):
        self.app.log(self.format(record))
