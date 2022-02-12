from jupyter_packaging.setupbase import is_stale


def test_destination_is_not_stale(source_dir, destination_dir):
    assert is_stale(str(destination_dir), str(source_dir)) is False


def test_root_file_causes_stale(source_dir, destination_dir):
    source_dir.join("file1.txt").setmtime(30000)
    assert is_stale(str(destination_dir), str(source_dir)) is True


def test_sub_file_causes_stale(source_dir, destination_dir):
    source_dir.join("sub", "subfile2.txt").setmtime(30000)
    assert is_stale(str(destination_dir), str(source_dir)) is True


def test_folder_mtime_does_not_prevent_stale(source_dir, destination_dir):
    source_dir.join("sub", "subfile2.txt").setmtime(30000)
    destination_dir.setmtime(40000)
    destination_dir.join("sub").setmtime(40000)
    destination_dir.setmtime(40000)
    assert is_stale(str(destination_dir), str(source_dir)) is True


def test_folder_mtime_does_not_cause_stale(source_dir, destination_dir):
    source_dir.setmtime(40000)
    source_dir.join("sub").setmtime(40000)
    source_dir.setmtime(40000)
    assert is_stale(str(destination_dir), str(source_dir)) is False


# This behavior might not always be wanted?
# The alternative is to check whether ALL files in destination is newer
# than the newest file in source (more conservative).
def test_only_newest_files_determine_stale(source_dir, destination_dir):
    source_dir.join("file1.txt").setmtime(30000)
    destination_dir.join("file1.rtf").setmtime(40000)
    assert is_stale(str(destination_dir), str(source_dir)) is False


def test_unstale_on_equal(source_dir):
    assert is_stale(str(source_dir), str(source_dir)) is False


def test_file_vs_dir(source_dir, destination_dir):
    assert is_stale(str(destination_dir.join("file1.rtf")), str(source_dir)) is False
    source_dir.join("file2.txt").setmtime(30000)
    assert is_stale(str(destination_dir.join("file1.rtf")), str(source_dir)) is True


def test_dir_vs_file(source_dir, destination_dir):
    assert is_stale(str(destination_dir), str(source_dir.join("file1.txt"))) is False
    source_dir.join("file1.txt").setmtime(30000)
    assert is_stale(str(destination_dir), str(source_dir.join("file1.txt"))) is True


def test_file_vs_file(source_dir, destination_dir):
    assert (
        is_stale(
            str(destination_dir.join("file1.rtf")), str(source_dir.join("file1.txt"))
        )
        is False
    )
    source_dir.join("file1.txt").setmtime(30000)
    assert (
        is_stale(
            str(destination_dir.join("file1.rtf")), str(source_dir.join("file1.txt"))
        )
        is True
    )


def test_empty_dir(source_dir, tmpdir):
    empty_dir = tmpdir.mkdir("empty")
    assert is_stale(str(empty_dir), str(source_dir)) is True
    assert is_stale(str(source_dir), str(empty_dir)) is False
    assert is_stale(str(empty_dir), str(empty_dir)) is False
