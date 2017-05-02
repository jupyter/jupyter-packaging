
import pytest

from jupyter_packaging.setupbase import ensure_targets
from utils import run_command


def test_ensure_existing_targets(destination_dir):
    local_targets = ['file1.rtf', 'sub/subfile1.rtf']
    targets = [str(destination_dir.join(t)) for t in local_targets]
    cmd = ensure_targets(targets)
    run_command(cmd)


def test_ensure_missing_targets(source_dir):
    local_targets = ['file1.rtf', 'sub/subfile1.rtf']
    targets = [str(source_dir.join(t)) for t in local_targets]
    cmd = ensure_targets(targets)
    with pytest.raises(ValueError):
        run_command(cmd)
