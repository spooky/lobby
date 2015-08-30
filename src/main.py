import sys
import logging
import logging.config
import asyncio
import settings
from widgets import Application
from quamash import QEventLoop, QThreadExecutor

try:
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
except ImportError:
    pass


def configureLogging():
    try:
        logging.config.dictConfig(settings.LOGGING)
    except:
        from utils.logging import QtHandler
        logging.basicConfig(level=logging.WARNING, handlers=[QtHandler()])


def startApp(callback=None):
    app = Application(sys.argv)
    settings.init(app)

    configureLogging()
    log = logging.getLogger(__name__)
    log.info('starting app')

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    executor = QThreadExecutor(settings.EXECUTOR_THREADS)
    loop.set_default_executor(executor)

    with loop:
        app.start()
        if callback:
            callback(app)
        sys.exit(loop.run_forever())

    return app


def startAlfred(app):
    import alfred.widgets
    helper = alfred.widgets.MainWindow(app)
    helper.show()


if __name__ == '__main__':
    debug = '--debug' in sys.argv
    startApp(startAlfred if debug else None)
