from pathlib import Path
from git import Repo, InvalidGitRepositoryError
from functools import total_ordering
from cleo import Command
from typing import Optional

import re
import os
import logging



logger = logging.getLogger()

class InvalidProjectName(Exception):
    """ invalid project name """

@total_ordering
class Project:
    valid_reg = re.compile(r"^\d{4}-")

    def __init__(self, path:Path):
        self.path = Path(path)

    def rename(self, prefix):
        regex = re.compile(r'(^\d+-?)?(.*)')
        name=re.search(regex, self.path.name).groups()[-1]
        dest = self.path.parent / f'{prefix}-{name}'
        logger.debug(f"Renaming {self.path} to {dest}")
        self.path.rename(dest)

    @property
    def number(self): 
        if self.has_valid_name: return int(self.path.name[:4])
        else: return None 

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
        return self.path.name < other.path.name

    def __eq__(self, other):
        return self.path.name == other.path.name
