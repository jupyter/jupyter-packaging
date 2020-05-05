
import sys
from jupyter_packaging.setupbase import which


def test_which_finds_python_executable():
    assert which(sys.executable)
