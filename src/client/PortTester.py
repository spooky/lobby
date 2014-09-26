import logging

from PyQt4.QtCore import *

from PyQt4.QtNetwork import *

import util

import fa
from client import LOBBY_HOST

logger = logging.getLogger(__name__)

TEST_PORT = 8002


class PortTester(QThread):
    # Test result structure;
    # { port: %i,
    # success: %b,
    # reason: %s,
    #   alternative_port: %i
    # }
    testDone = pyqtSignal(dict)

    def __init__(self, magic_cookie, localIP, port):
        super(PortTester, self).__init__()

        self.moveToThread(self)
        self.magic_cookie = magic_cookie
        self.localIP = localIP
        self.port = port
        self.useUPnP = util.settings.value("app/upnp", True)

        self.testServer = None

        self.udpSocket = None
        self.timer = None

        self.recv_success = 0

        self.finished.connect(self.deleteLater)

    def _onRead(self):
        if not self.recv_success:
            logger.info("Port %i response from server.", self.udpSocket.localPort())
        self.udpSocket.readDatagram(0)
        self.recv_success += 1

    def sendPkt(self):
        self.udpSocket.writeDatagram(self.magic_cookie, self.testServer, TEST_PORT)

    def finishTest(self):
        self.testResult['success'] = self.recv_success > 2

        success = 'succeeded' if self.testResult['success'] else 'failed'
        logger.info("Port %i test %s.", self.udpSocket.localPort(), success)
        self.testDone.emit(self.testResult)

        self.udpSocket.close()

    def run(self):
        '''
        Here, we test with the server if the current game port set is all right.
        If not, we propose alternatives to the user
        '''
        addrs = QHostInfo.fromName(LOBBY_HOST).addresses()

        # FIXME: Ideally it should find a useable address based on local ip
        for addr in addrs:
            if addr.protocol() == QAbstractSocket.IPv4Protocol:
                self.testServer = addr

        if self.testServer is None:
            raise RuntimeError("Did not find useable ip for port testing.")

        if self.useUPnP:
            fa.upnp.createPortMapping(self.localIP, self.port, "UDP")

        self.testResult = {'port': self.port, 'success': False}

        #binding the port
        self.udpSocket = udpSocket = QUdpSocket(self)
        udpSocket.bind(self.port)
        udpSocket.readyRead.connect(self._onRead)

        if udpSocket.localPort() != self.port:
            logger.warning("The port (%i) is not available." % self.port)
            logger.warning("Testing alternative port (%i)." % udpSocket.localPort())
            self.testResult['alternative_port'] = udpSocket.localPort()

        logger.info("Sending packet to %s:%i from %s:%i",
                    self.testServer.toString(), TEST_PORT,
                    udpSocket.localAddress().toString(), udpSocket.localPort())

        if udpSocket.writeDatagram(self.magic_cookie, self.testServer, TEST_PORT) == -1:
            logger.warning("Unable to send UDP Packet: %s", udpSocket.errorString())
            self.testResult['success'] = False
            self.testResult['reason'] = udpSocket.errorString()
            self.testDone.emit(self.testResult)
            #QMessageBox.critical(self, "UDP Packet not sent !", "We are not able to send a UDP packet. <br><br>Possible reasons:<ul><li><b>Your firewall is blocking the UDP port {port}.</b></li><li><b>Your router is blocking or routing port {port} in a wrong way.</b></li></ul><br><font size='+2'>How to fix this : </font> <ul><li>Check your firewall and router. <b>More info in the wiki (Links -> Wiki)</li></b><li>You should also consider using <b>uPnP (Options -> Settings -> Gameport)</b></li><li>You should ask for assistance in the TechQuestions chat and/or in the <b>technical forum (Links -> Forums<b>)</li></ul><br><font size='+1'><b>FA will not be able to perform correctly until this issue is fixed.</b></font>".format(port=self.gamePort))

        # We can send on the interface, do extensive test
        else:
            self.timer = timer = QTimer(self)
            timer.start(500)

            timer.timeout.connect(self.sendPkt)

            #QTimer.singleShot(5000, timer.deleteLater)
            QTimer.singleShot(5000, self.finishTest)

        self.exec_()