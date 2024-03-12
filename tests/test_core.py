import unittest
import pytest
import sys

from os.path import dirname, abspath

project_root = dirname(dirname(abspath(__file__)))
sys.path.append(project_root)

def test_func():
    from src.core import func
    assert func(1) == None
    