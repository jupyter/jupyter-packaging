from unittest.mock import patch
import pytest
import sys

from setuptools.dist import Distribution
from jupyter_packaging.setupbase import __file__ as path
import jupyter_packaging.setupbase as pkg

from .utils import run_command


def test_get_version():
    version = pkg.get_version(path)
    assert version == pkg.__version__


def test_combine_commands():
    class MockCommand(pkg.BaseCommand):
        called = 0

        def run(self):
            MockCommand.called += 1

    combined_klass = pkg.combine_commands(MockCommand, MockCommand)
    combined = combined_klass(Distribution())
    combined.initialize_options()
    combined.finalize_options()
    combined.run()
    assert MockCommand.called == 2


def test_run():
    assert pkg.run(sys.executable + " --version") == 0

    with pytest.raises(ValueError):
        pkg.run("foobarbaz")


def test_ensure_existing_targets(destination_dir):
    local_targets = ["file1.rtf", "sub/subfile1.rtf"]
    targets = [str(destination_dir.join(t)) for t in local_targets]
    cmd = pkg.ensure_targets(targets)
    run_command(cmd)


def test_ensure_missing_targets(source_dir):
    local_targets = ["file1.rtf", "sub/subfile1.rtf"]
    targets = [str(source_dir.join(t)) for t in local_targets]
    cmd = pkg.ensure_targets(targets)
    with pytest.raises(ValueError):
        run_command(cmd)


def test_ensure_with_skip_npm(source_dir, mocker):
    mocker.patch("jupyter_packaging.setupbase.skip_npm", True)
    local_targets = ["file1.rtf", "sub/subfile1.rtf"]
    targets = [str(source_dir.join(t)) for t in local_targets]
    cmd = pkg.ensure_targets(targets)
    run_command(cmd)


class TestCommand(pkg.BaseCommand):
    def run(self):
        raise RuntimeError()


# Prevent pytest from trying to collect TestCommand as a test:
TestCommand.__test__ = False


def test_skip_existing(destination_dir):
    local_targets = ["file1.rtf", "sub/subfile1.rtf"]
    targets = [str(destination_dir.join(t)) for t in local_targets]
    cmd = pkg.skip_if_exists(targets, TestCommand)
    run_command(cmd)


def test_no_skip_missing(source_dir):
    local_targets = ["file1.rtf", "sub/subfile1.rtf"]
    targets = [str(source_dir.join(t)) for t in local_targets]
    cmd = pkg.skip_if_exists(targets, TestCommand)
    with pytest.raises(RuntimeError):
        run_command(cmd)
