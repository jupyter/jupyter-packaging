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


@fixture
def package_dir(tmpdir):
    pkg = tmpdir.mkdir('package')
    share = pkg.mkdir('share')
    jupyter = share.mkdir('jupyter')
    foo = jupyter.mkdir('jupyter_packaging_test_foo')
    foo.join('test.txt').write('hello, world!')
    pkg.join('jupyter_packaging_test_foo.py').write('print("hello, world!")')
    pkg.join('MANIFEST.in').write('recursive-include share *.*')
    pkg.join('setup.py').write("""
from jupyter_packaging import create_cmdclass
import setuptools
import os


name = "jupyter_packaging_test_foo"
HERE = os.path.abspath(os.path.dirname(__file__))
share_path = os.path.join(HERE, "share", "jupyter", name)

data_files_spec = [
    ("share/jupyter/%s" % name, share_path,  "*.txt"),
]


cmdclass = create_cmdclass( 
    data_files_spec=data_files_spec
)
    
setup_args = dict(
    name=name,
    version="foo version",
    url="foo url",
    author="foo author",
    description="foo package",
    long_description="long_description",
    long_description_content_type="text/markdown",
    cmdclass= cmdclass,
    packages=setuptools.find_packages(),
    zip_safe=False,
    py_modules=["jupyter_packaging_test_foo"],
    include_package_data=True
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)
""")
    return pkg

