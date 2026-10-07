import math
import unittest
from neutrino_reconstruction import reconstruct_w_to_munu as reconstruct, W_MASS_GEV, MUON_MASS_GEV

class ReconstructionTests(unittest.TestCase):
    def test_mass_convention(self):
        self.assertEqual(W_MASS_GEV,80.3625)
        self.assertEqual(MUON_MASS_GEV,0.1056583755)
        self.assertEqual(reconstruct(40,1,0,30,2),reconstruct(40,1,0,30,2,parent_mass_gev=80.3625))
        self.assertNotEqual(reconstruct(40,1,0,30,2),reconstruct(40,1,0,30,2,parent_mass_gev=80.4))

    def test_nonfinite_inputs(self):
        base=[40,1,0,30,2,80.3625,0.1056583755]
        for i in range(7):
            for value in [math.nan,math.inf,-math.inf]:
                args=base.copy();args[i]=value
                with self.subTest(i=i,value=value),self.assertRaises(ValueError):
                    reconstruct(*args)

    def test_domain(self):
        for args in [(-1,0,0,30,0),(40,0,0,-1,0),(40,0,0,30,0,0),(40,0,0,30,0,80,0),(40,0,0,30,0,.1,.2)]:
            with self.subTest(args=args),self.assertRaises(ValueError):
                reconstruct(*args)

    def test_overflow(self):
        for args in [(40,1000,0,30,0),(1e200,0,0,1e200,0),(40,0,1e308,30,-1e308)]:
            with self.subTest(args=args),self.assertRaises(ValueError):
                reconstruct(*args)

    def test_zero_met(self):
        r=reconstruct(40,1,0,0,0)
        self.assertEqual(r.branch_state,"TWO_REAL")
        self.assertLess(r.pz_nu_minus_gev,0)
        self.assertGreater(r.pz_nu_plus_gev,0)

    def test_zero_muon_pt(self):
        r=reconstruct(0,0,0,20,1)
        self.assertEqual(r.branch_state,"TWO_REAL")
        self.assertAlmostEqual(r.pz_nu_plus_gev,-r.pz_nu_minus_gev)

    def test_deterministic(self):
        self.assertEqual(reconstruct(40,1,0,30,2),reconstruct(40,1,0,30,2))

    def test_rotation(self):
        a=reconstruct(40,.7,.4,30,2)
        b=reconstruct(40,.7,1.4,30,3)
        self.assertAlmostEqual(a.pz_nu_plus_gev,b.pz_nu_plus_gev,places=10)
        self.assertAlmostEqual(a.discriminant_gev4,b.discriminant_gev4,places=6)

    def test_longitudinal_reflection(self):
        a=reconstruct(40,.7,0,30,2)
        b=reconstruct(40,-.7,0,30,2)
        self.assertAlmostEqual(a.pz_nu_plus_gev,-b.pz_nu_minus_gev,places=10)
        self.assertAlmostEqual(a.pz_nu_minus_gev,-b.pz_nu_plus_gev,places=10)

    def test_negative_zero_eta_regression(self):
        positive=reconstruct(33.6647,0.0,-1.2860,10.1983,-.7089)
        negative=reconstruct(33.6647,-0.0,-1.2860,10.1983,-.7089)
        self.assertEqual(positive,negative)
        self.assertGreater(negative.pz_nu_plus_gev,negative.pz_nu_minus_gev)

    def test_signed_zero_fresh_grid(self):
        # Separate synthetic cases beyond the observed source event.
        for pt in (0,29,71,300):
            for met in (0,3,27):
                for angle in (0,.4,1.8,math.pi):
                    a=reconstruct(pt,0.0,.2,met,angle)
                    b=reconstruct(pt,-0.0,.2,met,angle)
                    self.assertEqual(a,b)
                    if b.branch_state == "TWO_REAL":
                        self.assertGreater(b.pz_nu_plus_gev,b.pz_nu_minus_gev)
