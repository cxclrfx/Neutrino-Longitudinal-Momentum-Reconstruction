"""Separate 50-digit Decimal audit. Does not import the reconstruction package.

Reads original CSV and generated event rows. Transcendental cos/sinh remain
binary64; subsequent algebra and physical-root residuals use Decimal precision.
This checks implementation agreement, not detector truth or independent data.
"""
import argparse
from collections import Counter
import csv
from decimal import Decimal as D, localcontext
import itertools
import json
import hashlib
import math
from pathlib import Path
from verify_input import verify

def audit(source, results, mass):
    fingerprint = verify(source)
    summary = json.loads((results/"summary.json").read_text())
    if summary["input"] != fingerprint or summary["parent_mass_gev"] != mass or summary["muon_mass_gev"] != 0.1056583755:
        raise RuntimeError("Input or mass convention mismatch")
    digest = hashlib.sha256((results/"events.csv").read_bytes()).hexdigest()
    if digest != summary["events_sha256"]:
        raise RuntimeError("Derived event table hash mismatch")
    counts = Counter()
    max_relative_root_error = D(0)
    with localcontext() as ctx, source.open(newline="") as f, (results/"events.csv").open(newline="") as g:
        ctx.prec = 50
        m, M = D("0.1056583755"), D(str(mass))
        for raw, reported in itertools.zip_longest(csv.DictReader(f), csv.DictReader(g)):
            if raw is None or reported is None:
                raise RuntimeError("Row count mismatch")
            if (raw["Run"], raw["Event"]) != (reported["Run"], reported["Event"]):
                raise RuntimeError("Event ordering mismatch")
            pt, met = D(raw["pt"]), D(raw["MET"])
            c = D(str(math.cos(float(raw["phi"])-float(raw["phiMET"]))))
            pz = pt*D(str(math.sinh(float(raw["eta"]))))
            et2 = pt*pt+m*m
            energy = (et2+pz*pz).sqrt()
            a = (M*M-m*m)/2+pt*met*c
            disc = a*a-et2*met*met
            state = "TWO_REAL" if disc > 0 else "NO_REAL" if disc < 0 else "TANGENT"
            counts[state] += 1
            if state != reported["branch_state"]:
                raise RuntimeError("High-precision classification disagreement; inspect boundary")
            if disc >= 0:
                roots = [(a*pz+sign*energy*disc.sqrt())/et2 for sign in (1,-1)]
                for key, expected in zip(("pz_nu_plus_gev", "pz_nu_minus_gev"), roots):
                    actual = D(reported[key])
                    error = abs(actual-expected)/max(D(1),abs(expected))
                    max_relative_root_error = max(max_relative_root_error,error)
                    if error > D("1e-9"):
                        raise RuntimeError("Independent root mismatch")
                    residual = abs(m*m+2*(energy*(met*met+actual*actual).sqrt()-pt*met*c-pz*actual)-M*M)
                    if residual > D("1e-7")*M*M:
                        raise RuntimeError("Independent unsquared constraint failed")
        summary = json.loads((results/"summary.json").read_text())
        if {k:counts[k] for k in summary["counts"]} != summary["counts"]:
            raise RuntimeError("Summary count mismatch")
    report = {"status":"PASS", "events":sum(counts.values()), "counts":dict(sorted(counts.items())),
              "parent_mass_gev":mass, "events_sha256":digest, "decimal_precision":50,
              "max_relative_root_error":str(max_relative_root_error),
              "limitation":"cos and sinh evaluated in binary64; separate algebra, same source data"}
    (results/"independent-check.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps(report,indent=2))

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,default=Path("data/Wmunu.csv"))
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--mass",type=float,required=True)
    a=p.parse_args(); audit(a.input,a.output,a.mass)
