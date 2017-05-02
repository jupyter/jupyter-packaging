
from setuptools.dist import Distribution


def mock_dist():
    return Distribution(dict(
        script_name='setup.py',
        packages=['foo'],
        name='foo',
    ))

def run_command(cmd):
    """Run a distutils/setuptools Command """
    dist = mock_dist()
    instance = cmd(dist)
    instance.initialize_options()
    instance.finalize_options()
    return instance.run()
