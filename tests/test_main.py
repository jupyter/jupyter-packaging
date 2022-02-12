from jupyter_packaging.__main__ import main


def test_main_copies_setupbase(tmpdir):
    d = tmpdir.mkdir("sub")

    main([str(d)])
    assert d.join("setupbase.py").check()
