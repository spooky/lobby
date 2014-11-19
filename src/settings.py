import os
from PyQt5.QtCore import QSettings

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

ORGANIZATION_NAME = 'Forged Alliance Forever'
APPLICATION_NAME = 'lobby'

# Service URLs
AUTH_SERVICE_URL = 'http://{}:44343/auth'.format(LOBBY_HOST)
FAF_SERVICE_URL = 'http://{}:8080'.format(LOBBY_HOST)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'faf_console': {
            'class': 'utils.logging.QtHandler',
            'level': 'DEBUG',
            'formatter': 'simple'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'faf_console']
    }
}


def init(app):
    # required for settings persistance
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setOrganizationDomain(LOBBY_HOST)
    app.setApplicationName(APPLICATION_NAME)


def get():
    return QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
