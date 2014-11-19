import pytest


@pytest.fixture(scope='session', autouse=True)
def paths_setup():
    """
    Set up 'src' dir in the path so that imports are possible without making 'src' importable (HACK)
    """
    import os
    import sys

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
