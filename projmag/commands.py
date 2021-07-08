from cleo import Command
from pathlib import Path
from .project import Project
from .directory import Directory

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
