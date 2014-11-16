
from session.IRESTService import IRESTService

from client import USER_SERVICE_URL

class UserService(IRESTService):
    @staticmethod
    def Info(id_or_name):
        if isinstance(id_or_name, int):
            return IRESTService._get(USER_SERVICE_URL + "/%d/info" % id_or_name)
        else:
            assert isinstance(id_or_name, str)
            return IRESTService._get(USER_SERVICE_URL + "/infobyname/%s" % id_or_name)

import logging
logger = logging.getLogger(__name__)

from PyQt5.QtCore import *

class Avatar:
    def __init__(self, name, tooltip, url):
        self.name = name
        self.tooltip = tooltip
        self.url = url

class League:
    def __init__(self, league, division):
        self.league = league
        self.division = division

class Rating:
    def __init__(self, mean, deviation):
        self.mean = mean
        self.deviation = deviation

    def readable(self):
        '''
        :return: Human readable rating (int)
        '''
        return max(0, int(round(self.mean - 3*self.deviation, -2)))

class UserInfo(QObject):

    updated = pyqtSignal(object)

    def __init__(self, id_or_name):
        super(UserInfo, self).__init__()

        if isinstance(id_or_name, int):
            self.id = id_or_name
            self.username = None
        else:
            assert isinstance(id_or_name, str)
            self.id = None
            self.username = id_or_name

        self.avatar = None
        self.clan = None
        self.country = None
        self.league = None
        self.rating = None

    def update(self):
        id_or_name = self.id if self.id else self.username

        def _onError(resp):
            logger.warning('Failed to get info for user "%s": %s', id_or_name, resp["statusMessage"])

            del self._reply

        def _onSuccess(resp):

            if not self.id:
                self.id = resp["id"]

            if not self.username:
                self.username = resp['username']
            elif resp['username'] != self.username:
                # Username changed.
                self.username = resp['username']

            for attr in ['clan', 'country']:
                self.__dict__[attr] = resp[attr]

            self.avatar = Avatar(resp['avatar']['name'], resp['avatar']['tooltip'],
                                 resp['avatar']['url'])
            self.league = League(resp['league']['league'], resp['league']['division'])
            self.rating = Rating(resp['rating']['mean'], resp['rating']['deviation'])

            self.updated.emit(self)
            del self._reply

        self._reply = UserService.Info(id_or_name)

        self._reply.error.connect(_onError)
        self._reply.done.connect(_onSuccess)
