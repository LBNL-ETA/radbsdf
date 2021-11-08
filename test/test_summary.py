import unittest
import radbsdf
import subprocess as sp
import math




def vec_from_deg(theta: float, phi: float):
    theta = math.radians(theta)
    phi = math.radians(phi)
    x = math.sin(theta) * math.cos(phi)
    y = math.sin(theta) * math.sin(phi)
    z = math.cos(theta)
    return [x, y, z]


class TestDirectHemi(unittest.TestCase):
    xml_path = './test_fabric.xml'
    def test_hemispherical_scattering(self):
        sd_data = radbsdf.TabularBSDF(self.xml_path)
        sd_data.get_summary()
        # in = 30
        # pin = 270
        # ivec = vec_from_deg(tin, pin)
        # direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Sh"])
        # self.assertAlmostEqual(direct_hemi, 1.0177e-01, places=5)


if __name__ == "__main__":
    unittest.main()

