import importlib
import os
import os.path as osp
import subprocess
import shutil
import sys
import tarfile
import glob


def test_install(nested_package_dir, tmp_path):
    name = 'jupyter_packaging_test_foo'
    share = osp.join(sys.prefix, 'share', 'jupyter', name)
    if osp.exists(share):
        shutil.rmtree(share)
    subprocess.check_output([shutil.which('python'), 'setup.py', 'sdist', '--dist-dir', str(tmp_path)], cwd=str(nested_package_dir))
    fname = glob.glob(osp.join(str(tmp_path), name+"*.gz"))[0]
    tar = tarfile.open(fname, "r")
    f = tar.extractfile(osp.join(name+"-0.1", name, "main.py"))
    assert f.readlines()[0] == b'print("hello, world!")'
