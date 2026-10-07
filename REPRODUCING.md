# Reproducing the study

Use Python 3.12 (tested); the core supports Python >=3.11. From the repository root,
create and activate a virtual environment using your platform's usual commands.
Install the package and optional, fully pinned figure environment:

```sh
python -m pip install .
python -m pip install -r requirements-figures.txt
python -m unittest discover -s tests -v
python scripts/verify_input.py data/Wmunu.csv --download
python scripts/reproduce_analysis.py --mass 80.3625 --output scratch/primary
python scripts/reproduce_analysis.py --mass 80.4 --output scratch/control
python scripts/independent_check.py --mass 80.3625 --output scratch/primary
python scripts/independent_check.py --mass 80.4 --output scratch/control
python scripts/generate_figures.py --results scratch/primary --output figures
python scripts/integrity.py --check
```

If the CSV already exists, omit `--download`. The last command verifies committed
bytes; plots regenerated with different platforms/font renderers can differ in bytes
without changing the physics. Review those differences before updating the manifest.
The numerical core has no external dependencies and uses deterministic binary64
operations. Small final-bit differences in math libraries are possible.

## Physical and numerical domain

The implementation requires finite inputs, nonnegative transverse momentum and
MET, and parent mass > muon mass > 0. Within that domain,
`A + ET*MET >= (M*M-m*m)/2 > 0`, because `ET >= pt` and `cos(delta_phi) >= -1`.
The quadratic was obtained by squaring
`E_mu*sqrt(MET*MET+z*z) = A + pz_mu*z`; real solutions are checked against this
original positive-energy equation, so algebraic roots are not accepted blindly.

Classification uses `tol = 64 * epsilon * max(1, A*A, (ET*MET)**2, M**4)` in GeV^4,
where epsilon is the binary64 machine epsilon. `TANGENT` is a numerical boundary
band, including tiny positive or negative D; it is not evidence of an exactly
repeated mathematical root. No general finite-precision method can certify equality
from rounded measurements. The stored unmodified D and tolerance expose this band.
For this source sample, no events enter the band at either selected mass.

Both roots are returned with the documented plus/minus labels. Vieta evaluation
reduces cancellation in the smaller root; it is algebraically equivalent to the
README formula. The longitudinal signs, including signed zero, use one consistent
predicate. No root selection or MET adjustment is performed. Inputs whose
intermediates overflow are rejected; arbitrary extreme finite inputs are not a
claim of universal numerical conditioning.

## Outputs and checks

Each `events.csv` stores original Run/Event identifiers, all reconstructed muon
and transverse neutrino components, ET, mT, A, both discriminants, the tolerance,
branch state, and both real roots. Empty roots mean no real solution.
Each `summary.json` records input hashes, both particle masses, counts, extrema,
identity residuals, physical mass-shell residuals, and the validation limits.

The identity error is divided by `max(1,A*A,(ET*MET)**2,M**4)` and must be <=1e-12.
The unsquared mass-shell error is divided by `max(M*M,2*E_mu*E_nu)` and must be
<=1e-10. Absolute residuals are also reported so a large scale does not hide them.

`independent_check.py` imports no production reconstruction code. It reconstructs
roots with 50-digit Decimal algebra from original CSV fields, compares event
identity/order and root labels, checks the positive-energy mass equation, and
recounts states. cos and sinh still use binary64; this is a separate numerical
implementation, not independent detector information or an external review.
Its root relative error limit is 1e-9 with denominator max(1,abs(root)); its physical
mass-squared residual limit is 1e-7*M*M. The source sample reused after a repair
is regression evidence, not a fresh holdout.

## Integrity

After intentional changes, stage all intended files and run
`python scripts/integrity.py`, then stage SHA256SUMS. This enumerates every tracked
artifact in sorted order, excluding SHA256SUMS itself and .git. Verification also
checks the manifest's exact path set. It protects bytes, not scientific correctness.
Source-data integrity is recorded separately in data/README.md. Scratch tables,
virtual environments, caches, and downloaded data are never part of the manifest.
