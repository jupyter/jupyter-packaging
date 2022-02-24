# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import importlib
from pathlib import Path
import sys

from flit.buildapi import (
    get_requires_for_build_wheel,
    get_requires_for_build_sdist,
    prepare_metadata_for_build_wheel,
    build_sdist as orig_build_sdist,
    build_wheel as orig_build_wheel,
    build_editable as orig_build_editable,
)
import tomli


VERSION = "0.11.1"

# PEP 517 specifies that the CWD will always be the source tree
pyproj_toml = Path("pyproject.toml")


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """Build a wheel with an optional pre-build step."""
    builder = _get_build_func()
    if builder:
        builder()
    _replace_keys()
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
    _replace_keys()
    val = orig_build_sdist(sdist_directory, config_settings=config_settings)
    _ensure_targets()
    return val


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    """Build in editable mode pre-build step."""
    builder = _get_build_func("editable-build") or _get_build_func("build")
    if builder:
        builder()
    _replace_keys()
    val = orig_build_editable(
        wheel_directory,
        config_settings=config_settings,
        metadata_directory=metadata_directory,
    )
    _ensure_targets()
    return val


def _get_build_func(prefix="build"):
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        return
    target = prefix + "er"

    data = tomli.loads(pyproject.read_text(encoding="utf-8"))
    if "tool" not in data:
        return
    if "jupyter-packaging" not in data["tool"]:
        return
    if target not in data["tool"]["jupyter-packaging"]:
        return
    section = data["tool"]["jupyter-packaging"]

    if "factory" not in section[target]:
        raise ValueError(f"Missing `factory` specifier for {target}")

    factory_data = section[target]["factory"]
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
    kwargs = section.get(f"{prefix}-args", {})
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


def _replace_keys():
    if not pyproj_toml.exists():
        return
    data = pyproj_toml.read_text(encoding="utf-8")
    before = "[tool][jupyter-packaging][external-data]"
    after = "[tool][flit][external-data]"
    data = data.replace(before, after)
    pyproj_toml.write_text(data, encoding="utf-8")
