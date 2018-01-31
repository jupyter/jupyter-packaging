import os

from jupyter_packaging.setupbase import _get_data_files



def test_empty_relative_path(tmpdir):
    tmpdir.mkdir('sub1').join('a.json').write('')
    tmpdir.mkdir('sub2').join('b.json').write('')
    spec = [
        ('my/target', '', '**/*.json')
    ]
    res = _get_data_files(spec, None, str(tmpdir))
    assert sorted(res) == [
        ('my/target/sub1', ['sub1/a.json']),
        ('my/target/sub2', ['sub2/b.json']),
    ]


def test_dot_relative_path(tmpdir):
    tmpdir.mkdir('sub1').join('a.json').write('')
    tmpdir.mkdir('sub2').join('b.json').write('')
    spec = [
        ('my/target', '.', '**/*.json')
    ]
    res = _get_data_files(spec, None, str(tmpdir))
    assert sorted(res) == [
        ('my/target/sub1', ['sub1/a.json']),
        ('my/target/sub2', ['sub2/b.json']),
    ]


def test_subdir_relative_path(tmpdir):
    tmpdir.mkdir('sub1').join('a.json').write('')
    tmpdir.mkdir('sub2').join('b.json').write('')
    spec = [
        ('my/target', 'sub1', '**/*.json')
    ]
    res = _get_data_files(spec, None, str(tmpdir))
    assert sorted(res) == [
        ('my/target', ['sub1/a.json']),
    ]



def test_root_absolute_path(tmpdir):
    tmpdir.mkdir('sub1').join('a.json').write('')
    tmpdir.mkdir('sub2').join('b.json').write('')
    spec = [
        ('my/target', str(tmpdir), '**/*.json')
    ]
    res = _get_data_files(spec, None, str(tmpdir))
    assert sorted(res) == [
        ('my/target/sub1', ['sub1/a.json']),
        ('my/target/sub2', ['sub2/b.json']),
    ]


def test_subdir_absolute_path(tmpdir):
    tmpdir.mkdir('sub1').join('a.json').write('')
    tmpdir.mkdir('sub2').join('b.json').write('')
    spec = [
        ('my/target', str(tmpdir.join('sub1')), '**/*.json')
    ]
    res = _get_data_files(spec, None, str(tmpdir))
    assert sorted(res) == [
        ('my/target', ['sub1/a.json']),
    ]


