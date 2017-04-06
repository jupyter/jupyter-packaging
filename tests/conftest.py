from pytest import fixture


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
