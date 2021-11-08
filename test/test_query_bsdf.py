import radbsdf
import math
import unittest

def vec_from_deg(theta: float, phi: float) -> list:
    theta = math.radians(theta)
    phi = math.radians(phi)
    x = math.sin(theta) * math.cos(phi)
    y = math.sin(theta) * math.sin(phi)
    z = math.cos(theta)
    return [round(x, 4), round(y, 4), round(z, 4)]

class TestQuery(unittest.TestCase):

    xml_path = './test_fabric.xml'

    def test_query(self):
        sd_data = radbsdf.TabularBSDF(self.xml_path)
        tin = 30
        pin = 270
        tout = 180 - tin
        pout = 360 - pin
        ivec = vec_from_deg(tin, pin)
        ovec = vec_from_deg(tout, pout)
        res = sd_data.query(ovec, ivec)
        self.assertAlmostEqual(res[1], 3.622446, places=5)


if __name__ == "__main__":
    unittest.main()
