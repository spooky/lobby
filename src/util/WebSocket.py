
import logging
logger = logging.getLogger(__name__)

#####################################################
## EXIMIUS WALL
#####################################################

# Don't touch anything. It works.

import json
import socket
import errno

from PyQt5.QtCore import *

import thread
from Queue import Queue, Empty

from ws4py.client import WebSocketBaseClient
from ws4py.messaging import PongControlMessage

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
        logger.debug("Send: %s", message)

        self.w_queue.put(message.encode())

    def run(self):

        QTimer.singleShot(0, self._reconnect)

        self.exec_()

        self._ws.close()

    def _reconnect(self):
        logger.info("Reconnecting to %s...", self.addr)

        self._ws = WebSocketBaseClient(self.addr)

        self._ws.closed = self.closed
        self._ws.received_message = self.received_message

        self._ws.handshake_ok = lambda: None

        try:
            self._ws.connect()
            self._ws.sock.setblocking(0)

            logger.info("Connected to %s.", self.addr)
            self._socket_connected = True

            self.reconnected.emit()
            thread.start_new_thread(self._write_thread, ())

            self._read_timer = QTimer(self)
            self._read_timer.timeout.connect(self._read_some)
            self._read_timer.start(250)

            self._heartbeat_timer = QTimer(self)
            self._heartbeat_timer.timeout.connect(self._heartbeat)
            self._heartbeat_timer.start(10*60*1000)

            self._socket_connected = True
        except socket.error as e:
            logger.debug("Failed to connect to %s", str(e))
            QTimer.singleShot(10*1000, self._reconnect)

    def _heartbeat(self):
        self._ws.send(PongControlMessage(data='beep'))

    def _read_some(self):
        try:
            while True:
                data = self._ws.sock.recv(1024)
                self._ws.process(data)

        except socket.error as e:
            if e.errno == errno.EAGAIN: # Non-blocking op
                return
            else:
                raise


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
        logger.info("Closed WebSocket to %s: %s, %s", self.addr, code, reason)

        self._socket_connected = False

        QTimer.singleShot(500, self._reconnect)

    def received_message(self, m_):
        logger.info("Recv: %s", m_)

        self.messageReceived.emit(str(m_))