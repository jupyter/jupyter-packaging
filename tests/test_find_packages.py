
import os

import pytest

from jupyter_packaging.setupbase import find_packages


here = os.path.dirname(__file__)
root = os.path.join(here, os.pardir)


def test_finds_itself():
    with pytest.warns(DeprecationWarning):
        assert ['jupyter_packaging'] == find_packages(root)


def test_finds_subpackages(tmpdir):
    a = tmpdir.mkdir('packageA')
    sub_a1 = a.mkdir('sub1')
    sub_a2 = a.mkdir('sub2')
    b = tmpdir.mkdir('packageB')
    sub_b1 = b.mkdir('sub1')
    sub_b2 = b.mkdir('sub2')
    for d in (a, sub_a1, sub_a2, b, sub_b1, sub_b2):
        d.join('__init__.py').write('')
    # using sets ensure order won't matter
    expected = set([
        'packageA', 'packageA.sub1', 'packageA.sub2',
        'packageB', 'packageB.sub1', 'packageB.sub2'
    ])
    with pytest.warns(DeprecationWarning):
        found = set(find_packages(str(tmpdir)))
    assert expected == found


def test_finds_only_direct_subpackages(tmpdir):
    a = tmpdir.mkdir('packageA')
    sub_a1 = a.mkdir('sub1')
    sub_a2 = a.mkdir('sub2')
    # No __init__.py in packageA:
    for d in (sub_a1, sub_a2):
        d.join('__init__.py').write('')

    expected = []
    with pytest.warns(DeprecationWarning):
        assert expected == find_packages(str(tmpdir))
