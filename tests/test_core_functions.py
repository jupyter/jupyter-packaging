from pathlib import Path
from unittest.mock import call

from setuptools.dist import Distribution

from jupyter_packaging.setupbase import npm_builder, wrap_installers


def test_wrap_installers():
    called = False

    def func():
        nonlocal called
        called = True

    cmd_class = wrap_installers(
        pre_dist=func, pre_develop=func, post_dist=func, post_develop=func
    )

    for name in ["pre_dist", "pre_develop", "post_dist", "post_develop"]:
        cmd_class[name](Distribution()).run()
        assert called
        called = False


def test_npm_builder(mocker):
    which = mocker.patch("jupyter_packaging.setupbase.which")
    run = mocker.patch("jupyter_packaging.setupbase.run")
    builder = npm_builder()
    which.return_value = ["foo"]
    builder()
    cwd = Path.cwd()
    run.assert_has_calls(
        [call(["npm", "install"], cwd=cwd), call(["npm", "run", "build"], cwd=cwd)]
    )


def test_npm_build_skip(mocker):
    which = mocker.patch("jupyter_packaging.setupbase.which")
    run = mocker.patch("jupyter_packaging.setupbase.run")
    mocker.patch("jupyter_packaging.setupbase.skip_npm", True)
    builder = npm_builder()
    which.return_value = ["foo"]
    builder()
    run.assert_not_called()


def test_npm_builder_yarn(tmp_path, mocker):
    which = mocker.patch("jupyter_packaging.setupbase.which")
    run = mocker.patch("jupyter_packaging.setupbase.run")
    tmp_path.joinpath("yarn.lock").write_text("hello")
    builder = npm_builder(path=tmp_path)
    which.return_value = ["foo"]
    builder()
    run.assert_has_calls(
        [
            call(["yarn", "install"], cwd=tmp_path),
            call(["yarn", "run", "build"], cwd=tmp_path),
        ]
    )


def test_npm_builder_missing_yarn(tmp_path, mocker):
    which = mocker.patch("jupyter_packaging.setupbase.which")
    run = mocker.patch("jupyter_packaging.setupbase.run")
    tmp_path.joinpath("yarn.lock").write_text("hello")
    builder = npm_builder(path=tmp_path)
    which.side_effect = ["", "foo"]
    builder()
    run.assert_has_calls(
        [
            call(["npm", "install"], cwd=tmp_path),
            call(["npm", "run", "build"], cwd=tmp_path),
        ]
    )


def test_npm_builder_not_stale(tmp_path, mocker):
    which = mocker.patch("jupyter_packaging.setupbase.which")
    run = mocker.patch("jupyter_packaging.setupbase.run")
    is_stale = mocker.patch("jupyter_packaging.setupbase.is_stale")
    is_stale.return_value = False
    builder = npm_builder(build_dir=tmp_path, source_dir=tmp_path)
    which.return_value = ["foo"]
    builder()
    run.assert_not_called()


def test_npm_builder_no_npm(mocker):
    which = mocker.patch("jupyter_packaging.setupbase.which")
    run = mocker.patch("jupyter_packaging.setupbase.run")
    is_stale = mocker.patch("jupyter_packaging.setupbase.is_stale")
    is_stale.return_value = False
    builder = npm_builder()
    which.return_value = []
    builder()
    run.assert_not_called()
