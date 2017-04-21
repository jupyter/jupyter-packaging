
import os

from jupyter_packaging.setupbase import find_packages


here = os.path.dirname(__file__)
root = os.path.join(here, os.pardir)


def test_finds_itself():
    assert ['jupyter_packaging'] == find_packages(root)

