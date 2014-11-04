#!/usr/bin/env python
""" git.py

    File that handles writing facts to the filesystem
"""

from git import Repo

import uuid

class MyGit(object):
    """ Dumper class. Used to dump facts to the filesystem
        and monitor via the Git API
    """

    def __init__(self):
        """ Creates a git object """

        self.repo = Repo("/Users/mierdin/Code/Nexus9kBUVisit")
        assert self.repo.bare == False

    def addfile(self, filename):
        #TODO: Check to see if something changed first before adding.
        self.repo.index.add([filename])

    def commitchanges(self):

        ID = None
        ID = str(uuid.uuid4())
        self.repo.index.commit(message="Automated Commit. ID: " + ID)
