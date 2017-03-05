#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from glob import glob
import logging as log
import os
from os.path import join as pjoin
import pipes

# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

from distutils.cmd import Command
from distutils.command.build_py import build_py
from distutils.command.sdist import sdist
from subprocess import check_call
import sys

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None

if any(arg.startswith('bdist') for arg in sys.argv):
    from setuptools.command.bdist_egg import bdist_egg
else:
    bdist_egg = None

if 'setuptools' in sys.modules:
    from setuptools.command.develop import develop


__all__ = ['create_python_cmdclass', 'create_dual_cmdclass', 'find_packages']

# ---------------------------------------------------------------------------
# Public Functions
# ---------------------------------------------------------------------------


def find_packages(top):
    """
    Find all of the packages.
    """
    packages = []
    for dir, subdirs, files in os.walk(top):
        package = dir.replace(os.path.sep, '.')
        if '__init__.py' not in files:
            # Not a package
            continue
        packages.append(package)
    return packages


def create_python_cmdclass():
    """Create the cmdclass for a Python only package.
    """
    cmdclass = dict(
        build_py=check_package_data_first(build_py),
        sdist=sdist
    )
    if 'setuptools' in sys.modules:
        # setup.py develop should check for submodules
        cmdclass['develop'] = develop
    if bdist_wheel:
        cmdclass['bdist_wheel'] = bdist_wheel
    return cmdclass


def create_dual_cmdclass(js_targets):
    """Create the cmdclass for a dual Python and JavaScript package.

    Parameters
    ----------
    js_targets: list(paths)
        a list of JavaScript paths that must be included.
    """
    NPM.targets = js_targets
    cmdclass = dict(
        jsdeps=NPM,
        build_py=check_package_data_first(js_prerelease(build_py)),
        sdist=js_prerelease(sdist, strict=True)
    )
    if 'setuptools' in sys.modules:
        # setup.py develop should check for submodules
        cmdclass['develop'] = js_prerelease(develop)
    if bdist_wheel:
        cmdclass['bdist_wheel'] = js_prerelease(bdist_wheel)
    return cmdclass


# -----------------------------------------------------------------------------
# Minimal Python version sanity check
# -----------------------------------------------------------------------------

v = sys.version_info
if v[:2] < (2, 7) or (v[0] >= 3 and v[:2] < (3, 3)):
    error = "ERROR: package requires Python version 2.7 or 3.3 or above."
    print(error, file=sys.stderr)
    sys.exit(1)

PY3 = (sys.version_info[0] >= 3)


# -----------------------------------------------------------------------------
# get on with it
# -----------------------------------------------------------------------------

log.basicConfig(level=log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

repo_root = os.path.dirname(os.path.abspath(sys.argv[0]))
is_repo = os.path.exists(pjoin(repo_root, '.git'))

npm_path = os.pathsep.join([
    pjoin(repo_root, 'node_modules', '.bin'),
    os.environ.get("PATH", os.defpath),
])


if sys.platform == 'win32':
    from subprocess import list2cmdline
else:
    def list2cmdline(cmd_list):
        return ' '.join(map(pipes.quote, cmd_list))


def mtime(path):
    """shorthand for mtime"""
    return os.stat(path).st_mtime


def run(cmd, *args, **kwargs):
    """Echo a command before running it"""
    log.info('> ' + list2cmdline(cmd))
    kwargs.setdefault('cwd', repo_root)
    kwargs.setdefault('shell', sys.platform == 'win32')
    return check_call(cmd, *args, **kwargs)


def js_prerelease(command, strict=False):
    """Decorator for building JavaScript prior to another command"""
    class DecoratedCommand(command):

        def run(self):
            jsdeps = self.distribution.get_command_obj('jsdeps')
            if not is_repo and all(os.path.exists(t) for t in jsdeps.targets):
                # sdist, nothing to do
                command.run(self)
                return

            try:
                self.distribution.run_command('jsdeps')
            except Exception as e:
                missing = [t for t in jsdeps.targets if not os.path.exists(t)]
                if strict or missing:
                    log.warn("rebuilding js and css failed")
                    if missing:
                        log.error("missing files: %s" % missing)
                    raise e
                else:
                    log.warn("rebuilding js and css failed (not a problem)")
                    log.warn(str(e))
            command.run(self)
            update_package_data(self.distribution)
    return DecoratedCommand


def check_package_data(package_data):
    """Verify that package_data globs make sense."""
    log.info("Checking package data")
    for pkg, data in package_data.items():
        pkg_root = pjoin(*pkg.split('.'))
        for d in data:
            path = pjoin(pkg_root, d)
            if '*' in path:
                assert len(glob(path)) > 0, "No files match pattern %s" % path
            else:
                assert os.path.exists(path), "Missing package data: %s" % path


def check_package_data_first(command):
    """decorator for checking package_data before running a given command

    Probably only needs to wrap build_py
    """
    class DecoratedCommand(command):

        def run(self):
            check_package_data(self.package_data)
            command.run(self)
    return DecoratedCommand


def update_package_data(distribution):
    """update package_data to catch changes during setup"""
    build_py = distribution.get_command_obj('build_py')
    # distribution.package_data = find_package_data()
    # re-init build_py options which load package_data
    build_py.finalize_options()


class NPM(Command):
    description = "install package.json dependencies using npm"

    user_options = []

    node_modules = pjoin(repo_root, 'node_modules')

    targets = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def has_npm(self):
        try:
            run(['npm', '--version'])
            return True
        except Exception as e:
            log.error(e)
            return False

    def should_run_npm(self):
        if not os.path.exists(self.node_modules):
            return True
        return (mtime(self.node_modules) <
                mtime(pjoin(repo_root, 'package.json')))

    def run(self):
        has_npm = self.has_npm()
        if not has_npm:
            log.error(
                "`npm` unavailable.  If you're running this command" +
                " using sudo, make sure `npm` is available to sudo"
            )

        env = os.environ.copy()
        env['PATH'] = npm_path

        if has_npm and self.should_run_npm():
            log.info(
                "Installing build dependencies with npm.  This may take a " +
                "while...")
            run(['npm', 'install'])
            os.utime(self.node_modules, None)

        for t in self.targets:
            if not os.path.exists(t):
                msg = "Missing file: %s" % t
                if not has_npm:
                    msg += '\nnpm is required to build a development version'
                raise ValueError(msg)

        # update package data in case this created new files
        update_package_data(self.distribution)
