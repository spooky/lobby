import os

# These directories are in Appdata (e.g. C:\ProgramData on some Win7 versions)
if os.name == 'nt':
    APPDATA_DIR = os.path.join(os.environ['ALLUSERSPROFILE'], 'FAForever')
else:
    APPDATA_DIR = os.path.join(os.environ['HOME'], '.FAForever')

LOBBY_HOST = 'faforever.tk'
LOBBY_PORT = 8080
BIN_DIR = os.path.join(APPDATA_DIR, 'bin')
LOG_DIR = os.path.join(APPDATA_DIR, 'logs')
LOG_FILE_GAME = os.path.join(LOG_DIR, 'game.log')
LOG_FILE_REPLAY = os.path.join(LOG_DIR, 'replay.log')
GAME_PORT_DEFAULT = 6112

AUTH_SERVICE_URL = "http://faforever.tk:44343/auth"

from .GameConnection import *
from .GameSession import *
from .LobbyServerContext import *
from .WebSocket import *
from .AuthService import *

# __all__ = (GameConnection.__all__ +
#            GameSession.__all__ +
#            LobbyServerContext.__all__ +
#            WebSocket.__all__)
