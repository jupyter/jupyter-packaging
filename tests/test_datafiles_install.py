import pytest
import subprocess
import shutil
import pathlib
import sys

from deprecation import fail_if_not_removed

from .utils import site_packages_readonly


data_files_combinations = [
    (
        # data file source
        ("share/test.txt",),
        # data file spec
        ("jupyter-packaging-test", "share", "**/*"),
        # data file target
        "jupyter-packaging-test/test.txt",
    ),
    (
        # data file source
        ("share/test.txt",),
        # data file spec
        ("jupyter-packaging-test/level1", "share", "**/[a-z]est.txt"),
        # data file target
        "jupyter-packaging-test/level1/test.txt",
    ),
    (
        # data file source
        ("level1/test/test.txt",),
        # data file spec
        ("jupyter-packaging-test", "level1/test", "**/*"),
        # data file target
        "jupyter-packaging-test/test.txt",
    ),
    (
        # data file source
        ("level1/test/test.txt",),
        # data file spec
        ("jupyter-packaging-test/level1/level2", "level1/test", "**/*"),
        # data file target
        "jupyter-packaging-test//level1/level2/test.txt",
    ),
    (
        # data file source
        ("level1/level2/test/test.txt",),
        # data file spec
        ("jupyter-packaging-test", "level1", "**/*"),
        # data file target
        "jupyter-packaging-test/level2/test/test.txt",
    ),
]


@pytest.mark.skipif(site_packages_readonly, reason="Site Packages are Read-only")
@fail_if_not_removed
@pytest.mark.parametrize("source,spec,target", data_files_combinations)
def test_develop(make_package_deprecated, source, spec, target):
    name = "jupyter_packaging_test_foo"
    package_dir = make_package_deprecated(
        name=name, data_files=source, data_files_spec=[spec]
    )
    target_path = pathlib.Path(sys.prefix).joinpath(target)
    if target_path.exists():
        shutil.rmtree(str(target_path.parent))
    subprocess.check_output(
        [sys.executable, "-m", "pip", "install", "-e", "."], cwd=str(package_dir)
    )
    assert target_path.exists()
    subprocess.check_output(
        [sys.executable, "-m", "pip", "uninstall", "-y", name], cwd=str(package_dir)
    )
    # This is something to fix later. uninstalling a package installed
    # with -e should be removed.
    assert target_path.exists()
    shutil.rmtree(str(target_path.parent))


@pytest.mark.skipif(site_packages_readonly, reason="Site Packages are Read-only")
@pytest.mark.parametrize("source,spec,target", data_files_combinations)
def test_install(make_package, source, spec, target):
    name = "jupyter_packaging_test_foo"
    package_dir = make_package(name=name, data_files=source, data_files_spec=[spec])
    target_path = pathlib.Path(sys.prefix).joinpath(target)
    if target_path.exists():
        shutil.rmtree(str(target_path.parent))
    subprocess.check_output(
        [sys.executable, "-m", "pip", "install", "."], cwd=str(package_dir)
    )
    assert target_path.exists()
    subprocess.check_output(
        [sys.executable, "-m", "pip", "uninstall", "-y", name], cwd=str(package_dir)
    )
    assert not target_path.exists()
