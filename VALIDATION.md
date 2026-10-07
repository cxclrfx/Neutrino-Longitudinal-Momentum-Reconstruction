# Executed validation

Validation date: 2026-10-07. Environment: CPython 3.12, binary64; exact optional
figure-package versions are recorded in requirements-figures.txt. No benchmark
or detector-resolution claim is made.

## Results

- `python -m unittest discover -s tests -v`: **22 tests passed**.
- Official CSV bytes, schema, row count, Adler-32, and SHA-256: **PASS**.
- Full 100,000-event reproduction at 80.3625 GeV: **PASS**.
- Full 100,000-event reproduction at 80.4 GeV: **PASS**.
- Separate Decimal audit of event order, classifications, both labeled roots,
  and the unsquared physical constraint, at both masses: **PASS**.
- Figures generated from the primary result; PNG layouts visually inspected.

Evidence: [primary summary](evidence/primary-summary.json),
[control summary](evidence/control-summary.json),
[primary separate check](evidence/primary-independent-check.json),
[control separate check](evidence/control-independent-check.json), and
[unit-test report](evidence/unit-tests.json).
See REPRODUCING.md for exact commands, residual definitions and thresholds.
Per-event table hashes bind these summaries to generated event output; the tables
are reproducible scratch outputs and are not committed.

## Preserved failure and coverage

The initial 20-test suite passed but the separate Decimal check found reversed
plus/minus labels for a source event with negative-zero pseudorapidity. The physical
root set was correct, so mass-shell checks alone did not expose the labeling error.
[The original failure](evidence/development-regression.json) is retained with its
cause and counterexample. A consistent signed-zero predicate repairs the label
mapping. The final suite adds that regression and a separate synthetic signed-zero
grid. Rechecking the same CMS sample is regression evidence, not a fresh holdout
and not external independent scientific review.

Coverage includes discriminant factorization/sign, both positive-energy mass-shell
roots, exact constructed tangency and nearby resolved sides, the numerical boundary
band, branch sum/separation, rotations/reflections, zero MET/pt, a zero-root
cancellation case, non-finite and out-of-domain inputs, overflow rejection,
determinism, and both explicit mass conventions.

## Original scientific claims and limits

The algebraic factorization and physical-domain sign argument were checked against
the implementation. The CERN event count, file fingerprint, published variables,
source selection description, educational-use limitation and CC0 attribution were
verified against the official source. The stated PDG 2026 W mass was verified against
the linked review. Its world average excludes the CDF Run-II result; this project
uses the stated central value solely as a constraint, not as a new mass estimate.
The positive second factor requires the declared physical domain M > m > 0.

The supplied README's historical assertion of a completed frozen analysis could
not be independently established from a pre-existing code checkpoint: the remote
repository was empty. This repository supplies a new executed reproduction and
states its actual review status. The source selection's second-muon veto, detector
response, true neutrino pz, and true branch cannot be re-established from this
reduced CSV. They are not claimed as new empirical findings. No novelty of the
standard quadratic solution is asserted.

## Before public visibility

Perform final human scientific and licensing review, including ownership of any
future contributions before offering alternative licenses. Check GitHub CI and
rendered mathematics on the final commit. The repository must remain private until
its owner explicitly authorizes a visibility change; no release is created here.
