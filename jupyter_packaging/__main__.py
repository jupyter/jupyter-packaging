#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
"""
Copies jupyter-packaging's setupbase.py to the specified directory.
If no directory is given, it uses the current directory.
"""

import argparse
import os
import shutil


def check_dir(dirpath):
    if not os.path.isdir(dirpath):
        raise argparse.ArgumentTypeError(
            'Given path is not a directory: %s' % dirpath)
    return os.path.abspath(dirpath)


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'destination', type=check_dir, default='.', nargs='?',
        help="The directory to copy setupbase.py to.",
        )

    args = parser.parse_args(args)

    here = os.path.dirname(__file__)
    source = os.path.join(here, 'setupbase.py')
    destination = args.destination

    shutil.copy(source, destination)


if __name__ == '__main__':
    main()
