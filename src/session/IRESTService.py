import json

from PyQt5.QtCore import QObject, QUrl, pyqtSignal
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager

# from client import networkAccessManager
networkAccessManager = QNetworkAccessManager()


class RESTResponse(QObject):

    error = pyqtSignal(dict)
    done = pyqtSignal(dict)

    def __init__(self, reply):
        super(RESTResponse, self).__init__()

        self.reply = reply
        reply.finished.connect(self._onFinished)

    def _onFinished(self):
        resData = bytes(self.reply.readAll()).decode()
        if self.reply.error():
            if len(resData) == 0:
                self.error.emit({'statusMessage': self.reply.errorString()})
            else:
                try:
                    self.error.emit(json.loads(resData))
                except ValueError:  # Non-json response -> Internal vibe.d error
                    self.error.emit({'statusMessage': resData})

        else:
            try:
                self.done.emit(json.loads(resData))
            except ValueError:  # Non-json response -> Internal vibe.d error
                self.error.emit({'statusMessage': resData})


class IRESTService:

    @staticmethod
    def _get(url):
        req = QNetworkRequest(QUrl(url))
        return RESTResponse(networkAccessManager.get(req))

    @staticmethod
    def _post(url, postData):
        req = QNetworkRequest(QUrl(url))
        req.setHeader(QNetworkRequest.ContentTypeHeader, 'application/json')

        return RESTResponse(networkAccessManager.post(req, json.dumps(postData).encode()))
