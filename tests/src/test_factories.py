import os.path

from PyQt5.QtCore import QUrl


def test_create_local_map():
    from factories import create_local_map

    code = 'sample_map'
    path = os.path.join(os.path.dirname(__file__), code)
    m = create_local_map(code, path)

    assert m.code == 'sample_map'
    assert m.name == '2V2 Sand Box'
    assert m.description == 'lorem ipsum'
    assert m.version == '66'
    assert m.slots == 4
    assert m.size == ['512', '510']
    assert m.preview_small == QUrl.fromLocalFile(os.path.join(path, 'sample_map.png'))
    assert m.preview_big is None


def test_create_local_map_with_screwed_up_versioning():
    from factories import create_local_map

    code = 'sample_map.v002'
    path = os.path.join(os.path.dirname(__file__), code)
    m = create_local_map(code, path)

    assert m.code == 'sample_map.v002'
    assert m.name == '2V2 Sand Box'
    assert m.description == 'lorem ipsum'
    assert m.version == '66'
    assert m.slots == 4
    assert m.size == ['512', '510']
    assert m.preview_small == QUrl.fromLocalFile(os.path.join(path, 'sample_map.v002.png'))
    assert m.preview_big is None


def test_create_local_mod():
    from factories import create_local_mod

    name = 'sample_mod'
    path = os.path.join(os.path.dirname(__file__), name)
    m = create_local_mod(name, path)

    assert m.uid == '78613f40-3428-44be-8fca-e4f6967c1bb3'
    assert m.name == 'sample_mod'
    assert m.description == 'sample mod for tests'
    assert m.author == 'spooky'
    assert m.version == '33'
    assert m.icon == QUrl.fromLocalFile(os.path.join(path, 'mod_icon.png'))
    assert m.ui_only is True
    assert m.conflicts == ['8f3031ed-41fc-46e8-b409-d2820ae4b0b5']
