"""Generate or verify hashes for every tracked file except SHA256SUMS itself."""
import argparse
import hashlib
from pathlib import Path
import subprocess

def main(check):
    root=Path(__file__).resolve().parents[1]
    paths=subprocess.check_output(["git","ls-files","-z"],cwd=root).decode().split("\0")
    paths=sorted(p for p in paths if p and p != "SHA256SUMS")
    text="".join(f"{hashlib.sha256((root/p).read_bytes()).hexdigest()}  {p}\n" for p in paths)
    manifest=root/"SHA256SUMS"
    if check:
        if manifest.read_text(encoding="utf-8") != text:
            raise SystemExit("Integrity manifest mismatch or tracked-file set changed")
        print(f"PASS: {len(paths)} tracked files")
    else:
        manifest.write_text(text,encoding="utf-8",newline="\n")
        print(f"Wrote {len(paths)} entries")

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--check",action="store_true")
    main(p.parse_args().check)
