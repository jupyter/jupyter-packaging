
import importlib
import os
import os.path as osp
import subprocess
import shutil
import sys


def test_develop(package_dir):
    name = 'jupyter_packaging_test_foo'
    share = osp.join(sys.prefix, 'share', 'jupyter', name)
    if osp.exists(share):
        shutil.rmtree(share)
    subprocess.check_output([shutil.which('pip'), 'install', '-e', '.'], cwd=str(package_dir))
    assert osp.exists(osp.join(share, 'test.txt'))
    subprocess.check_output([shutil.which('pip'), 'uninstall', '-y', name], cwd=str(package_dir))
    assert osp.exists(osp.join(share, 'test.txt'))
    shutil.rmtree(share)
