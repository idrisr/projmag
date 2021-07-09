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
    def __init__(self, path=Path.home() / "nassync"):
        self.path = path
        self._reload()

    def _reload(self):
        projects = [Project(self.path / o) for o in os.listdir(self.path) if not o.startswith('.')]
        self.projects = sorted(projects, reverse=False)

    def fix_names(self):
        stack = list(range(len(self)))[::-1]
        for project in self.projects:
            if project.number in stack:
                stack.pop(stack.index(project.number))
            else:
                dest = stack.pop()
                project.rename(f'{dest:04d}')

        self._reload()

    @property
    def nextname(self): 
        for _ in range(max(self.valid_projects).number):
            if _ not in self: 
                return f'{_:04d}'
        return f'{max(self.valid_projects).number + 1:04d}'

    @property
    def valid_projects(self): return [o for o in self.projects if o.has_valid_name]

    @property
    def invalid_projects(self): 
        return [o for o in self.projects if not o.has_valid_name]

    @property
    def dupes(self):
        c = Counter([o.number for o in self.projects if o.has_valid_name])
        d = list(k for k,v in c.items() if v>1)
        return list(chain(*[self[v] for v in d]))


    # use bisect to avoid O(n)
    def __getitem__(self, i): return [_ for _ in self.valid_projects if _.number == i]
    def __contains__(self, i): return len(self[i]) > 0
    def __repr__(self): return "\n".join(f'{_}' for _ in self.projects)
    def __len__(self): return len(self.projects)
