from jupyter_packaging.setupbase import get_data_files


def test_empty_relative_path(tmpdir):
    tmpdir.mkdir("sub1").join("a.json").write("")
    tmpdir.mkdir("sub2").join("b.json").write("")
    spec = [("my/target", "", "**/*.json")]
    res = get_data_files(spec, top=str(tmpdir))
    assert sorted(res) == [
        ("my/target/sub1", ["sub1/a.json"]),
        ("my/target/sub2", ["sub2/b.json"]),
    ]


def test_dot_relative_path(tmpdir):
    tmpdir.mkdir("sub1").join("a.json").write("")
    tmpdir.mkdir("sub2").join("b.json").write("")
    spec = [("my/target", ".", "**/*.json")]
    res = get_data_files(spec, top=str(tmpdir))
    assert sorted(res) == [
        ("my/target/sub1", ["sub1/a.json"]),
        ("my/target/sub2", ["sub2/b.json"]),
    ]


def test_subdir_relative_path(tmpdir):
    tmpdir.mkdir("sub1").join("a.json").write("")
    tmpdir.mkdir("sub2").join("b.json").write("")
    spec = [("my/target", "sub1", "**/[a-z].json")]
    res = get_data_files(spec, top=str(tmpdir))
    assert sorted(res) == [
        ("my/target", ["sub1/a.json"]),
    ]


def test_root_absolute_path(tmpdir):
    tmpdir.mkdir("sub1").join("a.json").write("")
    tmpdir.mkdir("sub2").join("b.json").write("")
    spec = [("my/target", str(tmpdir), "**/*.json")]
    res = get_data_files(spec, top=str(tmpdir))
    assert sorted(res) == [
        ("my/target/sub1", ["sub1/a.json"]),
        ("my/target/sub2", ["sub2/b.json"]),
    ]


def test_subdir_absolute_path(tmpdir):
    tmpdir.mkdir("sub1").join("a.json").write("")
    tmpdir.mkdir("sub2").join("b.json").write("")
    spec = [("my/target", str(tmpdir.join("sub1")), "**/*.json")]
    res = get_data_files(spec, top=str(tmpdir))
    assert sorted(res) == [
        ("my/target", ["sub1/a.json"]),
    ]


def test_absolute_trailing_slash(tmpdir):
    maindir = tmpdir.mkdir("main")
    maindir.mkdir("sub1").join("a.json").write("")
    maindir.mkdir("sub2").join("b.json").write("")
    spec = [("my/target/", str(tmpdir) + "/", "**/*.*")]
    res = get_data_files(spec, top=str(tmpdir))
    assert sorted(res) == [
        ("my/target/main/sub1", ["main/sub1/a.json"]),
        ("my/target/main/sub2", ["main/sub2/b.json"]),
    ]


def test_relative_trailing_slash(tmpdir):
    maindir = tmpdir.mkdir("main")
    maindir.mkdir("sub1").join("a.json").write("")
    maindir.mkdir("sub2").join("b.json").write("")
    spec = [("my/target/", "main/", "**/*.json")]
    res = get_data_files(spec, top=str(tmpdir))
    assert sorted(res) == [
        ("my/target/sub1", ["main/sub1/a.json"]),
        ("my/target/sub2", ["main/sub2/b.json"]),
    ]


def test_nested_source_dir(tmpdir):
    maindir = tmpdir.mkdir("main")
    maindir.mkdir("sub1").join("a.json").write("")
    maindir.mkdir("sub2").join("b.json").write("")
    spec = [("my/target", "main/sub1", "a.json")]
    res = get_data_files(spec, top=str(tmpdir))
    assert sorted(res) == [
        ("my/target", ["main/sub1/a.json"]),
    ]
