import math
import random
import unittest
from neutrino_reconstruction import reconstruct_w_to_munu as reconstruct

class DiscriminantTests(unittest.TestCase):
    def test_random_identity_and_sign(self):
        rng=random.Random(5205)
        for mass in (80.3625,80.4):
            for _ in range(1000):
                r=reconstruct(rng.uniform(25,1000),rng.uniform(-2.1,2.1),rng.uniform(-math.pi,math.pi),rng.uniform(0,1000),rng.uniform(-math.pi,math.pi),mass)
                scale=max(1,r.a_gev2**2,mass**4,abs(r.discriminant_gev4))
                self.assertLess(abs(r.discriminant_gev4-r.factored_discriminant_gev4)/scale,1e-12)
                if r.branch_state != "TANGENT":
                    self.assertEqual(r.discriminant_gev4>0,r.transverse_mass_gev<mass)

    def test_positive_second_factor(self):
        for pt in (0,25,10000):
            for met in (0,30,10000):
                r=reconstruct(pt,0,0,met,math.pi)
                self.assertGreater(r.a_gev2+r.et_mu_gev*met,0)
