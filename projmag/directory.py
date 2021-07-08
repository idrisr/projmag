import os
import sys
import logging

from pathlib import Path 
from itertools import chain
from collections import Counter
from debjig import log

from .project import Project

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.debug("here we are")

global calls
calls = 0

class Directory:
    @log()
    def __init__(self, path=Path.home() / "nassync"):
        self.path = path

    @log()
    def fix_names(self):
        logger.debug('wtf')
        for o in (self.dupes + self.invalid_projects):
            logger.debug(o.path)
            o.rename(self.nextname)
        for o in self.projects:
            if o.number > int(self.nextname):
                logger.debug(o.path)
                o.rename(self.nextname)

    @property
    @log()
    def projects(self):
        global calls
        calls+=1
        logger.debug(calls)
        projects = [Project(self.path / o) for o in os.listdir(self.path) if not o.startswith('.')]
        return sorted(projects)

    @property
    @log()
    def nextname(self): 
        for _ in range(max(self.valid_projects).number):
            if _ not in self: 
                return f'{_:04d}'
        return f'{max(self.valid_projects).number + 1:04d}'

    @property
    @log()
    def valid_projects(self): return [o for o in self.projects if o.has_valid_name]

    @property
    @log()
    def invalid_projects(self): 
        return [o for o in self.projects if not o.has_valid_name]

    @property
    @log()
    def dupes(self):
        c = Counter([o.number for o in self.projects if o.has_valid_name])
        d = list(k for k,v in c.items() if v>1)
        return list(chain(*[self[v] for v in d]))


    # use bisect to avoid O(n)
    @log()
    def __getitem__(self, i): return [_ for _ in self.valid_projects if _.number == i]
    @log()
    def __contains__(self, i): return len(self[i]) > 0
    @log()
    def __repr__(self): return "\n".join(f'{_}' for _ in self.projects)
    @log()
    def __len__(self): return len(self.projects)
