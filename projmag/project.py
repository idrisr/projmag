from pathlib import Path
from git import Repo, InvalidGitRepositoryError
from functools import total_ordering

import re
import os
from cleo import Command

class InvalidProjectName(Exception):
    """ invalid project name """

@total_ordering
class Project:
    valid_reg = re.compile(r"^\d{4}-")

    def __init__(self, path:Path):
        self.path = Path(path)

    @property
    def number(self): 
        if self.has_valid_name: return int(self.path.name[:4])
        else: raise InvalidProjectName

    @property
    def has_valid_name(self): return bool(re.match(self.valid_reg, self.path.name))

    @property
    def has_git(self): 
        try: return bool(Repo(self.path))
        except InvalidGitRepositoryError: return False

    @property
    def has_remote(self): return len(Repo(self.path).remotes) > 0
    def __repr__(self): return repr(self.path.as_posix()).replace("'", "")

    def __lt__(self, other):
        if self.has_valid_name and other.has_valid_name:
            return self.number < other.number
        else: return False

    def __eq__(self, other):
        if self.has_valid_name and other.has_valid_name: 
            return self.number == other.number
        else: return False
