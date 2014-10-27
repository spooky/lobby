__author__ = 'Sheeo'

from git import Repository, Version
from fa import featured

from collections import namedtuple

class GameVersion():
    """
    For describing the exact version of FA used.
    """
    def __init__(self, dict):
        self._versions = dict

    @property
    def is_valid(self):
        """
        Validity means that the dictionary contains the
        required keys with instances of Version.

        :return: bool
        """
        def valid_version(version):
            return isinstance(version, Version)

        def valid_featured_mod(mod):
            return isinstance(mod, featured.FeaturedMod) \
                   and valid_version(mod.version) and featured.is_featured_mod(mod)

        def valid_mod(mod):
            return True

        valid = "engine" in self._versions
        valid = valid and "game" in self._versions
        for key,value in self._versions.iteritems():
            valid = valid and {
                'engine': lambda version: valid_version(version),
                'game': lambda mod: valid_featured_mod(mod),
                'mods': lambda versions: any(versions)
                                         and all(map(lambda v: valid_mod(v), versions)),
            }.get(key, lambda k: True)(value)

        return valid
