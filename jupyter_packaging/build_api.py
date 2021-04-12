# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import importlib
from pathlib import Path
import os
import sys

from deprecation import deprecated
from setuptools.build_meta import (
    get_requires_for_build_wheel,
    get_requires_for_build_sdist,
    prepare_metadata_for_build_wheel,
    build_sdist as orig_build_sdist,
    build_wheel as orig_build_wheel,
)
import tomlkit

from jupyter_packaging.setupbase import __version__


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """Build a wheel with an optional pre-build step."""
    builder = _get_build_func()
    if builder:
        builder()
    return orig_build_wheel(wheel_directory, config_settings=config_settings, metadata_directory=metadata_directory)


def build_sdist(sdist_directory, config_settings=None):
    """Build an sdist with an optional pre-build step."""
    builder = _get_build_func()
    if builder:
        builder()
    return orig_build_sdist(sdist_directory, config_settings=config_settings)


@deprecated(deprecated_in="0.8", removed_in="1.0", current_version=__version__,
            details="Use `factory =` instead")
def _handle_deprecated_metadata():
    pass


def _get_build_func():
    pyproject = Path('pyproject.toml')
    if not pyproject.exists():
        return
    data = tomlkit.loads(pyproject.read_text(encoding='utf-8'))
    if 'tool' not in data:
        return
    if 'jupyter-packaging' not in data['tool']:
        return
    if 'builder' not in data['tool']['jupyter-packaging']:
        return
    section = data['tool']['jupyter-packaging']

    # Handle deprecated "func" builder kwarg
    if 'func' in section['builder']:
        _handle_deprecated_metadata()
        if not 'factory' in section['builder']:
            section['builder']['factory'] = section['builder']['func']

    if 'factory' not in section['builder']:
        raise ValueError('Missing `factory` specifier for builder')

    factory_data = section['builder']['factory']
    mod_name, _, factory_name = factory_data.rpartition('.')

    # If the module fails to import, try importing as a local script
    try:
        mod = importlib.import_module(mod_name)
    except ImportError:
        try:
            sys.path.insert(0, os.getcwd())
            mod = importlib.import_module(mod_name)
        finally:
            sys.path.pop(0)

    factory = getattr(mod, factory_name)
    kwargs = section.get('build-args', {})
    return factory(**kwargs)
