

import pytest
import subprocess
import shutil
import pathlib
import sys


data_files_specs = [
    ("jupyter-packaging-test", "share", "test.txt"),
    ("jupyter-packaging-test/level1", "share", "test.txt"),
    ("jupyter-packaging-test", "level1/test", "test.txt"),
    ("jupyter-packaging-test/level1/level2", "level1/test", "test.txt")
]


@pytest.mark.parametrize(
    'data_files_spec,',
    data_files_specs
)
def test_develop(make_package, data_files_spec):
    name = 'jupyter_packaging_test_foo'
    package_dir = make_package(name=name, data_files_spec=[data_files_spec])
    target_suffix = data_files_spec[0]
    target = pathlib.Path(sys.base_prefix).joinpath(target_suffix).resolve()
    if target.exists():
        shutil.rmtree(target)
    subprocess.check_output([shutil.which('pip'), 'install', '-e', '.'], cwd=str(package_dir))
    assert target.joinpath('test.txt').exists()
    subprocess.check_output([shutil.which('pip'), 'uninstall', '-y', name], cwd=str(package_dir))
    assert target.joinpath('test.txt').exists()
    shutil.rmtree(target)
