
from PyQt5.QtCore import *

from ws4py.client.threadedclient import WebSocketClient

class WebSocket(QThread, WebSocketClient):
    def __init__(self, socket_addr, parent=None):
        super(WebSocket, self).__init__(parent)

        self._ws = WebSocketClient(socket_addr)

    def run(self):
        self._ws.connect()
        self._ws.run_forever()

    def stop(self):
        self._ws.close()
        self.wait()

    # WebSockedClient callbacks
    def opened(self):
        pass

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        pass