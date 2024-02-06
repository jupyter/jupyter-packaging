# Jupyter Packaging

:warning: We recommend using [Hatch Jupyter Builder](https://github.com/jupyterlab/hatch-jupyter-builder) instead of Jupyter Packaging for new and existing projects.
See the blog post [Packaging for Jupyter in 2022](https://blog.jupyter.org/packaging-for-jupyter-in-2022-c7be64c38926).

## About

Tools to help build and install Jupyter Python packages that require a pre-build step that may include JavaScript build steps.

## Install

`pip install jupyter-packaging`

## Usage

There are three ways to use `jupyter-packaging` in another package.
In general, you should not depend on `jupyter_packaging` as a runtime dependency, only as a build dependency.

### As a Build Requirement

Use a `pyproject.toml` file as outlined in [pep-518](https://www.python.org/dev/peps/pep-0518/).
An example:

```toml
[build-system]
requires = ["jupyter_packaging>=0.10,<2"]
build-backend = "setuptools.build_meta"
```

Below is an example `setup.py` using the above config.
It assumes the rest of your metadata is in [`setup.cfg`](https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html).
We wrap the import in a try/catch to allow the file to be run without `jupyter_packaging`
so that `python setup.py` can be run directly when not building.

```py
from setuptools import setup

try:
    from jupyter_packaging import wrap_installers, npm_builder
    builder = npm_builder()
    cmdclass = wrap_installers(pre_develop=builder, pre_dist=builder)
except ImportError:
    cmdclass = {}

setup(cmdclass=cmdclass))
```

### As a Build Backend

Use the `jupyter_packaging` build backend.
The pre-build command is specified as metadata in `pyproject.toml`:

```toml
[build-system]
requires = ["jupyter_packaging>=0.10,<2"]
build-backend = "jupyter_packaging.build_api"

[tool.jupyter-packaging.builder]
factory = "jupyter_packaging.npm_builder"

[tool.jupyter-packaging.build-args]
build_cmd = "build:src"
```

The corresponding `setup.py` would be greatly simplified:

```py
from setuptools import setup
setup()
```

The `tool.jupyter-packaging.builder` section expects a `func` value that points to an importable
module and a function with dot separators.  If not given, no pre-build function will run.

The optional `tool.jupyter-packaging.build-args` sections accepts a dict of keyword arguments to
give to the pre-build command.

The build backend does not handle the `develop` command (`pip install -e .`).
If desired, you can wrap just that command:

```py
import setuptools

try:
    from jupyter_packaging import wrap_installers, npm_builder
    builder = npm_builder(build_cmd="build:dev")
    cmdclass = wrap_installers(pre_develop=builder)
except ImportError:
    cmdclass = {}

setup(cmdclass=cmdclass))
```

The optional `tool.jupyter-packaging.options` section accepts the following options:

- `skip-if-exists`: A list of local files whose presence causes the prebuild to skip
- `ensured-targets`: A list of local file paths that should exist when the dist commands are run

### As a Vendored File

Vendor `setupbase.py` locally alongside `setup.py` and import the module directly.

```py
import setuptools
from setupbase import wrap_installers, npm_builder
func = npm_builder()
cmdclass = wrap_installers(post_develop=func, pre_dist=func)
setup(cmdclass=cmdclass)
```

## Usage Notes

- This package does not work with the deprecated `python setup.py bdist_wheel` or `python setup.py sdist` commands, PyPA recommends using the [build](https://pypa-build.readthedocs.io/en/latest/index.html) package (`pip install build && python -m build .`).
- We recommend using `include_package_data=True` and `MANIFEST.in` to control the assets included in the [package](https://setuptools.readthedocs.io/en/latest/userguide/datafiles.html).
- Tools like [`check-manifest`](https://github.com/mgedmin/check-manifest) or [`manifix`](https://github.com/vidartf/manifix) can be used to ensure the desired assets are included.
- Simple uses of `data_files` can be handled in `setup.cfg` or in `setup.py`.  For more advanced usage, see below paragraph.
- Unfortunately `data_files` are not supported in `develop` mode (a limitation of `setuptools`).  You can work around it by doing a full install (`pip install .`) before the develop install (`pip install -e .`), or by adding a script to push the data files to `sys.base_prefix`.

### Advanced Data Files Usage

If the simple data_files support of `setup.cfg` is not sufficient for your needs, use `get_data_files()` from this package. The simplest use case is for including checked in files in a recursive (glob's `**` pattern) manner. In this case, set the `data_files` argument to the `setup()` function in `setup.py` to the output of the `get_data_files()` function.

If you need to include files that are generated during the build, then add the following logic to the end of your `pre_dist` command:
```python
builder = npm_builder()
def build_with_datafiles():
    builder()
    # needed as some dirs are generated as part of the build (or lazy):
    <need reference to dist here!>.data_files = get_data_files([
        ("etc/jupyter", "jupyter-config", "**/*.json"),
    ])
    
cmdclass = wrap_installers(
    pre_dist=build_with_datafiles,
)
```

## Development Install

```bash
git clone https://github.com/jupyter/jupyter-packaging.git
cd jupyter-packaging
pip install -e .[test]
pre-commit install
```

You can test changes locally by creating a `pyproject.toml` with the following, replacing the local path to the git checkout:

```toml
[build-system]
requires = ["jupyter_packaging@file://<path-to-git-checkout>"]
build-backend = "setuptools.build_meta"
```

Note: you need to run `pip cache remove jupyter_packaging` any time changes are made to prevent `pip` from using a cached version of the source.
