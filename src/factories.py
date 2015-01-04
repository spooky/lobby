import logging
import os.path
from PyQt5.QtCore import QUrl

from models import Map
from utils.lua import Parser


def run_chain(handlers, *args, **kwargs):
    for h in handlers:
        result = h(*args, **kwargs)
        if result:
            return result


def create_local_map(code, path):
    log = logging.getLogger(__name__)

    def preview(code, path):
        if os.path.exists(os.path.join(path, code + '.png')):
            return QUrl.fromLocalFile(os.path.join(path, code + '.png'))

    def preview_small(code, path):
        if os.path.exists(os.path.join(path, code + '.small.png')):
            return QUrl.fromLocalFile(os.path.join(path, code + '.small.png'))

    def preview_large(code, path):
        if os.path.exists(os.path.join(path, code + '.large.png')):
            return QUrl.fromLocalFile(os.path.join(path, code + '.large.png'))

    small = run_chain([preview_small, preview], code, path)
    big = run_chain([preview_large], code, path)

    path = os.path.join(path, '{}_scenario.lua'.format(code))
    log.debug('Parsing map file: {}'.format(path))
    lua_parser = Parser(path)
    search = {'scenarioinfo>name': 'name', 'description': 'description', 'map_version': 'version', 'armies': 'slots', 'size': 'size'}
    defaults = {'name': None, 'description': None, 'version': None, 'slots': 0, 'size': {'0': '0', '1': '0'}}

    map_info = lua_parser.parse(search, defaults)
    map_info['size'] = [map_info['size']['0'], map_info['size']['1']]
    map_info['slots'] = len(map_info['slots'])
    map_info['preview_small'] = small
    map_info['preview_big'] = big
    log.debug('Map info: {}'.format(map_info))

    return Map(code, **map_info)
