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


class TestDirectHemi(unittest.TestCase):

    xml_path = './test_fabric.xml'

    def test_hemispherical_scattering(self):
        sd_data = radbsdf.TabularBSDF(self.xml_path)
        tin = 0
        pin = 0
        ivec = vec_from_deg(tin, pin)
        proj = sd_data.proj_solid_angle(ivec)
        self.assertAlmostEqual(proj[0], 3.0680e-3, places=7)
        self.assertAlmostEqual(proj[1], 1.9635e-1, places=5)


if __name__ == "__main__":
    unittest.main()

