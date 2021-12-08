import unittest
import radbsdf
import math


def vec_from_deg(theta: float, phi: float):
    theta = math.radians(theta)
    phi = math.radians(phi)
    x = math.sin(theta) * math.cos(phi)
    y = math.sin(theta) * math.sin(phi)
    z = math.cos(theta)
    return [x, y, z]


class TestProjSolidAngle(unittest.TestCase):

    tt_xml_path = './test_fabric.xml'
    kf_xml_path = './test_blinds_kf.xml'

    def test_proj_solid_angle_tt(self):
        sd_data = radbsdf.TabularBSDF(self.tt_xml_path)
        tin = 0
        pin = 0
        ivec = vec_from_deg(tin, pin)
        proj = sd_data.proj_solid_angle(ivec)
        self.assertAlmostEqual(proj[0], 3.0680e-3, places=7)
        self.assertAlmostEqual(proj[1], 1.9635e-1, places=5)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        proj = sd_data.proj_solid_angle(ivec)
        self.assertAlmostEqual(proj[0], 3.0680e-3, places=7)
        self.assertAlmostEqual(proj[1], 1.9635e-1, places=5)

    def test_proj_solid_angle_tt2(self):
        sd_data = radbsdf.TabularBSDF(self.tt_xml_path)
        tin = 30
        pin = 270
        vin = vec_from_deg(tin, pin)
        tout = 150
        pout = 90
        vout = vec_from_deg(tout, pout)
        proj = sd_data.proj_solid_angle2(vout, vin)
        self.assertAlmostEqual(proj[0], 3.0680e-3, places=5)
        self.assertAlmostEqual(proj[1], 3.0680e-3, places=5)

    def test_proj_solid_angle_kf(self):
        sd_data = radbsdf.TabularBSDF(self.kf_xml_path)
        tin = 0
        pin = 0
        ivec = vec_from_deg(tin, pin)
        proj = sd_data.proj_solid_angle(ivec)
        self.assertAlmostEqual(proj[0], 2.3864e-02, places=5)
        self.assertAlmostEqual(proj[1], 2.3864e-02, places=5)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        proj = sd_data.proj_solid_angle(ivec)
        self.assertAlmostEqual(proj[0], 2.3622e-02, places=5)
        self.assertAlmostEqual(proj[1], 2.3622e-02, places=5)

    def test_proj_solid_angle_kf2(self):
        sd_data = radbsdf.TabularBSDF(self.kf_xml_path)
        tin = 30
        pin = 270
        vin = vec_from_deg(tin, pin)
        tout = 150
        pout = 90
        vout = vec_from_deg(tout, pout)
        proj = sd_data.proj_solid_angle2(vout, vin)
        self.assertAlmostEqual(proj[0], 2.3622e-2, places=5)
        self.assertAlmostEqual(proj[1], 2.3622e-2, places=5)

if __name__ == "__main__":
    unittest.main()

