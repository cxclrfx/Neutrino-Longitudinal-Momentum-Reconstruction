"""Reproduce all events, both roots, and numerical validation; no event cuts."""
import argparse
from collections import Counter
import csv
from dataclasses import asdict
import json
import hashlib
import math
from pathlib import Path
from neutrino_reconstruction import reconstruct_w_to_munu, MUON_MASS_GEV
from neutrino_reconstruction.kinematics import invariant_mass_squared
from verify_input import verify

def reproduce(source, output, mass):
    fingerprint = verify(source)
    output.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    max_identity = max_shell = max_shell_scaled = 0.0
    min_mt, max_mt = math.inf, -math.inf
    with source.open(newline="") as inp, (output/"events.csv").open("w", newline="") as out:
        writer = None
        for row in csv.DictReader(inp):
            r = reconstruct_w_to_munu(*(float(row[k]) for k in ("pt", "eta", "phi", "MET", "phiMET")), parent_mass_gev=mass)
            counts[r.branch_state] += 1
            scale = max(1, r.a_gev2**2, (r.et_mu_gev*float(row["MET"]))**2, mass**4)
            identity = abs(r.discriminant_gev4-r.factored_discriminant_gev4)/scale
            if identity > 1e-12:
                raise RuntimeError("Discriminant identity failed")
            max_identity = max(max_identity, identity)
            delta = mass**2 - r.transverse_mass_gev**2
            if r.branch_state != "TANGENT" and ((r.discriminant_gev4 > 0) != (delta > 0)):
                raise RuntimeError("Boundary sign mismatch")
            for root in (r.pz_nu_plus_gev, r.pz_nu_minus_gev):
                if root is None:
                    continue
                shell = invariant_mass_squared(r.e_mu_gev, r.px_mu_gev, r.py_mu_gev, r.pz_mu_gev, r.px_nu_gev, r.py_nu_gev, root, MUON_MASS_GEV)
                residual = abs(shell-mass**2)
                shell_scale = max(mass**2, 2*r.e_mu_gev*math.hypot(float(row["MET"]), root))
                if residual/shell_scale > 1e-10:
                    raise RuntimeError("Physical mass-shell check failed")
                max_shell = max(max_shell, residual)
                max_shell_scaled = max(max_shell_scaled, residual/shell_scale)
            min_mt, max_mt = min(min_mt, r.transverse_mass_gev), max(max_mt, r.transverse_mass_gev)
            result = {"Run": row["Run"], "Event": row["Event"], **asdict(r)}
            if writer is None:
                writer = csv.DictWriter(out, fieldnames=result)
                writer.writeheader()
            writer.writerow(result)
    summary = {"input": fingerprint, "parent_mass_gev": mass, "muon_mass_gev": MUON_MASS_GEV,
               "counts": {k: counts[k] for k in ("TWO_REAL", "TANGENT", "NO_REAL")},
               "events": sum(counts.values()), "events_sha256": hashlib.sha256((output/"events.csv").read_bytes()).hexdigest(), "mt_min_gev": min_mt, "mt_max_gev": max_mt,
               "max_identity_scaled_error": max_identity, "identity_scaled_limit": 1e-12,
               "max_mass_shell_abs_error_gev2": max_shell, "max_mass_shell_scaled_error": max_shell_scaled,
               "mass_shell_scaled_limit": 1e-10, "validation": "PASS"}
    (output/"summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, default=Path("data/Wmunu.csv"))
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--mass", type=float, required=True)
    a = p.parse_args()
    reproduce(a.input, a.output, a.mass)
