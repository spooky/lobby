import os.path
import asyncio
import pytest

from PyQt5.QtCore import QUrl


@pytest.fixture(scope='module')
def loop(request):
    loop = asyncio.get_event_loop()

    def close_loop():
        loop.close()
    request.addfinalizer(close_loop)

    return loop


def test_createLocalMap(loop):
    from factories import createLocalMap

    code = 'sample_map'
    path = os.path.join(os.path.dirname(__file__), code)
    m = loop.run_until_complete(createLocalMap(code, path))

    assert m.code == 'sample_map'
    assert m.name == '2V2 Sand Box'
    assert m.description == 'lorem ipsum'
    assert m.version == '66'
    assert m.slots == 4
    assert m.size == (512, 510)
    assert m.previewSmall == QUrl.fromLocalFile(os.path.join(path, 'sample_map.png'))
    assert m.previewBig is None


def test_createLocalMap_with_screwed_up_versioning(loop):
    from factories import createLocalMap

    code = 'sample_map.v002'
    path = os.path.join(os.path.dirname(__file__), code)
    m = loop.run_until_complete(createLocalMap(code, path))

    assert m.code == 'sample_map.v002'
    assert m.name == '2V2 Sand Box'
    assert m.description == 'lorem ipsum'
    assert m.version == '66'
    assert m.slots == 4
    assert m.size == (512, 510)
    assert m.previewSmall == QUrl.fromLocalFile(os.path.join(path, 'sample_map.v002.png'))
    assert m.previewBig is None


def test_createLocalMod(loop):
    from factories import createLocalMod

    name = 'sample_mod'
    path = os.path.join(os.path.dirname(__file__), name)
    m = loop.run_until_complete(createLocalMod(name, path))

    assert m.uid == '78613f40-3428-44be-8fca-e4f6967c1bb3'
    assert m.name == 'sample_mod'
    assert m.description == 'sample mod for tests'
    assert m.author == 'spooky'
    assert m.version == '33'
    assert m.icon == QUrl.fromLocalFile(os.path.join(path, 'mod_icon.png'))
    assert m.uiOnly is True
    assert m.conflicts == ['8f3031ed-41fc-46e8-b409-d2820ae4b0b5']
