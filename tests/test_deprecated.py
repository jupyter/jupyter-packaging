
import os
import sys
from unittest.mock import patch

from deprecation import fail_if_not_removed
import pytest

from setuptools.dist import Distribution

import jupyter_packaging.setupbase as pkg


here = os.path.dirname(__file__)
root = os.path.join(here, os.pardir)


@fail_if_not_removed
def test_finds_itself():
    with pytest.warns(DeprecationWarning):
        assert ['jupyter_packaging'] == pkg.find_packages(root)


def test_finds_subpackages(tmpdir):
    a = tmpdir.mkdir('packageA')
    sub_a1 = a.mkdir('sub1')
    sub_a2 = a.mkdir('sub2')
    b = tmpdir.mkdir('packageB')
    sub_b1 = b.mkdir('sub1')
    sub_b2 = b.mkdir('sub2')
    for d in (a, sub_a1, sub_a2, b, sub_b1, sub_b2):
        d.join('__init__.py').write('')
    # using sets ensure order won't matter
    expected = set([
        'packageA', 'packageA.sub1', 'packageA.sub2',
        'packageB', 'packageB.sub1', 'packageB.sub2'
    ])
    with pytest.warns(DeprecationWarning):
        found = set(pkg.find_packages(str(tmpdir)))
    assert expected == found


def test_finds_only_direct_subpackages(tmpdir):
    a = tmpdir.mkdir('packageA')
    sub_a1 = a.mkdir('sub1')
    sub_a2 = a.mkdir('sub2')
    # No __init__.py in packageA:
    for d in (sub_a1, sub_a2):
        d.join('__init__.py').write('')

    expected = []
    with pytest.warns(DeprecationWarning):
        assert expected == pkg.find_packages(str(tmpdir))


@pytest.mark.skipif(sys.version_info >= (3, 10), reason="Not compatible with Python 3.10+")
def test_ensure_python():
    pkg.ensure_python('>=3.6')
    pkg.ensure_python(['>=3.6', '>=3.5'])

    with pytest.raises(ValueError):
        pkg.ensure_python('<3.5')


@pytest.mark.skipif(sys.version_info < (3, 10), reason="Tests RuntimeError for Python 3.10+")
def test_ensure_python_310():
    with pytest.raises(RuntimeError):
        pkg.ensure_python('>=3.6')


def test_create_cmdclass(make_package_deprecated, mocker):
    source = ("share/test.txt",)
    spec =  ("jupyter-packaging-test", "share", "**/*")
    target = "jupyter-packaging-test/test.txt"

    pkg_path = make_package_deprecated(data_files=source, data_files_spec=spec)
    os.chdir(pkg_path)
    cmdclass = pkg.create_cmdclass(
        package_data_spec=dict(foo="*.*"),
        data_files_spec=[spec],
        exclude=lambda x: False
    )
    for name in ['build_py', 'handle_files', 'sdist', 'bdist_wheel']:
        assert name in cmdclass

    dist = Distribution()
    cmdclass['handle_files'](dist).run()
    assert dist.data_files == [('jupyter-packaging-test', ['share/test.txt'])]
    assert dist.package_data == {'foo': []}

    # Test installation of data_files in develop mode
    dist = Distribution()
    handler = cmdclass['handle_files'](dist)
    develop = cmdclass['develop'](dist)

    def run_command(name):
        cmdclass[name](dist).run()

    mocker.patch.object(pkg.develop, 'install_for_development')
    develop.run_command = run_command
    develop.install_for_development()
    assert dist.data_files == [('jupyter-packaging-test', ['share/test.txt'])]


def test_command_for_func():
    called = False
    def func():
        nonlocal called
        called = True

    cmd = pkg.command_for_func(func)
    cmd(Distribution()).run()
    assert called


def test_install_npm():
    builder = pkg.install_npm()
    assert issubclass(builder, pkg.BaseCommand)


def test__wrap_command():
    called = False
    def func(self, cmd):
        nonlocal called
        called = True

    class TestCommand(pkg.BaseCommand):
        def run(self):
            pass

    cmd = pkg._wrap_command(['js'], TestCommand)
    cmd.run_command = func
    dist = Distribution()
    cmd(dist).run()
    assert called == True


@fail_if_not_removed
def test_get_version_info():
    assert pkg.get_version_info('1.3.0') == (1,3,0)
    assert pkg.get_version_info('1.3.0a1') == (1,3,0,'a1')
    assert pkg.get_version_info('1.3.0.dev0') == (1,3,0,'.dev0')
    with pytest.raises(ValueError):
        pkg.get_version_info('1.3.0foo1')
