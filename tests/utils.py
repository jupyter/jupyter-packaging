
import os
import site

from setuptools.dist import Distribution


def mock_dist():
    return Distribution(dict(
        script_name='setup.py',
        packages=['foo'],
        name='foo',
    ))

def run_command(cmd):
    """Run a setuptools Command """
    dist = mock_dist()
    instance = cmd(dist)
    instance.initialize_options()
    instance.finalize_options()
    return instance.run()


site_packages = site.getsitepackages()[0]
try:
    target = os.path.join(site_packages, 'jupyter_packaging_test.txt')
    with open(target, 'w') as fid:
        pass
    os.remove(target)
    site_packages_readonly = False
except Exception:
    site_packages_readonly = True
