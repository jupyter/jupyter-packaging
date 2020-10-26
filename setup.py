#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
import os
from setuptools import setup
from jupyter_packaging.setupbase import (
    create_cmdclass, find_packages, __version__
)

here = os.path.dirname(os.path.abspath(__file__))

setup_args = dict(
    name            = 'jupyter-packaging',
    version         = __version__,
    packages        = find_packages(here),
    description     = "Jupyter Packaging Utilities",
    long_description= """
    This package contains utilities for making Python packages with
    and without accompanying JavaScript packages.
    """,
    long_description_content_type='text/x-rst',
    author          = 'Jupyter Development Team',
    author_email    = 'jupyter@googlegroups.com',
    url             = 'http://jupyter.org',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'Packaging'],
    cmdclass        = create_cmdclass(),
    python_requires = '>=3.6',
    install_requires = "packaging",
    extras_require  = {
        'test': [
            'pytest'
        ],
    },
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)
