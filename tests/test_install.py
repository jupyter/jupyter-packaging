import subprocess
from pathlib import Path
import sys
import sysconfig

from .utils import site_packages_readonly

import pytest


@pytest.mark.skipif(site_packages_readonly, reason="Site Packages are Read-only")
def test_install(make_package, tmp_path):
    name = "jupyter_packaging_test_foo"
    ensured_targets = [f"{name}/main.py"]
    package_dir = make_package(name=name, ensured_targets=ensured_targets)
    subprocess.check_output(
        [sys.executable, "-m", "pip", "install", "."], cwd=str(package_dir)
    )
    # Get site packages where the package is installed.
    sitepkg = Path(sysconfig.get_paths()["purelib"])
    installed_file = sitepkg / f"{name}/main.py"
    assert installed_file.exists()
    excluded_file = sitepkg / f"{name}/exclude.py"
    assert not excluded_file.exists()
    subprocess.check_output(
        [sys.executable, "-m", "pip", "uninstall", name, "-y"], cwd=str(package_dir)
    )
    assert not installed_file.exists()


@pytest.mark.skipif(site_packages_readonly, reason="Site Packages are Read-only")
def test_install_hybrid(make_hybrid_package, tmp_path):
    name = "jupyter_packaging_test_foo"
    ensured_targets = [f"{name}/main.py", f"{name}/generated.js"]
    package_dir = make_hybrid_package(
        name=name,
        ensured_targets=ensured_targets,
        skip_if_exists=[f"{name}/generated.js"],
    )
    subprocess.check_output(
        [sys.executable, "-m", "pip", "install", "."], cwd=str(package_dir)
    )
    # Get site packages where the package is installed.
    sitepkg = Path(sysconfig.get_paths()["purelib"])
    installed_py_file = sitepkg / f"{name}/main.py"
    installed_js_file = sitepkg / f"{name}/generated.js"
    assert installed_py_file.exists()
    assert installed_js_file.exists()
    content = installed_js_file.read_text(encoding="utf-8")
    Path(f"{package_dir}/{name}/generated.js").write_text(content, encoding="utf-8")
    excluded_file = sitepkg / f"{name}/exclude.py"
    assert not excluded_file.exists()
    subprocess.check_output(
        [sys.executable, "-m", "pip", "install", "."], cwd=str(package_dir)
    )
    assert content == installed_js_file.read_text(encoding="utf-8")
    subprocess.check_output(
        [sys.executable, "-m", "pip", "uninstall", name, "-y"], cwd=str(package_dir)
    )
    assert not installed_py_file.exists()
    assert not installed_js_file.exists()


@pytest.mark.skipif(site_packages_readonly, reason="Site Packages are Read-only")
def test_install_missing(make_package, tmp_path):
    name = "jupyter_packaging_test_foo"
    ensured_targets = [f"{name}/missing.py"]
    package_dir = make_package(name=name, ensured_targets=ensured_targets)
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_output(
            [sys.executable, "-m", "pip", "install", "."], cwd=str(package_dir)
        )
    subprocess.check_output(
        [sys.executable, "-m", "pip", "install", "-e", "."], cwd=str(package_dir)
    )
