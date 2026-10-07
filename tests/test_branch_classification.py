import math
import unittest
from neutrino_reconstruction import reconstruct_w_to_munu as reconstruct, W_MASS_GEV as M, MUON_MASS_GEV as m

class BranchTests(unittest.TestCase):
    def boundary_met(self):
        return (M*M-m*m)/(2*(math.hypot(m,40)+40))

    def test_below(self):
        r=reconstruct(40,.5,0,self.boundary_met()*.99,math.pi)
        self.assertEqual(r.branch_state,"TWO_REAL")
        self.assertLess(r.transverse_mass_gev,M)

    def test_tangent(self):
        r=reconstruct(40,.5,0,self.boundary_met(),math.pi)
        self.assertEqual(r.branch_state,"TANGENT")
        self.assertEqual(r.pz_nu_plus_gev,r.pz_nu_minus_gev)
        self.assertAlmostEqual(r.transverse_mass_gev,M)

    def test_above(self):
        r=reconstruct(40,.5,0,self.boundary_met()*1.01,math.pi)
        self.assertEqual(r.branch_state,"NO_REAL")
        self.assertIsNone(r.pz_nu_plus_gev)
        self.assertIsNone(r.pz_nu_minus_gev)

    def test_near_boundary_resolved_sides(self):
        for shift,state in [(-1e-10,"TWO_REAL"),(1e-10,"NO_REAL")]:
            r=reconstruct(40,.5,0,self.boundary_met()*(1+shift),math.pi)
            self.assertEqual(r.branch_state,state)

    def test_boundary_band_is_numerical(self):
        for met in [math.nextafter(self.boundary_met(),0),self.boundary_met(),math.nextafter(self.boundary_met(),math.inf)]:
            r=reconstruct(40,.5,0,met,math.pi)
            self.assertEqual(r.branch_state,"TANGENT")
            self.assertLessEqual(abs(r.discriminant_gev4),r.tolerance_gev4)

    def test_mass_change_crosses_boundary(self):
        met=((80.38)**2-m*m)/(2*(math.hypot(m,40)+40))
        self.assertEqual(reconstruct(40,0,0,met,math.pi,80.3625).branch_state,"NO_REAL")
        self.assertEqual(reconstruct(40,0,0,met,math.pi,80.4).branch_state,"TWO_REAL")
