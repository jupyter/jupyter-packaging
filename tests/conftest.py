import json
import pathlib
import sys
from pytest import fixture
from subprocess import run

HERE = pathlib.Path(__file__).resolve()
NAME = "jupyter_packaging_test_foo"

PACKAGE_JSON = json.dumps(
    dict(
        name="foo",
        version="0.1.0",
        scripts=dict(build=f"echo $(DATE) > {NAME}/generated.js"),
    )
)


@fixture(scope="session", autouse=True)
def clear_pip_cache():
    run([sys.executable, "-m", "pip", "cache", "remove", "jupyter_packaging"])


@fixture
def pyproject_toml():
    """A fixture that enables other fixtures to build mock packages
    with that depend on this package.
    """
    root_path = HERE.joinpath("../..").resolve()
    return f"""
[build-system]
requires = ["jupyter_packaging@file://{root_path.as_posix()}"]
build-backend = "setuptools.build_meta"
"""


setup_cfg_maker = lambda name=NAME: """
[metadata]
name = {name}
version = 0.1
author = Jupyter Development Team
author_email = jupyter@googlegroups.com
url = http://jupyter.org
description="foo package",
long_description="long_description",
long_description_content_type="text/markdown",

[options]
zip_safe = False
include_package_data = True
py_modules = foo
python_requires = >=3.6
""".format(
    name=name
)

setup_maker = lambda name=NAME, data_files_spec=None, pre_dist=None, ensured_targets=None, skip_if_exists=None, **kwargs: """
from jupyter_packaging import get_data_files, wrap_installers, npm_builder
import setuptools
import os

def exclude(filename):
    return os.path.basename(filename) == "exclude.py"

data_files=get_data_files({data_files_spec}, exclude=exclude)

cmdclass = wrap_installers(pre_dist={pre_dist}, ensured_targets={ensured_targets}, skip_if_exists={skip_if_exists})

setuptools.setup(data_files=data_files, cmdclass=cmdclass, {setup_args})
""".format(
    name=name,
    data_files_spec=data_files_spec,
    pre_dist=pre_dist or "lambda: print",
    ensured_targets=ensured_targets or [],
    skip_if_exists=skip_if_exists or [],
    setup_args="".join(
        ["{}={},\n\t".format(key, str(val)) for key, val in kwargs.items()]
    ),
)

setup_maker_deprecated = lambda name=NAME, data_files_spec=None, pre_dist=None, ensured_targets=None, **kwargs: """
from jupyter_packaging import create_cmdclass, install_npm
import setuptools
import os

def exclude(filename):
    return os.path.basename(filename) == "exclude.py"


cmdclass = create_cmdclass('jsdeps', data_files_spec={data_files_spec}, exclude=exclude)
cmdclass['jsdeps'] = install_npm()

setuptools.setup(cmdclass=cmdclass, {setup_args})
""".format(
    name=name,
    data_files_spec=data_files_spec,
    setup_args="".join(
        ["{}={},\n\t".format(key, str(val)) for key, val in kwargs.items()]
    ),
)


def make_package_base(
    tmp_path, pyproject_toml, setup_func=setup_maker, include_js=False
):
    def do_stuff(
        name=NAME,
        data_files=None,
        data_files_spec=None,
        ensured_targets=None,
        skip_if_exists=None,
        py_module=False,
    ):
        # Create the package directory.
        pkg = tmp_path.joinpath("package")
        pkg.mkdir()

        # What type of a package is this, single module or nested package?
        setup_args = {}
        if py_module:
            setup_args.update({"py_module": [NAME]})
            pkg.joinpath(f"{NAME}_foo.py").write_text('print("hello, world!")')
            pkg.joinpath("MANIFEST.in").write_text("recursive-include share *.*")
        else:
            setup_args.update({"packages": "setuptools.find_packages('.')"})
            mod = pkg.joinpath(NAME)
            mod.mkdir()
            mod.joinpath("__init__.py").write_text("")
            mod.joinpath("main.py").write_text('print("hello, world!")')
            # path that is meant to be excluded
            mod.joinpath("exclude.py")
            pkg.joinpath("MANIFEST.in").write_text("recursive-include share *.*")

        # Fill the package with content.
        # 1. Add a setup.py
        setuppy = pkg.joinpath("setup.py")
        # Pass the data_file spec to the setup.py
        pre_dist = None
        if include_js:
            pre_dist = "npm_builder()"
        setup_content = setup_func(
            name=name,
            data_files_spec=data_files_spec,
            ensured_targets=ensured_targets,
            skip_if_exists=skip_if_exists,
            pre_dist=pre_dist,
            **setup_args,
        )
        setuppy.write_text(setup_content)

        # 2. Add pyproject.toml to package.
        pkg.joinpath("pyproject.toml").write_text(pyproject_toml)

        # 3. Add setup.cfg to package.
        pkg.joinpath("setup.cfg").write_text(setup_cfg_maker(name=name))

        # 4. Add datafiles content.
        manifest = pkg / "MANIFEST.in"
        if data_files:
            for datafile_path in data_files:
                data_file = pkg.joinpath(datafile_path)
                data_dir = data_file.parent
                data_dir.mkdir(parents=True, exist_ok=True)
                data_file.write_text("hello, world!")
                text = manifest.read_text()
                manifest.write_text(f"{text}\ninclude {datafile_path}")

        # 5. Add package.json if needed.
        if include_js:
            package_json = pkg.joinpath("package.json")
            package_json.write_text(PACKAGE_JSON, encoding="utf-8")

            text = manifest.read_text()
            manifest.write_text(f"{text}\ninclude {name}/generated.js")

        return pkg

    return do_stuff


@fixture
def make_package(tmp_path, pyproject_toml):
    """A callable fixture that creates a mock python package
    in tmp_path and returns the package directory
    """
    return make_package_base(tmp_path, pyproject_toml)


@fixture
def make_package_deprecated(tmp_path, pyproject_toml):
    """A callable fixture that creates a mock python package
    in tmp_path and returns the package directory
    """
    return make_package_base(
        tmp_path, pyproject_toml, setup_func=setup_maker_deprecated, include_js=True
    )


@fixture
def make_hybrid_package(tmp_path, pyproject_toml):
    """A callable fixture that creates a mock hybrid package
    in tmp_path and returns the package directory
    """
    return make_package_base(tmp_path, pyproject_toml, include_js=True)


@fixture
def source_dir(tmpdir):
    source = tmpdir.mkdir("source")
    source.join("file1.txt").write("original content")
    source.join("file2.txt").write("original content")
    sub = source.mkdir("sub")
    sub.join("subfile1.txt").write("original content")
    sub.join("subfile2.txt").write("original content")
    source.mkdir("node_modules")
    sub2 = source.mkdir("node_modules", "lol")
    sub2.join("index.js").write("use strict;")
    for p in source.visit():
        p.setmtime(10000)
    return source


@fixture
def destination_dir(tmpdir):
    destination = tmpdir.mkdir("destination")
    destination.join("file1.rtf").write("original content")
    destination.join("file2.rtf").write("original content")
    sub = destination.mkdir("sub")
    sub.join("subfile1.rtf").write("original content")
    sub.join("subfile2.rtf").write("original content")
    destination.mkdir("sub2")
    sub2 = destination.mkdir("sub2", "lol")
    sub2.join("static.html").write("<html><body>original content</body></html>")
    for p in destination.visit():
        p.setmtime(20000)
    return destination
