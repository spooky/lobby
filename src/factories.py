import logging
import asyncio
import itertools
import os
from PyQt5.QtCore import QUrl

from models import Map, Mod
from utils.lua import get_lua_runtime


def __run_chain(handlers, *args, **kwargs):
    for h in handlers:
        result = h(*args, **kwargs)
        if result:
            return result


@asyncio.coroutine
def __local_lookup(paths, factory_method):
    dirs = [(n, os.path.join(p, n)) for p in paths for n in os.listdir(p)]

    tasks = itertools.starmap(factory_method, dirs)
    results = yield from asyncio.gather(*tasks, return_exceptions=True)

    return filter(lambda x: not isinstance(x, Exception), results)


def __execute_lua(path):
    log = logging.getLogger(__name__)

    with open(path) as f:
        try:
            lua = get_lua_runtime()
            lua.execute(f.read())
            return lua.globals()
        except Exception as e:
            log.warning('Error while trying to parse {}. {}'.format(path, e))


@asyncio.coroutine
def local_map_lookup(paths):
    maps = yield from __local_lookup(paths, create_local_map)
    return {m.code: m for m in maps}


@asyncio.coroutine
def create_local_map(code, path):

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

    def read():
        si = __execute_lua(scenario).ScenarioInfo
        return dict(
            name=si.name,
            description=si.description,
            version=str(si.map_version),
            size=(si.size[1], si.size[2]),
            slots=len(si.Configurations.standard.teams[1].armies)
        )

    map_info = yield from asyncio.get_event_loop().run_in_executor(None, read)
    map_info['preview_small'] = small
    map_info['preview_big'] = big

    return Map(code, **map_info)


@asyncio.coroutine
def local_mod_lookup(paths):
    mods = yield from __local_lookup(paths, create_local_mod)
    return {m.uid: m for m in mods}


@asyncio.coroutine
def create_local_mod(name, path):

    def icon(file_name, path):
        if os.path.exists(os.path.join(path, file_name)):
            return QUrl.fromLocalFile(os.path.join(path, file_name))

    info = os.path.join(path, 'mod_info.lua')

    def read():
        g = __execute_lua(info)
        return {p: g[p] for p in ['uid', 'name', 'description', 'author', 'version', 'icon', 'ui_only', 'conflicts']}

    mod_info = yield from asyncio.get_event_loop().run_in_executor(None, read)  # None means run in default executor
    mod_info['version'] = str(mod_info['version'])
    mod_info['conflicts'] = list(mod_info['conflicts'].values()) if mod_info['conflicts'] is not None else None
    mod_info['icon'] = icon(mod_info['icon'].split('/').pop(), path) if mod_info['icon'] is not None else None

    return Mod(**mod_info)
