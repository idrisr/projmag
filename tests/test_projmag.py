from projmag import __version__
from projmag.project import Project, InvalidProjectName
from pathlib import Path
from pytest import raises
from git import Repo

import tempfile
import pytest
import re


def test_version():
    assert __version__ == '0.1.0'

@pytest.mark.parametrize('name,value,number', [
    ("../2025-test-something",  True,  2025),
    ("../202-test-something",   False, None),
    ("../20225-test-something", False, None),
    ("../9999-test-something",  True,  9999),
    ("../0000-test-something",  True,  0),
    ("../0001-test-something",  True,  1)
    ])
def test_has_valid_name(name,value,number):
    path = Path(name)
    p = Project(path)
    assert p.has_valid_name == value

    if p.has_valid_name:
        assert p.number == number
    else: 
        with raises(InvalidProjectName): p.number

def test_has_git():
    with tempfile.TemporaryDirectory() as d:
        r = Repo.init(d)
        p = Project(d)
        assert p.has_git

    with tempfile.TemporaryDirectory() as d:
        p = Project(d)
        assert not p.has_git

def test_has_remote():
    p = Project(".")
    assert not p.has_remote

def test_repr():
    with tempfile.TemporaryDirectory() as d:
        p = Project(d)
        assert "'" not in repr(p)

@pytest.fixture
def projs():
    with tempfile.TemporaryDirectory() as d:
        dirs=['0001-something', '0001-nothing', '0002-everything', '0004-thing',
                '0004-thething', 'shiteshite']
        [(Path(d) / o).mkdir(parents=True, exist_ok=True) for o in dirs]
        yield [Project(Path(d) / o) for o in dirs]

def test_cmp(projs):
    assert projs[0] == projs[1]
    assert projs[1] < projs[2]
    assert projs[2] > projs[0]
    assert projs[3] == projs[4]
    assert projs[3] > projs[2]
    assert projs[5] > projs[4]
    assert projs[5] > projs[0]
    assert projs[5] > projs[1]
