from pathlib import Path
import re

class InvalidProjectName(Exception):
    """ invalid project name """

class Project:
    valid_reg = re.compile(r"^\d{4}-")

    def __init__(self, path:Path):
        self.path = path


    @property
    def number(self): 
        if self.has_valid_name: return int(self.path.name[:4])
        else: raise InvalidProjectName

    @property
    def has_valid_name(self): return bool(re.match(self.valid_reg, self.path.name))
