__author__ = "Thygrrr, humbly treading in the shadow of sheeo's awesomeness"

import os
import git
import util
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)


FeaturedModVersion = namedtuple('FeaturedModVersion', ['repo', 'tag', 'hash'])

def checkout_featured_mod(featured_mod, featured_repo, featured_version="faf/master", repo_dir=util.REPO_DIR):
    mod_repo = git.Repository(os.path.join(repo_dir, featured_mod), featured_repo)
    mod_repo.fetch()
    mod_repo.checkout(featured_version)

def featured_versions_to_repo_tag(featured_versions_hash):
    return str(reduce(max, featured_versions_hash.itervalues(), 0))

def replay_info_to_featured_mod_version(replay_info):
    return FeaturedModVersion("FAForever/fa",
                              featured_versions_to_repo_tag(replay_info["featured_mod_versions"]),
                              None)