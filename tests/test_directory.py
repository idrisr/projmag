from projmag.project import Project
from projmag.directory import Directory
from pathlib import Path

import tempfile
import pytest
import os


@pytest.fixture
def dir_():
    with tempfile.TemporaryDirectory() as d:
        dirs=['0001-something', '0001-nothing', '0002-everything', '0004-thing',
                '0004-thething']
        [(Path(d) / o).mkdir(parents=True, exist_ok=True) for o in dirs]
        yield Directory(Path(d))


@pytest.fixture
def dir_none():
    with tempfile.TemporaryDirectory() as d:
        dirs=['0000-yeah', '0001-something', '0002-nothing', '0003-everything', '0004-thing',
                '0005-thething', '0006-six-is-nine', "whatwhat"]
        [(Path(d) / o).mkdir(parents=True, exist_ok=True) for o in dirs]
        yield Directory(Path(d))

@pytest.fixture
def dir_missing():
    with tempfile.TemporaryDirectory() as d:
        dirs=['0000-yeah', '0001-something', '0002-nothing', 'everything', '0004-thing',
                '0005-thething', '0006-six-is-nine', "whatwhat"]
        [(Path(d) / o).mkdir(parents=True, exist_ok=True) for o in dirs]
        yield Directory(Path(d))


def test_valid_projects(dir_, dir_none):
    assert len(dir_.valid_projects) == 5
    assert len(dir_none.valid_projects) == 7


def test_invalid_projects(dir_, dir_none):
    assert len(dir_.invalid_projects) == 0
    assert len(dir_none.invalid_projects) == 1


def test_dupes(dir_none):
    assert len(dir_none.dupes) == 0
    assert len(dir_none) == 8


def test_dupes2(dir_):
    assert len(dir_.dupes) == 4
    assert len(dir_) == 5
    assert isinstance(dir_.dupes[0], Project)


def test_get_item(dir_, dir_none):
    assert len(dir_[1]) == 2
    assert len(dir_[0]) == 0
    assert len(dir_[2]) == 1
    assert len(dir_[3]) == 0
    assert len(dir_[30]) == 0
    assert len(dir_['asdf']) == 0

    assert len(dir_none[1]) == 1
    assert len(dir_none[0]) == 1
    assert len(dir_none[2]) == 1
    assert len(dir_none[3]) == 1
    assert len(dir_none[30]) == 0
    assert len(dir_none['asdf']) == 0


#  @pytest.mark.skip(reason="come back to this")
def test_next_name(dir_, dir_none, dir_missing):
    assert dir_.nextname == '0000'
    assert dir_none.nextname == '0007'
    assert dir_missing.nextname == '0003'

#  @pytest.mark.skip(reason="come back to this")
def test_fix_projects(dir_none, dir_):
    dir_none.fix_names()
    assert len(dir_none.invalid_projects) == 0
    assert '0000-yeah' in os.listdir(dir_none.path)
    assert '0007-whatwhat' in os.listdir(dir_none.path)

    dir_.fix_names()
    assert len(dir_.invalid_projects) == 0
    assert len(dir_.dupes) == 0
    assert '0001-nothing' in os.listdir(dir_.path)
    assert '0000-something' in os.listdir(dir_.path)


@pytest.fixture
def dir_big():
    with tempfile.TemporaryDirectory() as d:
        [(Path(d) / f'{o:04d}-asdf').mkdir(parents=True, exist_ok=True) for o in
                range(50)]
        yield Directory(Path(d))

@pytest.mark.timeout(4)
def test_slow(dir_big):
    # on the full nassync dir everything is slow. probably because projects is 
    # is a property. See if I can recreate that in a test
    dir_big.fix_names()
