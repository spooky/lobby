
import logging
logger = logging.getLogger(__name__)

#####################################################
## EXIMIUS WALL
#####################################################

# Don't touch anything. It works.

import json
import socket

from PyQt5.QtCore import *

import thread
from Queue import Queue, Empty

from ws4py.client.threadedclient import WebSocketClient

class WebSocket(QThread):
    def __init__(self, socket_addr, parent=None):
        super(WebSocket, self).__init__(parent)

        self.addr = socket_addr
        self._ws = WebSocketClient(socket_addr, heartbeat_freq=60*1000)

        self._ws.opened = self.opened
        self._ws.closed = self.closed
        self._ws.received_message = self.received_message

        self.w_queue = Queue()

        self.moveToThread(self)

        self._socket_connected = False

    # subsystem, command_id, args
    messageReceived = pyqtSignal(str, str, dict)

    reconnected = pyqtSignal()

    @pyqtSlot(str, dict)
    def sendMessage(self, command_id, message):
        logger.info("Send: %s : %s", command_id, message)

        self._ws.send(json.dumps({'id': command_id,
                                  'data': message}))
    def run(self):

        QTimer.singleShot(0, self._reconnect)

        self.exec_()

        self._ws.close()

    def _reconnect(self):
        logger.info("%s: Reconnecting...", id(self))

        self._ws = WebSocketClient(self.addr, heartbeat_freq=60*1000)

        self._ws.opened = self.opened
        self._ws.closed = self.closed
        self._ws.received_message = self.received_message

        try:
            self._ws.connect()
            self.reconnected.emit()
        except socket.error as e:
            logger.info("%s: Failed to connect: %s", id(self), str(e))
            QTimer.singleShot(10*1000, self._reconnect)


    def _write_thread(self):
        while self._socket_connected:
            try:
                msg = self.w_queue.get(timeout=1)

                self._ws.send(msg)

                self.w_queue.task_done()
            except Empty:
                pass

    # WebSocketClient callbacks
    def opened(self):
        logger.info("Opened WebSocket %s", id(self))
        self._socket_connected = True

        thread.start_new_thread(self._write_thread, ())
        pass

    def closed(self, code, reason=None):
        logger.info("Closed WebSocket %s : %s, %s", id(self), code, reason)

        self._socket_connected = False

        QTimer.singleShot(500, self._reconnect)

    def received_message(self, m):
        m = json.loads(str(m))

        logger.info("Recv: %s : %s : %s", m['subsystem'], m['id'], m['data'])

        self.messageReceived.emit(m['subsystem'], m['id'], m['data'])