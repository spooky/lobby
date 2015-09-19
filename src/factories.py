import logging
import asyncio
import itertools
import os
from PyQt5.QtCore import QUrl

import utils.lua
from models import Map, Mod


def __runChain(handlers, *args, **kwargs):
    for h in handlers:
        result = h(*args, **kwargs)
        if result:
            return result


@asyncio.coroutine
def __localLookup(paths, factory_method):
    dirs = [(n, os.path.join(p, n)) for p in paths for n in os.listdir(p)]

    tasks = itertools.starmap(factory_method, dirs)
    results = yield from asyncio.gather(*tasks, return_exceptions=True)

    return filter(lambda x: not isinstance(x, Exception), results)


def __executeLua(path):
    log = logging.getLogger(__name__)

    with open(path) as f:
        try:
            lua = utils.lua.runtime()
            lua.execute(f.read())
            return lua.globals()
        except Exception as e:
            log.warning('Error while trying to parse {}. {}'.format(path, e))


@asyncio.coroutine
def localMapLookup(paths):
    maps = yield from __localLookup(paths, createLocalMap)
    return {m.code: m for m in maps}


@asyncio.coroutine
def createLocalMap(code, path):

    def preview(code, path, suffix=''):
        file_name = '{}{}.png'.format(code, suffix)

        if os.path.exists(os.path.join(path, file_name)):
            return QUrl.fromLocalFile(os.path.join(path, file_name))

    def previewSmall(code, path):
        return preview(code, path, suffix='.small')

    def preview_large(code, path):
        return preview(code, path, suffix='.large')

    small = __runChain([previewSmall, preview], code, path)
    big = __runChain([preview_large], code, path)

    # strips the screwed up .vXYZ suffix that are sometimes used in map dir names
    dot_index = code.rfind('.')
    stripped_code = code if dot_index < 0 else code[:dot_index]

    scenario = os.path.join(path, '{}_scenario.lua'.format(stripped_code))

    def read():
        si = __executeLua(scenario).ScenarioInfo
        return dict(
            name=si.name,
            description=si.description,
            version=str(si.map_version),
            size=(si.size[1], si.size[2]),
            slots=len(si.Configurations.standard.teams[1].armies)
        )

    mapInfo = yield from asyncio.get_event_loop().run_in_executor(None, read)
    mapInfo['previewSmall'] = small
    mapInfo['previewBig'] = big

    return Map(code, **mapInfo)


@asyncio.coroutine
def localModLookup(paths):
    mods = yield from __localLookup(paths, createLocalMod)
    return {m.uid: m for m in mods}


@asyncio.coroutine
def createLocalMod(name, path):

    def icon(file_name, path):
        if os.path.exists(os.path.join(path, file_name)):
            return QUrl.fromLocalFile(os.path.join(path, file_name))

    info = os.path.join(path, 'mod_info.lua')

    def read():
        mi = __executeLua(info)
        return dict(
            uid=mi.uid,
            name=mi.name,
            description=mi.description,
            author=mi.author,
            version=mi.version,
            icon=mi.icon,
            uiOnly=mi.ui_only,
            conflicts=mi.conflicts
        )

    modInfo = yield from asyncio.get_event_loop().run_in_executor(None, read)  # None means run in default executor
    modInfo['version'] = str(modInfo['version'])
    modInfo['conflicts'] = list(modInfo['conflicts'].values()) if modInfo['conflicts'] is not None else None
    modInfo['icon'] = icon(modInfo['icon'].split('/').pop(), path) if modInfo['icon'] is not None else None

    return Mod(**modInfo)
