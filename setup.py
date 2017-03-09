#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
from setuptools import setup
from jupyter_packaging import __version__, create_cmdclass


setup_args = dict(
    name            = 'jupyter-packaging',
    version         = __version__,
    py_modules      = ['jupyter_packaging'],
    description     = "Jupyter Packaging Utilities",
    long_description= """
    This package contains utilities for making Python packages with
    and without accompanying JavaScript packages.
    """,
    author          = 'Jupyter Development Team',
    author_email    = 'jupyter@googlegroups.com',
    url             = 'http://jupyter.org',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'Packaging'],
    cmdclass        = create_cmdclass(),
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)
