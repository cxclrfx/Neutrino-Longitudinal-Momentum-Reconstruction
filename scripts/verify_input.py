"""Verify the exact CERN CSV bytes and schema before analysis."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zlib

URL = "https://opendata.cern.ch/record/5205/files/Wmunu.csv"
SHA256 = "8031d7f62935b75e02f066caf8d20e7661f98effe18dcc25b63c604bd158b04d"
HEADER = "Run,Event,pt,eta,phi,Q,chiSq,dxy,iso,MET,phiMET".split(",")

def verify(path):
    raw = Path(path).read_bytes()
    info = {"filename": "Wmunu.csv", "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "adler32": f"{zlib.adler32(raw) & 0xffffffff:08x}"}
    rows = csv.reader(io.StringIO(raw.decode("utf-8")))
    if next(rows) != HEADER:
        raise ValueError("Unexpected CSV schema")
    count = 0
    for row in rows:
        if len(row) != len(HEADER):
            raise ValueError("Malformed CSV row")
        count += 1
    info["events"] = count
    if (info["bytes"], info["adler32"], info["sha256"], count) != (7969331, "0607d5ee", SHA256, 100000):
        raise ValueError(f"Source fingerprint mismatch: {info}")
    return info

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    if args.download:
        if args.path.exists():
            raise SystemExit("Refusing to overwrite existing input; verify it without --download")
        args.path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(URL, timeout=120) as response:
            raw = response.read()
        if hashlib.sha256(raw).hexdigest() != SHA256:
            raise SystemExit("Download SHA-256 mismatch; file not saved")
        args.path.write_bytes(raw)
    print(json.dumps(verify(args.path), indent=2, sort_keys=True))
