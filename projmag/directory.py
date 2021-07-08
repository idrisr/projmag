import os

from .project import Project
from pathlib import Path 
from itertools import chain
from cleo import Command
from collections import Counter


class Directory:
    def __init__(self, path=Path.home() / "nassync"):
        self.path = path

    def fix_names(self):
        for o in (self.dupes + self.invalid_projects):
            print(o)
            o.rename(self.nextname)

    @property
    def projects(self):
        projects = [Project(self.path / o) for o in os.listdir(self.path) if not o.startswith('.')]
        return sorted(projects)

    @property
    def nextname(self): 
        for _ in range(max(self.valid_projects).number):
            if _ not in self: 
                return f'{_:04d}'
        return f'{max(self.valid_projects).number + 1:04d}'

    @property
    def valid_projects(self): return [o for o in self.projects if o.has_valid_name]

    @property
    def invalid_projects(self): return [o for o in self.projects if not o.has_valid_name]

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

class RenameCommand(Command):
    """
    rename dirs into valid things

    rename
    """
    def handle(self):
        path = Path.home() / "nassync"
        d = Directory(path)
        d.fix_names()

class NextCommand(Command):
    """
    next valid command

    next
    """
    def handle(self):
        path = Path.home() / "nassync"
        d = Directory(path)
        self.line(d.nextname)

class ListCommand(Command):
    """
    List Dirs

    list
        {--r|reverse : If set, the task will yell in uppercase letters}
    """

    def handle(self):
        path = Path.home() / "nassync"
        d = Directory(path)
        self.line(str(d))

class DupeCommand(Command):
    """
    Find Dupes

    dupes
    """

    def handle(self):
        path = Path.home() / "nassync"
        d = Directory(path)
        self.line('<info>f"{"\n".join([str(_) for _ in d.dupes])}"</info>')
