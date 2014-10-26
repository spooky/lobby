from fa.version import GameVersion
from fa.featured import FeaturedMod
from git import Repository,Version

import pytest

__author__ = 'Sheeo'

TEST_GAME_VERSION = Version('FAForever/fa', '3634')
TEST_SIM_MOD = Version('FAForever/test_sim_mod', 'master')

VALID_BINARY_PATCH = Version('FAForever/binary-patch', 'master')

VALID_GAME_VERSION_INFO = {
    "binary-patch": Version('FAForever/binary-patch', 'master'),
    "featured-mods": [FeaturedMod("faf",TEST_GAME_VERSION)],
    "sim-mods": [TEST_SIM_MOD],
    "map": {"name": "scmp_0009", "version": None},
    "featured_mod": "faf",
}


@pytest.fixture(scope='function')
def version():
    return VALID_GAME_VERSION_INFO.copy()

def test_game_version_can_be_created_from_valid_dict():
    assert GameVersion(VALID_GAME_VERSION_INFO).is_valid

def test_game_version_requires_valid_binary_patch_version(version):
    version["binary-patch"]  = {"a":"b"}
    assert not GameVersion(version).is_valid()

def test_game_version_requires_valid_featured_mods(version):
    version['featured-mods'] = []
    assert not GameVersion(version).is_valid()

def test_game_version_requires_existing_featured_mods(version):
    version['featured-mods'] = [FeaturedMod("non-existing-featured-mod", Version('example', 'example'))]
    assert not GameVersion(version).is_valid()
