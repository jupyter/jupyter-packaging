import site
from pathlib import Path

from setuptools.dist import Distribution


def mock_dist():
    return Distribution(
        dict(
            script_name="setup.py",
            packages=["foo"],
            name="foo",
        )
    )


def run_command(cmd):
    """Run a setuptools Command"""
    dist = mock_dist()
    instance = cmd(dist)
    instance.initialize_options()
    instance.finalize_options()
    return instance.run()


site_packages = Path(site.getsitepackages()[0])
try:
    target = site_packages / "jupyter_packaging_test.txt"
    site_packages.touch()
    site_packages.unlink()
    site_packages_readonly = False
except Exception:
    site_packages_readonly = True
