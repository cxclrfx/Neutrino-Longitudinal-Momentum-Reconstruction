"""Exact equations with an explicitly numerical boundary band (binary64)."""
from dataclasses import dataclass
import math
import sys
from .constants import MUON_MASS_GEV, W_MASS_GEV
from .kinematics import muon_four_vector

@dataclass(frozen=True)
class Reconstruction:
    px_mu_gev: float
    py_mu_gev: float
    pz_mu_gev: float
    e_mu_gev: float
    et_mu_gev: float
    px_nu_gev: float
    py_nu_gev: float
    transverse_mass_gev: float
    a_gev2: float
    discriminant_gev4: float
    factored_discriminant_gev4: float
    tolerance_gev4: float
    branch_state: str
    pz_nu_plus_gev: float | None
    pz_nu_minus_gev: float | None

def reconstruct_w_to_munu(pt_mu_gev, eta_mu, phi_mu, met_gev, phi_met,
                          parent_mass_gev=W_MASS_GEV, muon_mass_gev=MUON_MASS_GEV):
    """Return both branches; never select one or alter MET.

    Domain: finite inputs, pt and MET >= 0, M > m > 0. This ensures
    A + ET*MET > 0 and avoids extraneous squared-equation solutions.
    TANGENT means |D| <= 64*epsilon*max(1, A^2, (ET*MET)^2, M^4).
    It is a numerical boundary classification, not proof of exact equality.
    Overflow / non-finite intermediates raise ValueError.
    """
    values = (pt_mu_gev, eta_mu, phi_mu, met_gev, phi_met, parent_mass_gev, muon_mass_gev)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("All inputs must be finite")
    if pt_mu_gev < 0 or met_gev < 0 or not parent_mass_gev > muon_mass_gev > 0:
        raise ValueError("Require pt >= 0, MET >= 0 and parent mass > muon mass > 0")
    try:
        em, px, py, pz, et = muon_four_vector(pt_mu_gev, eta_mu, phi_mu, muon_mass_gev)
        nx, ny = met_gev * math.cos(phi_met), met_gev * math.sin(phi_met)
        dot = pt_mu_gev * met_gev * math.cos(phi_mu - phi_met)
        mt2 = muon_mass_gev**2 + 2 * (et * met_gev - dot)
        a = (parent_mass_gev**2 - muon_mass_gev**2) / 2 + dot
        d = a*a - et*et*met_gev*met_gev
        delta = parent_mass_gev**2 - mt2
        df = 0.25 * delta * (delta + 4*et*met_gev)
        scale = max(1.0, a*a, (et*met_gev)**2, parent_mass_gev**4)
        tol = 64 * sys.float_info.epsilon * scale
        if mt2 < 0 or not all(math.isfinite(v) for v in (em, px, py, pz, et, nx, ny, mt2, a, d, df, tol)):
            raise ValueError("Unrepresentable intermediate value")
        plus = minus = None
        if d < -tol:
            state = "NO_REAL"
        elif d > tol:
            state = "TWO_REAL"
            # Vieta evaluation protects the smaller root from cancellation.
            b, s, den = a*pz, em*math.sqrt(d), et*et
            large = (b + (s if b >= 0 else -s)) / den
            product = (em*em*met_gev*met_gev - a*a) / den
            small = product / large
            plus, minus = (large, small) if b >= 0 else (small, large)
        else:
            state = "TANGENT"
            plus = minus = a*pz/(et*et)
        if plus is not None and not all(math.isfinite(v) for v in (plus, minus)):
            raise ValueError("Unrepresentable longitudinal root")
        return Reconstruction(px, py, pz, em, et, nx, ny, math.sqrt(mt2), a, d, df, tol, state, plus, minus)
    except (OverflowError, ZeroDivisionError) as exc:
        raise ValueError("Input exceeds supported floating-point range") from exc
