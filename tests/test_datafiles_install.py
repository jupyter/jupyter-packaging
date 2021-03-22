

import pytest
import subprocess
import shutil
import pathlib
import sys

from deprecation import fail_if_not_removed



data_files_combinations = [
    (
        # data file source
        ("share/test.txt",),
        # data file spec
        ("jupyter-packaging-test", "share", "**/*"),
        # data file target
        "jupyter-packaging-test/test.txt"
    ),
    (
        # data file source
        ("share/test.txt",),
        # data file spec
        ("jupyter-packaging-test/level1", "share", "**/[a-z]est.txt"),
        # data file target
        "jupyter-packaging-test/level1/test.txt"
    ),
    (
        # data file source
        ("level1/test/test.txt",),
        # data file spec
        ("jupyter-packaging-test", "level1/test", "**/*"),
        # data file target
        "jupyter-packaging-test/test.txt"
    ),
    (
        # data file source
        ("level1/test/test.txt",),
        # data file spec
        ("jupyter-packaging-test/level1/level2", "level1/test", "**/*"),
        # data file target
        "jupyter-packaging-test//level1/level2/test.txt"
    ),
    (
        # data file source
        ("level1/level2/test/test.txt",),
        # data file spec
        ("jupyter-packaging-test", "level1", "**/*"),
        # data file target
        "jupyter-packaging-test/level2/test/test.txt"
    ),

]


@fail_if_not_removed
@pytest.mark.parametrize(
    'source,spec,target',
    data_files_combinations
)
def test_develop(make_package_deprecated, source,spec,target):
    name = 'jupyter_packaging_test_foo'
    package_dir = make_package_deprecated(name=name, data_files=source, data_files_spec=[spec])
    target_path = pathlib.Path(sys.base_prefix).joinpath(target)
    if target_path.exists():
        shutil.rmtree(str(target_path.parent))
    subprocess.check_output([shutil.which('pip'), 'install', '-e', '.'], cwd=str(package_dir))
    assert target_path.exists()
    subprocess.check_output([shutil.which('pip'), 'uninstall', '-y', name], cwd=str(package_dir))
    # This is something to fix later. uninstalling a package installed
    # with -e should ne removed.
    assert target_path.exists()
    shutil.rmtree(str(target_path.parent))


@pytest.mark.parametrize(
    'source,spec,target',
    data_files_combinations
)
def test_install(make_package, source,spec,target):
    name = 'jupyter_packaging_test_foo'
    package_dir = make_package(name=name, data_files=source, data_files_spec=[spec])
    target_path = pathlib.Path(sys.base_prefix).joinpath(target)
    if target_path.exists():
        shutil.rmtree(str(target_path.parent))
    subprocess.check_output([shutil.which('pip'), 'install', '.'], cwd=str(package_dir))
    assert target_path.exists()
    subprocess.check_output([shutil.which('pip'), 'uninstall', '-y', name], cwd=str(package_dir))
    assert not target_path.exists()
