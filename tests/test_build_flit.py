import os
from pathlib import Path
import sys
from subprocess import check_call
from unittest.mock import patch

import pytest

from jupyter_packaging.build_flit import build_wheel, build_sdist, build_editable


TOML_CONTENT = """
[project]
name = "foo"
version = "0.1.0"
description = "foo package"

[tool.jupyter-packaging.builder]
factory = "foo.main"

[tool.jupyter-packaging.build-args]
fizz = "buzz"
"""

DATA_CONTENT = """
[tool.jupyter-packaging.external-data]
directory = "data"
"""

FOO_CONTENT = r"""
from pathlib import Path
def main(fizz=None):
    Path('foo.txt').write_text(f'fizz={fizz}', encoding='utf-8')
"""

BAD_CONTENT = """
[tool.jupyter-packaging.builder]
bar = "foo.main"
"""

ENSURED_CONTENT = """
[tool.jupyter-packaging.options]
ensured-targets = ["foo.txt"]
"""

SKIP_IF_EXISTS = """
[tool.jupyter-packaging.options]
skip-if-exists = ["foo.txt"]
"""


def test_build_wheel_no_toml(tmp_path):
    os.chdir(tmp_path)
    orig_wheel = patch("jupyter_packaging.build_flit.orig_build_wheel")
    build_wheel(tmp_path)
    orig_wheel.assert_called_with(
        tmp_path, config_settings=None, metadata_directory=None
    )


def test_build_wheel(tmp_path, mocker):
    os.chdir(tmp_path)
    tmp_path.joinpath("foo.py").write_text(FOO_CONTENT)
    tmp_path.joinpath("pyproject.toml").write_text(
        TOML_CONTENT + DATA_CONTENT + ENSURED_CONTENT, encoding="utf-8"
    )
    orig_wheel = mocker.patch("jupyter_packaging.build_flit.orig_build_wheel")
    build_wheel(tmp_path)
    orig_wheel.assert_called_with(
        tmp_path, config_settings=None, metadata_directory=None
    )
    data = tmp_path.joinpath("foo.txt").read_text(encoding="utf-8")
    assert data == "fizz=buzz"

    content = TOML_CONTENT.replace("buzz", "fizz") + SKIP_IF_EXISTS
    tmp_path.joinpath("pyproject.toml").write_text(content, encoding="utf-8")
    build_wheel(tmp_path)
    data = tmp_path.joinpath("foo.txt").read_text(encoding="utf-8")
    assert data == "fizz=buzz"


def test_build_wheel_bad_toml(tmp_path, mocker):
    os.chdir(tmp_path)
    tmp_path.joinpath("foo.py").write_text(FOO_CONTENT)
    tmp_path.joinpath("pyproject.toml").write_text(BAD_CONTENT, encoding="utf-8")
    orig_wheel = mocker.patch("jupyter_packaging.build_flit.orig_build_wheel")
    with pytest.raises(ValueError):
        build_wheel(tmp_path)
    orig_wheel.assert_not_called()


def test_build_wheel_no_toml(tmp_path, mocker):
    os.chdir(tmp_path)
    orig_wheel = mocker.patch("jupyter_packaging.build_flit.orig_build_wheel")
    build_wheel(tmp_path)
    orig_wheel.assert_called_with(
        tmp_path, config_settings=None, metadata_directory=None
    )


def test_build_editable(tmp_path, mocker):
    os.chdir(tmp_path)
    tmp_path.joinpath("foo.py").write_text(FOO_CONTENT)
    tmp_path.joinpath("pyproject.toml").write_text(
        TOML_CONTENT + ENSURED_CONTENT, encoding="utf-8"
    )
    orig_wheel = mocker.patch("jupyter_packaging.build_flit.orig_build_wheel")
    build_wheel(tmp_path)
    orig_wheel.assert_called_with(
        tmp_path, config_settings=None, metadata_directory=None
    )
    data = tmp_path.joinpath("foo.txt").read_text(encoding="utf-8")
    assert data == "fizz=buzz"

    content = TOML_CONTENT.replace("buzz", "fizz") + SKIP_IF_EXISTS
    tmp_path.joinpath("pyproject.toml").write_text(content, encoding="utf-8")
    build_editable(tmp_path)
    data = tmp_path.joinpath("foo.txt").read_text(encoding="utf-8")
    assert data == "fizz=buzz"


def test_build_sdist(tmp_path, mocker):
    os.chdir(tmp_path)
    tmp_path.joinpath("foo.py").write_text(FOO_CONTENT)
    tmp_path.joinpath("pyproject.toml").write_text(
        TOML_CONTENT + ENSURED_CONTENT, encoding="utf-8"
    )
    orig_sdist = mocker.patch("jupyter_packaging.build_flit.orig_build_sdist")
    build_sdist(tmp_path)
    orig_sdist.assert_called_with(tmp_path, config_settings=None)
    data = tmp_path.joinpath("foo.txt").read_text(encoding="utf-8")
    assert data == "fizz=buzz"


def test_build_sdist_bad_toml(tmp_path, mocker):
    os.chdir(tmp_path)
    tmp_path.joinpath("foo.py").write_text(FOO_CONTENT)
    tmp_path.joinpath("pyproject.toml").write_text(BAD_CONTENT, encoding="utf-8")
    orig_sdist = mocker.patch("jupyter_packaging.build_flit.orig_build_sdist")
    with pytest.raises(ValueError):
        build_sdist(tmp_path)
    orig_sdist.assert_not_called()


def test_build_sdist_no_toml(tmp_path, mocker):
    os.chdir(tmp_path)
    orig_sdist = mocker.patch("jupyter_packaging.build_flit.orig_build_sdist")
    build_sdist(tmp_path)
    orig_sdist.assert_called_with(tmp_path, config_settings=None)


def test_build_package(make_package):
    package_dir = make_package()
    pyproject = package_dir / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    text = text.replace("setuptools.build_meta", "jupyter_packaging.build_flit")
    text += TOML_CONTENT
    text += DATA_CONTENT
    data_dir = package_dir / "data/etc/jupyter/jupyter_server_config.d"
    data_dir.mkdir(parents=True)
    data_file = data_dir / "jupyter_server_foo.json"
    data_file.write_text(
        '{"ServerApp": {"jpserver_extensions": {"jupyter_server_foo": true}}}"',
        encoding="utf-8",
    )
    pyproject.write_text(text, encoding="utf-8")
    package_dir.joinpath("foo.py").write_text(FOO_CONTENT, encoding="utf-8")
    check_call([sys.executable, "-m", "build"], cwd=package_dir)
    data = package_dir.joinpath("foo.txt").read_text(encoding="utf-8")
    assert data == "fizz=buzz"


def test_develop_package(make_package):
    package_dir = make_package()
    pyproject = package_dir / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    text = text.replace("setuptools.build_meta", "jupyter_packaging.build_flit")
    text += TOML_CONTENT.replace(".build", ".editable-build")
    text += DATA_CONTENT
    data_dir = package_dir / "data/etc/jupyter/jupyter_server_config.d"
    data_dir.mkdir(parents=True)
    data_file = data_dir / "jupyter_server_foo.json"
    data_file.write_text(
        '{"ServerApp": {"jpserver_extensions": {"jupyter_server_foo": true}}}"',
        encoding="utf-8",
    )
    pyproject.write_text(text, encoding="utf-8")
    package_dir.joinpath("foo.py").write_text(FOO_CONTENT, encoding="utf-8")
    check_call([sys.executable, "-m", "pip", "install", "-e", "."], cwd=package_dir)
    target = (
        Path(sys.base_prefix)
        / "etc/jupyter/jupyter_server_config.d/jupyter_server_foo.json"
    )
    assert target.exists()
