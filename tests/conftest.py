import os
import pathlib
from pytest import fixture

HERE = pathlib.Path(__file__).resolve()


@fixture
def pyproject_toml():
    """A fixture that enables other fixtures to build mock packages
    with that depend on this package.
    """
    root_path = HERE.joinpath("../..").resolve()
    return """
[build-system]
requires = ["jupyter_packaging@file://%s", "setuptools>=40.8.0", "wheel"]
build-backend = "setuptools.build_meta"
""" % str(root_path).replace(os.sep, '/')


setup = lambda name="jupyter_packaging_test_foo", data_files_spec=None, **kwargs: """
from jupyter_packaging import create_cmdclass
import setuptools
import os


name = "{name}"


def exclude(filename):
    return os.path.basename(filename) == "exclude.py"

cmdclass = create_cmdclass(
    data_files_spec={data_files_spec},
    exclude=exclude
)

setup_args = dict(
    name=name,
    version="0.1",
    url="foo url",
    author="foo author",
    description="foo package",
    long_description="long_description",
    long_description_content_type="text/markdown",
    cmdclass= cmdclass,
    zip_safe=False,
    include_package_data=True,
    {setup_args}
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)
""".format(
    name=name,
    data_files_spec=data_files_spec,
    setup_args="".join(['{}={},\n\t'.format(key, str(val)) for key, val in kwargs.items()])
)


@fixture
def make_package(tmp_path, pyproject_toml):
    """A callable fixture that creates a mock python package
    in tmp_path and returns the package directory
    """
    def stuff(
        name="jupyter_packaging_test_foo",
        data_files=None,
        data_files_spec=None,
        py_module=False
    ):
        # Create the package directory.
        pkg = tmp_path.joinpath('package')
        pkg.mkdir()

        # What type of a package is this, single module or nested package?
        setup_args = {}
        if py_module:
            setup_args.update({"py_module": ["jupyter_packaging_test_foo"]})
            pkg.joinpath('jupyter_packaging_test_foo.py').write_text('print("hello, world!")')
            pkg.joinpath('MANIFEST.in').write_text('recursive-include share *.*')
        else:
            setup_args.update({"packages": "setuptools.find_packages('.')"})
            mod = pkg.joinpath('jupyter_packaging_test_foo')
            mod.mkdir()
            mod.joinpath('__init__.py').write_text('')
            mod.joinpath('main.py').write_text('print("hello, world!")')
            # path that is meant to be excluded
            mod.joinpath("exclude.py")
            pkg.joinpath('MANIFEST.in').write_text('recursive-include share *.*')

        # Fill the package with content.
        # 1. Add a setup.py
        setuppy = pkg.joinpath("setup.py")
        # Pass the data_file spec to the setup.py
        setup_content = setup(
            name=name,
            data_files_spec=data_files_spec,
            **setup_args
        )
        setuppy.write_text(setup_content)

        # 2. Add pyproject.toml to package.
        with open(pkg.joinpath('pyproject.toml'), 'w') as fid:
            fid.write(pyproject_toml)

        # 3. Add datafiles content.
        if data_files:
            for datafile_path in data_files:
                data_file = pkg.joinpath(datafile_path)
                data_dir = data_file.parent
                data_dir.mkdir(parents=True, exist_ok=True)
                data_file.write_text("hello, world!")
        return pkg

    return stuff


@fixture
def source_dir(tmpdir):
    source = tmpdir.mkdir('source')
    source.join('file1.txt').write("original content")
    source.join('file2.txt').write("original content")
    sub = source.mkdir('sub')
    sub.join('subfile1.txt').write("original content")
    sub.join('subfile2.txt').write("original content")
    source.mkdir('node_modules')
    sub2 = source.mkdir('node_modules', 'lol')
    sub2.join('index.js').write("use strict;")
    for p in source.visit():
        p.setmtime(10000)
    return source


@fixture
def destination_dir(tmpdir):
    destination = tmpdir.mkdir('destination')
    destination.join('file1.rtf').write("original content")
    destination.join('file2.rtf').write("original content")
    sub = destination.mkdir('sub')
    sub.join('subfile1.rtf').write("original content")
    sub.join('subfile2.rtf').write("original content")
    destination.mkdir('sub2')
    sub2 = destination.mkdir('sub2', 'lol')
    sub2.join('static.html').write(
        "<html><body>original content</body></html>")
    for p in destination.visit():
        p.setmtime(20000)
    return destination
