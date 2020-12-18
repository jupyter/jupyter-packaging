import pytest

from jupyter_packaging.setupbase import skip_if_exists, BaseCommand
from utils import run_command


class TestCommand(BaseCommand):
    def run(self):
      raise RuntimeError()


def test_skip_existing(destination_dir):
    local_targets = ['file1.rtf', 'sub/subfile1.rtf']
    targets = [str(destination_dir.join(t)) for t in local_targets]
    cmd = skip_if_exists(targets, TestCommand)
    run_command(cmd)


def test_no_skip_missing(source_dir):
    local_targets = ['file1.rtf', 'sub/subfile1.rtf']
    targets = [str(source_dir.join(t)) for t in local_targets]
    cmd = skip_if_exists(targets, TestCommand)
    with pytest.raises(RuntimeError):
        run_command(cmd)
