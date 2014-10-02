import struct
import json
from datetime import datetime
import logging

from PyQt5.QtCore import *

from PyQt5.QtNetwork import *

logger = logging.getLogger(__name__)

PROTOCOL_VERSION = 0

STATE_HANDSHAKE = 0
STATE_LOGIN = 1
STATE_LOBBY = 2

class ProtocolError(Exception):
    def __init__(self, message):
        super(ProtocolError, self).__init__(message)


class LobbyServerContext(QObject):
    messageReceived = pyqtSignal(str, dict)
    loggedIn = pyqtSignal()

    @pyqtSlot(str, dict)
    def sendMessage(self, command_id, message):

        assert isinstance(command_id, basestring)

        logger.info("Send: %s : %s", command_id, message)

        self._send(command_id, message)

    def __init__(self):
        super(LobbyServerContext, self).__init__()

        self.socket = QTcpSocket()
        self.state = STATE_HANDSHAKE

        self.socket.readyRead.connect(self._onReadyRead)
        self.socket.error.connect(self._onError)
        self.socket.disconnected.connect(self._onDisconnected)

    def connectToHost(self, host, port):
        self.socket.connectToHost(host, port)

        self.sendMessage('handshake', {'server_address': host, 'protocol_version': 0})

    def login(self, username, session_id):
        self.socket.waitForConnected(5000)
        if self.socket.state() != QTcpSocket.ConnectedState and not self.socket.isValid():
            raise ProtocolError("FAF Connection timed out.")

        self.sendMessage('login', {'username': username, 'session_id': session_id})

    def _send(self, command_id, message):
        return
        data = json.dumps({'id': command_id, 'data': message}).encode()
        self.socket.write(struct.pack('=l', len(data)))
        self.socket.write(data)

    def _onMessage(self, command_id, message):

        logger.debug('Recv: %s : %s', command_id, message)

        if self.state == STATE_HANDSHAKE:
            if command_id != 'handshake_resp':
                raise ProtocolError("Wrong state.")

            if not message['success']:
                raise ProtocolError(message['reason'])

            self.state = STATE_LOGIN
            return

        # Keep Alive
        if command_id == "keep_alive":
            self._send("keep_alive", {'time': datetime.now().isoformat()})
            return

        if self.state == STATE_LOGIN:
            if command_id != 'login_resp':
                raise ProtocolError("Wrong state.")

            if not message['success']:
                # Our session_id should normally succeed
                raise ProtocolError(message['reason'])

            self.loggedIn.emit()
        elif self.state == STATE_LOBBY:
            self.messageReceived.emit(command_id, message)
        else:
            raise ProtocolError("Unknown state.")

    def _onReadyRead(self):
        while self.socket.bytesAvailable() >= 4:
            size, = struct.unpack('=l', self.socket.peek(4))

            if self.socket.bytesAvailable() < size + 4:
                return

            self.socket.read(4)
            msg = json.loads(self.socket.read(size).decode())

            self._onMessage(msg['id'], msg['data'])

    def _onError(self):
        logger.warning("Error with lobby socket: %s.", self.socket.errorString())
        pass

    def _onDisconnected(self):
        logger.info("Disconnected from server.")