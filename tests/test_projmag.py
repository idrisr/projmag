from projmag import __version__
from projmag.project import Project, InvalidProjectName
from pathlib import Path
from pytest import raises
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
