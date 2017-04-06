
from jupyter_packaging.setupbase import which


def test_which_finds_python():
    assert which('python')
