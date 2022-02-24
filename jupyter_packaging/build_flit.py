# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import importlib
from pathlib import Path
import sys

from flit.build_api import (
    get_requires_for_build_wheel,
    get_requires_for_build_sdist,
    prepare_metadata_for_build_wheel,
    build_sdist as orig_build_sdist,
    build_wheel as orig_build_wheel,
)
import tomli


VERSION = "0.11.1"


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """Build a wheel with an optional pre-build step."""
    builder = _get_build_func()
    if builder:
        builder()
    val = orig_build_wheel(
        wheel_directory,
        config_settings=config_settings,
        metadata_directory=metadata_directory,
    )
    _ensure_targets()
    return val


def build_sdist(sdist_directory, config_settings=None):
    """Build an sdist with an optional pre-build step."""
    builder = _get_build_func()
    if builder:
        builder()
    val = orig_build_sdist(sdist_directory, config_settings=config_settings)
    _ensure_targets()
    return val


def _get_build_func():
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        return
    data = tomli.loads(pyproject.read_text(encoding="utf-8"))
    if "tool" not in data:
        return
    if "jupyter-packaging" not in data["tool"]:
        return
    if "builder" not in data["tool"]["jupyter-packaging"]:
        return
    section = data["tool"]["jupyter-packaging"]

    if "factory" not in section["builder"]:
        raise ValueError("Missing `factory` specifier for builder")

    factory_data = section["builder"]["factory"]
    mod_name, _, factory_name = factory_data.rpartition(".")

    if "options" in section and "skip-if-exists" in section["options"]:
        skip_if_exists = section["options"]["skip-if-exists"]
        if all(Path(path).exists() for path in skip_if_exists):
            return None

    # If the module fails to import, try importing as a local script
    try:
        mod = importlib.import_module(mod_name)
    except ImportError:
        try:
            sys.path.insert(0, str(Path.cwd()))
            mod = importlib.import_module(mod_name)
        finally:
            sys.path.pop(0)

    factory = getattr(mod, factory_name)
    kwargs = section.get("build-args", {})
    return factory(**kwargs)


def _ensure_targets():
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        return
    data = tomli.loads(pyproject.read_text(encoding="utf-8"))
    if "tool" not in data:
        return
    if "jupyter-packaging" not in data["tool"]:
        return
    section = data["tool"]["jupyter-packaging"]
    if "options" in section and "ensured-targets" in section["options"]:
        targets = section["options"]["ensured-targets"]
        missing = [t for t in targets if not Path(t).exists()]
        if missing:
            raise ValueError(("missing files: %s" % missing))
