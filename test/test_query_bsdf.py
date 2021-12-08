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

    tt_xml_path = './test_fabric.xml'
    kf_xml_path = './test_blinds_kf.xml'

    def test_query(self):
        sd_data = radbsdf.TabularBSDF(self.tt_xml_path)
        tin = 0
        pin = 0
        tout = 180 - tin
        pout = 360 - pin
        ivec = vec_from_deg(tin, pin)
        ovec = vec_from_deg(tout, pout)
        res = sd_data.query(ovec, ivec)
        self.assertAlmostEqual(res[1], 7.07400, places=3)
        tin = 30
        pin = 270
        tout = 180 - tin
        pout = 360 - pin
        ivec = vec_from_deg(tin, pin)
        ovec = vec_from_deg(tout, pout)
        res = sd_data.query(ovec, ivec)
        self.assertAlmostEqual(res[1], 3.622, places=3)

    def test_query_kf(self):
        sd_data = radbsdf.TabularBSDF(self.kf_xml_path)
        tin = 0
        pin = 0
        tout = 180 - tin
        pout = 360 - pin
        ivec = vec_from_deg(tin, pin)
        ovec = vec_from_deg(tout, pout)
        res = sd_data.query(ovec, ivec)
        self.assertAlmostEqual(res[1], 3.465e+01, places=3)
        tin = 30
        pin = 270
        tout = 180 - tin
        pout = 360 - pin
        ivec = vec_from_deg(tin, pin)
        ovec = vec_from_deg(tout, pout)
        res = sd_data.query(ovec, ivec)
        self.assertAlmostEqual(res[1], 1.427e+01, places=5)

if __name__ == "__main__":
    unittest.main()
