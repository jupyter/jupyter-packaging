# jupyter-packaging

Tools to help build and install Jupyter Python packages

## Install

`pip install jupyter-packaging`

## Usage

Below is an example `setup.py` that uses jupyter-packaging.  The 
contents of `jupyter_packaging.py` are copied locally to `setupbase.py`
so they are available to run the `setup.py` script itself.

```py
from setuptools import setup
from setupbase import create_cmdclass, install_npm


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
