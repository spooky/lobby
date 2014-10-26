__author__ = 'Sheeo'

from git import Repository, Version

from collections import namedtuple

FeaturedMod = namedtuple("FeaturedMod", "mod version")

class GameVersion():
    """
    For describing the exact version of FA used.
    """
    def __init__(self, dict):
        self._versions = dict

    def is_valid(self):
        """
        Validity means that the dictionary contains the
        required keys with instances of Version.

        :return: bool
        """
        def valid_version(version):
            return isinstance(version, Version)

        def valid_featured_mod(mod):
            return valid_version(mod.version)

        valid = "binary-patch" in self._versions
        valid = valid and "featured-mods" in self._versions
        for key,value in self._versions.iteritems():
            valid = valid and {
                'binary-patch': lambda version: valid_version(version),
                'featured-mods': lambda versions: any(versions)
                                                  and all(map(lambda v: valid_featured_mod(v), versions)),
            }.get(key, lambda k: True)(value)

        return valid
