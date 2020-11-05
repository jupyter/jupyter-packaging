# jupyter-packaging

Tools to help build and install Jupyter Python packages

## Install

`pip install jupyter-packaging`

## Usage

There are two ways to use `jupyter-packaging` in another package.

The first to use a `pyproject.toml` file as outlined in [pep-518](https://www.python.org/dev/peps/pep-0518/).
An example:

```
[build-system]
requires = ["jupyter_packaging~=0.6.0", "jupyterlab~=2.0", "setuptools>=40.8.0", "wheel"]
build-backend = "setuptools.build_meta"
```

The second method is to vendor `setupbase.py` locally alongside `setup.py` and import the helpers from `setupbase`.

Below is an example `setup.py` that uses the `pyproject.toml` approach:

```py
from setuptools import setup
from jupyter_packaging import create_cmdclass, install_npm


cmdclass = create_cmdclass(['js'])
cmdclass['js'] = install_npm()

setup_args = dict(
    name             = 'PROJECT_NAME',
    description      = 'PROJECT_DESCRIPTION',
    long_description = 'PROJECT_LONG_DESCRIPTION',
    version          = 'PROJECT_VERSION',
    author           = 'Jupyter Development Team',
    author_email     = 'jupyter@googlegroups.com',
    url              = 'http://jupyter.org',
    license          = 'BSD',
    platforms        = "Linux, Mac OS X, Windows",
    keywords         = ['ipython', 'jupyter'],
    classifiers      = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass         = cmdclass,
    install_requires = [
        'notebook>=4.3.0',
    ]
)

if __name__ == '__main__':
    setup(**setup_args)
```

## Development Install

```
git clone https://github.com/jupyter/jupyter-packaging.git
cd jupyter-packaging
pip install -e .
```

You can test changes locally by creating a `pyproject.toml` with the following, replacing the local path to the git checkout:

```
[build-system]
requires = ["jupyter_packaging@file://<path-to-git-checkout>", "setuptools>=40.8.0", "wheel"]
build-backend = "setuptools.build_meta"
```