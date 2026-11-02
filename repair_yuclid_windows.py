"""Install the checksum-verified Boost 1.88 runtime for py-yuclid on Windows.

Run with this project's .venv Python. The original wheel executable is retained
as yuclid.original.exe so the import-name patch can be reapplied safely.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE_NAME = "libboost-1.88.0-h9dfe17d_7.conda"
URL = f"https://conda.anaconda.org/conda-forge/win-64/{PACKAGE_NAME}"
SHA256 = "fad63bb3b722d4fc50c8258fc30402970ad36baf73edd87c1b647bdd6aed3f04"
BOOST_NAMES = ("boost_log_setup", "boost_log", "boost_thread", "boost_json", "boost_program_options")


def repair(package: Path) -> None:
    scripts = HERE / ".venv" / "Scripts"
    installed = scripts / "yuclid.exe"
    original = scripts / "yuclid.original.exe"
    if not installed.is_file():
        raise FileNotFoundError(installed)
    package.parent.mkdir(parents=True, exist_ok=True)
    if not package.exists():
        urllib.request.urlretrieve(URL, package)
    if hashlib.sha256(package.read_bytes()).hexdigest() != SHA256:
        raise ValueError("Boost package SHA-256 mismatch; refusing to install")

    scratch = HERE / ".tmp" / "libboost_repair"
    scratch.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package) as archive:
        members = [name for name in archive.namelist() if name.startswith("pkg-") and name.endswith(".tar.zst")]
        if len(members) != 1:
            raise ValueError("Unexpected conda package structure")
        archive.extract(members[0], scratch)
    subprocess.run(["tar", "-xf", str(scratch / members[0]), "-C", str(scratch)], check=True)
    dlls = list((scratch / "Library" / "bin").glob("boost_*.dll"))
    if len(dlls) < 5:
        raise ValueError("Boost runtime DLLs missing from the package")

    if not original.exists():
        shutil.copy2(installed, original)
    data = original.read_bytes()
    for name in BOOST_NAMES:
        old = (name + "-vc143-mt-x64-1_88.dll").encode("ascii")
        new = (name + ".dll").encode("ascii")
        if data.count(old) != 1:
            raise ValueError(f"Expected exactly one {old.decode()} import in original Yuclid executable")
        data = data.replace(old, new + b"\0" * (len(old) - len(new)))
    for dll in dlls:
        shutil.copy2(dll, scripts / dll.name)
    installed.write_bytes(data)
    smoke = subprocess.run([str(installed), "--help"], capture_output=True, text=True)
    if smoke.returncode or "Allowed options" not in smoke.stdout:
        raise RuntimeError(f"Yuclid still fails to start (exit {smoke.returncode})")
    print(f"Yuclid Windows runtime repaired: {installed}")
    print(f"Boost package SHA-256 verified: {SHA256}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=HERE / ".tmp" / PACKAGE_NAME,
                        help="Optional predownloaded conda-forge package")
    repair(parser.parse_args().package)
