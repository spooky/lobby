from check import check_version

from git import Version
__author__ = 'Sheeo'

TEST_GAME_VERSION = Version('FAForever/fa', '3634')
TEST_SIM_MOD = Version('FAForever/test_sim_mod', 'master')

VALID_GAME_VERSION_INFO = {
    "binary-patch": Version('FAForever/binary-patch', 'master'),
    "featured-mods": [TEST_GAME_VERSION],
    "sim-mods": [TEST_SIM_MOD],
    "map": {"name": "scmp_0009", "version": None},
    "featured_mod": "faf",
}

def test_check_valid_game_info():
    assert check_version(VALID_GAME_VERSION_INFO) is True
