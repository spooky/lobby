import os
from PyQt5.QtCore import QSettings

# These directories are in Appdata (e.g. C:\ProgramData on some Win7 versions)
if os.name == 'nt':
    APPDATA_DIR = os.path.join(os.environ['ALLUSERSPROFILE'], 'FAForever')
else:
    APPDATA_DIR = os.path.join(os.environ['HOME'], '.FAForever')

# This should be 'My Documents' for most users. However,
# users with accents in their names can't even use these folders in Supcom
# so we are nice and create a new home for them in the APPDATA_DIR
try:
    bytes(os.environ['USERNAME'], 'ascii')  # Try to see if the user has a wacky username

    import ctypes
    from ctypes.wintypes import MAX_PATH

    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        PERSONAL_DIR = (buf.value)
    else:
        raise Exception()
except UnicodeDecodeError:
    PERSONAL_DIR = os.path.join(APPDATA_DIR, 'user')

LOBBY_HOST = 'faforever.tk'
LOBBY_PORT = 8080
GAME_PORT_DEFAULT = 6112
BIN_DIR = os.path.join(APPDATA_DIR, 'bin')
LOG_DIR = os.path.join(APPDATA_DIR, 'logs')
FA_DIR = ''
LOG_FILE_GAME = os.path.join(LOG_DIR, 'game.log')
LOG_FILE_REPLAY = os.path.join(LOG_DIR, 'replay.log')

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

    global FA_DIR
    FA_DIR = get().value('fa_path') or ''


def get():
    return QSettings(ORGANIZATION_NAME, APPLICATION_NAME)


def get_map_dirs():
    stock = os.path.join(FA_DIR, 'maps')
    downloaded = os.path.join(PERSONAL_DIR, 'My Games', 'Gas Powered Games', 'Supreme Commander Forged Alliance', 'Maps')

    return [stock, downloaded]


def get_mod_dirs():
    stock = os.path.join(FA_DIR, 'mods')
    downloaded = os.path.join(PERSONAL_DIR, 'My Games', 'Gas Powered Games', 'Supreme Commander Forged Alliance', 'Mods')

    return [stock, downloaded]
