import logging
import os.path
from PyQt5.QtCore import QUrl

from models import Map, Mod
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

    scenario = os.path.join(path, '{}_scenario.lua'.format(code))
    log.debug('Parsing map file: {}'.format(scenario))
    lua_parser = Parser(scenario)
    search = {'scenarioinfo>name': 'name', 'description': 'description', 'map_version': 'version', 'armies': 'slots', 'size': 'size'}
    defaults = {'name': None, 'description': None, 'version': None, 'slots': 0, 'size': {'0': '0', '1': '0'}}

    map_info = lua_parser.parse(search, defaults)
    map_info['size'] = [map_info['size']['0'], map_info['size']['1']]
    map_info['slots'] = len(map_info['slots'])
    map_info['preview_small'] = small
    map_info['preview_big'] = big
    log.debug('Map info: {}'.format(map_info))

    return Map(code, **map_info)


def create_local_mod(name, path):
    log = logging.getLogger(__name__)

    def icon(file_name, path):
        if os.path.exists(os.path.join(path, file_name)):
            return QUrl.fromLocalFile(os.path.join(path, file_name))

    info = os.path.join(path, 'mod_info.lua')
    log.debug('Parsing mod file: {}'.format(info))

    lua_parser = Parser(info)
    search = {'uid': 'uid', 'name': 'name', 'description': 'description', 'author': 'author',
              'version': 'version', 'icon': 'icon', 'ui_only': 'ui_only', 'conflicts': 'conflicts'}
    defaults = {'uid': None, 'name': None, 'description': None, 'author': None, 'version': None, 'icon': None, 'ui_only': False, 'conflicts': {}}

    mod_info = lua_parser.parse(search, defaults)
    mod_info['conflicts'] = list(mod_info['conflicts'].values())
    mod_info['icon'] = icon(mod_info['icon'].split('/').pop(), path)
    mod_info['ui_only'] = mod_info['ui_only'] == 'true'
    log.debug('Mon info: {}'.format(mod_info))

    return Mod(**mod_info)
