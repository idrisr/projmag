from projmag import __version__
from projmag.project import Project, InvalidProjectName
from pathlib import Path
from pytest import raises
from git import Repo

import tempfile
import pytest
import re
import os


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
        assert p.number is None

def test_has_git():
    with tempfile.TemporaryDirectory() as d:
        r = Repo.init(d)
        p = Project(d)
        assert p.has_git

    with tempfile.TemporaryDirectory() as d:
        p = Project(d)
        assert not p.has_git

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
        yield [Project(Path(d) / o) for o in dirs], d

def test_cmp(projs):
    projs,*_ = projs
    assert projs[0] > projs[1]
    assert projs[1] < projs[2]
    assert projs[2] > projs[0]
    assert projs[4] < projs[3]
    assert projs[3] > projs[2]
    assert projs[5] > projs[4]
    assert projs[5] > projs[0]
    assert projs[5] > projs[1]

def test_cmp2():
    p1 = Project('0001-something')
    p2 = Project('0001-nothing')
    assert p2 < p1

def test_rename(projs):
    projs,d=projs
    p0 = projs[-1]
    p0.rename('0009')
    assert '0009-shiteshite' in os.listdir(d)
    p0 = projs[0]
    p0.rename('0019')
    assert '0019-something' in os.listdir(d)


def test_lt(projs):
    projs,d=projs
    projs = sorted(projs)
    assert 'shiteshite' in projs[-1].path.as_posix()
