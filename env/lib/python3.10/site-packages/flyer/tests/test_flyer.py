import pytest
import flyer


def test_project_defines_author_and_version():
    assert hasattr(flyer, '__author__')
    assert hasattr(flyer, '__version__')
