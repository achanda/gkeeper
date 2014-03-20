"""Revision management using git."""

from ConfigParser import DuplicateSectionError
from git import Repo
import os

KEEPER_NAME = 'keeper'
KEEPER_EMAIL = 'blah@blah.com'

class VersionManager(object):
    """Store versioned files in a git repository."""

    def __init__(self, path):
        """Initialize a git repo.

        Idempotent; will harmlessly reinitialize an existing repo.

        Args:
            path: Path on disk to the repository.
        """
        try:
           if not os.path.exists(path):
             os.makedirs(path)
           self._repo = Repo.init(path)
           self._cf_writer = self._repo.config_writer()
           self._cf_writer.add_section('user')
           self._cf_writer.set('user', 'name', KEEPER_NAME)
           self._cf_writer.set('user', 'email', KEEPER_EMAIL)

        except DuplicateSectionError: pass

    def add_file(self, name):
        """Add a file."""
        self._repo.git.add(name)

    def commit(self, message):
        """Commit changes to already-added files."""
        self._repo.git.commit('-m %s' % message)
