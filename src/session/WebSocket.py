
import logging
logger = logging.getLogger(__name__)

#####################################################
## EXIMIUS WALL
#####################################################

# Don't touch anything. It works.

from PyQt5.QtCore import QThread, QTimer, pyqtSignal, pyqtSlot

import _thread
from queue import Queue, Empty

from ws4py.client import WebSocketBaseClient
from ws4py.messaging import PingControlMessage


class WebSocket(QThread):

    def __init__(self, socket_addr, parent=None):
        super(WebSocket, self).__init__(parent)

        self.addr = socket_addr
        self.w_queue = Queue()
        self.moveToThread(self)

        self._read_timer = None
        self._socket_connected = False

    # (message)
    messageReceived = pyqtSignal(str)

    reconnected = pyqtSignal()

    @pyqtSlot(str)
    def sendMessage(self, message):
        logger.debug('Send: {}'.format(message))

        self.w_queue.put(message.encode())

    def run(self):

        QTimer.singleShot(0, self._reconnect)

        self.exec_()

        self._ws.close()

    def _reconnect(self):
        logger.info('Reconnecting to {}...'.format(self.addr))

        self._ws = WebSocketBaseClient(self.addr)

        self._ws.closed = self.closed
        self._ws.received_message = self.received_message

        self._ws.handshake_ok = lambda: None

        try:
            self._ws.connect()
            self._ws.sock.setblocking(0)

            logger.info('Connected to {}.'.format(self.addr))
            self._socket_connected = True

            self.reconnected.emit()
            _thread.start_new_thread(self._write_thread, ())

            self._read_timer = QTimer(self)
            self._read_timer.timeout.connect(self._read_some)
            self._read_timer.start(250)

            self._heartbeat_timer = QTimer(self)
            self._heartbeat_timer.timeout.connect(self._heartbeat)
            self._heartbeat_timer.start(30 * 1000)

            self._socket_connected = True
        except OSError as e:
            logger.debug('Failed to connect to {}'.format(e))
            QTimer.singleShot(10 * 1000, self._reconnect)

    def _heartbeat(self):
        self._ws.send(PingControlMessage(data='beep'))

    def _read_some(self):
        try:
            while True:
                data = self._ws.sock.recv(1024)
                if not self._ws.process(data):
                    self._ws.terminate()
                    break
        except BlockingIOError:
            return

    def _write_thread(self):
        while self._socket_connected:
            try:
                msg = self.w_queue.get(timeout=1)

                self._ws.send(msg)

                self.w_queue.task_done()
            except Empty:
                pass

    # WebSocketClient callbacks
    def closed(self, code, reason=None):
        logger.info('Closed WebSocket to {}: {}, {}'.format(self.addr, code, reason))

        self._socket_connected = False
        self._read_timer.stop()
        self._heartbeat_timer.stop()

        QTimer.singleShot(500, self._reconnect)

    def received_message(self, m_):
        logger.debug('Recv: {}'.format(m_))

        self.messageReceived.emit(str(m_))
