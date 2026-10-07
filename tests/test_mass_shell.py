import math
import random
import unittest
from neutrino_reconstruction import reconstruct_w_to_munu as reconstruct, MUON_MASS_GEV

class MassShellTests(unittest.TestCase):
    def test_both_roots_unsquared_constraint(self):
        rng=random.Random(1937)
        checked=0
        for mass in (80.3625,80.4):
            for _ in range(1000):
                pt,eta,phi,met,phin=rng.uniform(25,200),rng.uniform(-2.1,2.1),rng.uniform(-3,3),rng.uniform(0,150),rng.uniform(-3,3)
                r=reconstruct(pt,eta,phi,met,phin,mass)
                if r.branch_state != "TWO_REAL":continue
                for z in (r.pz_nu_plus_gev,r.pz_nu_minus_gev):
                    # Direct four-vector contraction, no production helper.
                    en=math.sqrt(met**2+z**2)
                    m2=(r.e_mu_gev+en)**2-(r.px_mu_gev+r.px_nu_gev)**2-(r.py_mu_gev+r.py_nu_gev)**2-(r.pz_mu_gev+z)**2
                    self.assertAlmostEqual(m2,mass**2,delta=1e-6)
                    self.assertGreater(r.a_gev2+r.pz_mu_gev*z,0)
                    checked+=1
        self.assertGreater(checked,100)

    def test_branch_sum_and_separation(self):
        r=reconstruct(40,1,0,30,2)
        self.assertAlmostEqual(r.pz_nu_plus_gev+r.pz_nu_minus_gev,2*r.a_gev2*r.pz_mu_gev/r.et_mu_gev**2,places=10)
        self.assertAlmostEqual(r.pz_nu_plus_gev-r.pz_nu_minus_gev,2*r.e_mu_gev*math.sqrt(r.discriminant_gev4)/r.et_mu_gev**2,places=10)

    def test_cancellation_zero_root(self):
        # Choose MET so z=0 satisfies the unsquared condition at eta=1.
        pt=40.;eta=1.;mass=80.3625;m=MUON_MASS_GEV
        em=math.sqrt(m*m+pt*pt*math.cosh(eta)**2)
        met=(mass*mass-m*m)/(2*em)
        r=reconstruct(pt,eta,0,met,math.pi/2,mass)
        self.assertAlmostEqual(r.pz_nu_minus_gev,0,delta=1e-10)
