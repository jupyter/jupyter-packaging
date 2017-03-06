#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
from os.path import join as pjoin
import shutil

from setuptools.cmd import Command
from setuptools.command import (
    build_py, sdist, develop, bdist_egg
)
from distutils import log
from subprocess import check_call
import sys

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None

here = os.path.abspath(os.path.dirname(sys.argv[0]))
is_repo = os.path.exists(pjoin(here, '.git'))
node_modules = pjoin(here, 'node_modules')
npm_path = ':'.join([
    pjoin(here, 'node_modules', '.bin'),
    os.environ.get('PATH', os.defpath),
])

# ---------------------------------------------------------------------------
# Public Functions
# ---------------------------------------------------------------------------


def get_data_files(top):
    """Get data files"""

    data_files = []
    ntrim = len(here + os.path.sep)

    for (d, dirs, filenames) in os.walk(top):
        data_files.append((
            d[ntrim:],
            [pjoin(d, f) for f in filenames]
        ))
    return data_files


def find_packages(top):
    """
    Find all of the packages.
    """
    packages = []
    for d, _, _ in os.walk(top):
        if os.path.exists(pjoin(d, '__init__.py')):
            packages.append(d.replace(os.path.sep, '.'))


def create_cmdclass(wrappers=None):
    """Create a command class with the given optional wrappers.

    Parameters
    ----------
    wrappers: list(str), optional
        The cmdclass names to run before running other commands
    """
    egg = bdist_egg if 'bdist_egg' in sys.argv else bdist_egg_disabled
    wrappers = wrappers or []
    cmdclass = dict(
        build_py=wrap_command(build_py, wrappers, strict=is_repo),
        sdist=wrap_command(sdist, strict=True),
        bdist_egg=egg,
        develop=wrap_command(develop, wrappers, strict=True)
    )
    if bdist_wheel:
        cmdclass['bdist_wheel'] = wrap_command(bdist_wheel, wrappers)
    return cmdclass


def mtime(path):
    """shorthand for mtime"""
    return os.stat(path).st_mtime


def should_run_npm():
    """Test whether npm should be run"""
    if not shutil.which('npm'):
        log.error("npm unavailable")
        return False
    if not os.path.exists(node_modules):
        return True
    return mtime(node_modules) < mtime(pjoin(here, 'package.json'))


def run_npm():
    """Run npm install"""
    log.info("Installing build dependencies with npm")
    check_call(['npm', 'install', '--progress=false'], cwd=here)
    os.utime(node_modules)
    env = os.environ.copy()
    env['PATH'] = npm_path


class BaseCommand(Command):
    """Dumb empty command because Command needs subclasses to override too much"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def get_inputs(self):
        return []

    def get_outputs(self):
        return []


# ---------------------------------------------------------------------------
# Private Functions
# ---------------------------------------------------------------------------


def wrap_command(cls, cmds, strict=True):
    """Wrap a setup command

    Parameters
    ----------
    cmds: list(str)
        The names of the other commands to run prior to the command.
    strict: boolean, optional
        Wether to raise errors when a pre-command fails.
    """
    class Command(cls):

        def run(self):
            if not getattr(self, 'uninstall'):
                try:
                    [self.run_command(cmd) for cmd in cmds]
                except Exception:
                    if strict:
                        raise
                    else:
                        pass
            return super().run()
    return Command


class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg
    Prevents setup.py install performing setuptools' default easy_install,
    which it should never ever do.
    """

    def run(self):
        sys.exit("Aborting implicit building of eggs. Use `pip install .` " +
                 " to install from source.")

