"""Install checksum-pinned released CLI bytes for offline contract checks."""
import argparse
import hashlib
from pathlib import Path
import platform
import tarfile
import urllib.request


ASSETS = {
    ("Linux", "x86_64"): ("linux_amd64", "c0ca0874b9fafe2e99011496135d944f807beb966b945785f6571ae6db749c6f"),
    ("Darwin", "arm64"): ("darwin_arm64", "34d464f027626a12df1e505efa80a83d54a2c77d069f63edbecec005461e6278"),
}


def install(destination):
    asset, expected = ASSETS[(platform.system(), platform.machine())]
    url = f"https://github.com/antaeusio/antaeus/releases/download/v0.7.0/antaeus_0.7.0_{asset}.tar.gz"
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as response:
        raw = response.read(16 * 1024 * 1024 + 1)
    if len(raw) > 16 * 1024 * 1024 or hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError("released CLI checksum/size mismatch")
    archive = destination / "release.tar.gz"
    archive.write_bytes(raw)
    with tarfile.open(archive) as release:
        release.extractall(destination, filter="data")
    binary = destination / f"antaeus_0.7.0_{asset}" / "antaeus"
    if not binary.is_file() or binary.is_symlink():
        raise ValueError("released CLI missing")
    return binary.resolve()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", default=".tmp/cli-v0.7.0")
    print(install(parser.parse_args().dir))
