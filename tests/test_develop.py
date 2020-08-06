

import pytest
import subprocess
import shutil
import pathlib
import sys


data_files_source = [
    ("share/test.txt",),
    ("share/test.txt",),
    ("level1/test/test.txt",),
    ("level1/test/test.txt",),
]

# Data file specs are tuples with (target_dir, source_dir, pattern)
data_files_specs = [
    ("jupyter-packaging-test", "share", "*.*"),
    ("jupyter-packaging-test/level1", "share",  "*.*"),
    ("jupyter-packaging-test", "level1/test",  "*.*"),
    ("jupyter-packaging-test/level1/level2", "level1/test", "*.*")
]


@pytest.mark.parametrize(
    'data_files,data_files_spec,',
    list(zip(data_files_source, data_files_specs))
)
def test_develop(make_package, data_files, data_files_spec):
    name = 'jupyter_packaging_test_foo'
    package_dir = make_package(name=name, data_files=data_files, data_files_spec=[data_files_spec])
    target_suffix = data_files_spec[0]
    target = pathlib.Path(sys.base_prefix).joinpath(target_suffix)
    if target.exists():
        shutil.rmtree(str(target))
    subprocess.check_output([shutil.which('pip'), 'install', '-e', '.'], cwd=str(package_dir))
    assert target.joinpath('test.txt').exists()
    subprocess.check_output([shutil.which('pip'), 'uninstall', '-y', name], cwd=str(package_dir))
    assert target.joinpath('test.txt').exists()
    shutil.rmtree(str(target))
