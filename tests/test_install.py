import importlib
import os
import os.path as osp
import subprocess
import shutil
import sys
import tarfile
import glob
import site
import pathlib
import sysconfig

def test_install(make_package, tmp_path):
    name = 'jupyter_packaging_test_foo'
    package_dir = make_package(name=name)
    subprocess.check_output([shutil.which('pip'), 'install', '.'], cwd=str(package_dir))
    # Get site packages where the package is installed.
    sitepkg = sysconfig.get_paths()["purelib"]
    installed_files = pathlib.Path(sitepkg).joinpath("{name}/main.py".format(name=name))
    assert installed_files.exists()
    subprocess.check_output([shutil.which('pip'), 'uninstall', name, '-y'], cwd=str(package_dir))
    assert not installed_files.exists()