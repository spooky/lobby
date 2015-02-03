# import logging
import asyncio
import os
from PyQt5.QtCore import QUrl

from models import Map, Mod
from utils.lua import Parser


def __run_chain(handlers, *args, **kwargs):
    for h in handlers:
        result = h(*args, **kwargs)
        if result:
            return result


@asyncio.coroutine
def __local_lookup(paths, factory_method):
    dirs = [(n, os.path.join(p, n)) for p in paths for n in os.listdir(p)]
    result = []
    for n, p in dirs:
        item = yield from factory_method(n, p)
        result.append(item)

    return result


@asyncio.coroutine
def local_map_lookup(paths):
    maps = yield from __local_lookup(paths, create_local_map)
    return {m.code: m for m in maps}


@asyncio.coroutine
def create_local_map(code, path):
    # log = logging.getLogger(__name__)

    def preview(code, path, suffix=''):
        file_name = '{}{}.png'.format(code, suffix)

        if os.path.exists(os.path.join(path, file_name)):
            return QUrl.fromLocalFile(os.path.join(path, file_name))

    def preview_small(code, path):
        return preview(code, path, suffix='.small')

    def preview_large(code, path):
        return preview(code, path, suffix='.large')

    small = __run_chain([preview_small, preview], code, path)
    big = __run_chain([preview_large], code, path)

    # strips the screwed up .vXYZ suffix that are sometimes used in map dir names
    dot_index = code.rfind('.')
    stripped_code = code if dot_index < 0 else code[:dot_index]

    scenario = os.path.join(path, '{}_scenario.lua'.format(stripped_code))
    # log.debug('Parsing map file: {}'.format(scenario))

    @asyncio.coroutine
    def parse(scenario):
        try:
            lua_parser = Parser(scenario)
            search = {'scenarioinfo>name': 'name', 'description': 'description', 'map_version': 'version', 'armies': 'slots', 'size': 'size'}
            defaults = {'name': None, 'description': None, 'version': None, 'slots': 0, 'size': {'0': '0', '1': '0'}}
            return (yield from asyncio.get_event_loop().run_in_executor(None, lua_parser.parse, search, defaults))  # None means run in default executor
        except Exception as e:
            # log.error(e)
            return None

    map_info = yield from parse(scenario)
    map_info['size'] = [map_info['size']['0'], map_info['size']['1']]
    map_info['slots'] = len(map_info['slots'])
    map_info['preview_small'] = small
    map_info['preview_big'] = big

    return Map(code, **map_info)


@asyncio.coroutine
def local_mod_lookup(paths):
    mods = yield from __local_lookup(paths, create_local_mod)
    return {m.uid: m for m in mods}


@asyncio.coroutine
def create_local_mod(name, path):
    # log = logging.getLogger(__name__)

    def icon(file_name, path):
        if os.path.exists(os.path.join(path, file_name)):
            return QUrl.fromLocalFile(os.path.join(path, file_name))

    info = os.path.join(path, 'mod_info.lua')
    # log.debug('Parsing mod file: {}'.format(info))

    @asyncio.coroutine
    def parse(info):
        try:
            lua_parser = Parser(info)
            search = {'uid': 'uid', 'name': 'name', 'description': 'description', 'author': 'author',
                      'version': 'version', 'icon': 'icon', 'ui_only': 'ui_only', 'conflicts': 'conflicts'}
            defaults = {'uid': None, 'name': None, 'description': None, 'author': None, 'version': None, 'icon': None, 'ui_only': False, 'conflicts':{}}
            return (yield from asyncio.get_event_loop().run_in_executor(None, lua_parser.parse, search, defaults))  # None means run in default executor
        except Exception as e:
            # log.error(e)
            return None

    mod_info = yield from parse(info)
    mod_info['conflicts'] = list(mod_info['conflicts'].values())
    mod_info['icon'] = icon(mod_info['icon'].split('/').pop(), path) if mod_info['icon'] is not None else None
    mod_info['ui_only'] = mod_info['ui_only'] == 'true'

    return Mod(**mod_info)
