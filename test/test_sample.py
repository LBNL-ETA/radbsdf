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
        sd_data = radbsdf.BSDF(self.xml_path)
        tin = 30
        pin = 270
        nsamp = 100
        ivec = vec_from_deg(tin, pin)
        samples = sd_data.sample(nsamp, ivec, radbsdf.SFLAGS["Th"])
        sample_results = [line[3:] for line in samples]
        ovecs = [line[:3] for line in samples]
        query_results = [sd_data.query(ovec, ivec) for ovec in ovecs]
        self.assertCountEqual(query_results, sample_results)
        self.assertListEqual(query_results, sample_results)



if __name__ == "__main__":
    unittest.main()

