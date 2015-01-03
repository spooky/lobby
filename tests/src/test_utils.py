import os.path
import pytest


def test_LocalContainer_find_valid_path():
    from utils.collections import LocalContainer

    search_paths = [os.path.dirname(os.path.dirname(__file__))]
    factory = lambda k, p: os.path.basename(p)
    c = LocalContainer(paths=search_paths, factory=factory)

    assert c['src'] == 'src'


def test_LocalContainer_raise_on_non_existing_item():
    from utils.collections import LocalContainer

    search_paths = [os.path.dirname(os.path.dirname(__file__))]
    factory = lambda k, p: os.path.basename(p)
    c = LocalContainer(paths=search_paths, factory=factory)

    with pytest.raises(KeyError):
        assert c['I_hope_this_is_not_here']


def test_Storage_find_valid_item():
    from utils.collections import Storage, LocalContainer

    search_paths = [os.path.dirname(os.path.dirname(__file__))]
    factory = lambda k, p: os.path.basename(p)
    lc = LocalContainer(paths=search_paths, factory=factory)

    s = Storage(containers=[lc])

    assert s['src'] == 'src'


def test_Storage_raise_on_invalid_item():
    from utils.collections import Storage, LocalContainer

    search_paths = [os.path.dirname(os.path.dirname(__file__))]
    factory = lambda k, p: os.path.basename(p)
    lc = LocalContainer(paths=search_paths, factory=factory)

    s = Storage(containers=[lc])

    with pytest.raises(KeyError):
        assert s['I_hope_this_is_not_here']


def test_Storage_find_valid_item_in_second_container():
    from utils.collections import Storage, LocalContainer

    factory = lambda k, p: os.path.basename(p)

    search_paths = [os.path.dirname(__file__)]
    lc1 = LocalContainer(paths=search_paths, factory=factory)

    search_paths = [os.path.dirname(os.path.dirname(__file__))]
    lc2 = LocalContainer(paths=search_paths, factory=factory)

    s = Storage(containers=[lc1, lc2])

    assert s['src'] == 'src'
