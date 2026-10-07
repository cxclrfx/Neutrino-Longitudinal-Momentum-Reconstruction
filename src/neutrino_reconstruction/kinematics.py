"""Four-vector helpers. Momenta and energies are in GeV, angles in radians."""
import math

def muon_four_vector(pt, eta, phi, mass):
    et = math.hypot(mass, pt)
    pz = pt * math.sinh(eta)
    return math.hypot(et, pz), pt * math.cos(phi), pt * math.sin(phi), pz, et

def invariant_mass_squared(e_mu, px_mu, py_mu, pz_mu, px_nu, py_nu, pz_nu, muon_mass):
    """Unsquared physical constraint, evaluated independently of the quadratic."""
    e_nu = math.hypot(px_nu, py_nu, pz_nu)
    return muon_mass**2 + 2 * math.fsum((e_mu * e_nu, -px_mu * px_nu, -py_mu * py_nu, -pz_mu * pz_nu))
