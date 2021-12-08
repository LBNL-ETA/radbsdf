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

    tt_xml_path = './test_fabric.xml'
    kf_xml_path = './test_blinds_kf.xml'

    def test_hemispherical_scattering_tt(self):
        sd_data = radbsdf.TabularBSDF(self.tt_xml_path)
        tin = 0
        pin = 0
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Sh"])
        self.assertAlmostEqual(direct_hemi, 1.0672e-01, places=5)
        tin = 10
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Sh"])
        self.assertAlmostEqual(direct_hemi, 1.0690e-01, places=5)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Sh"])
        self.assertAlmostEqual(direct_hemi, 1.0177e-01, places=5)
        tin = 60
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Sh"])
        self.assertAlmostEqual(direct_hemi, 1.0159e-01, places=5)

    def test_hemispherical_transmittance_tt(self):
        sd_data = radbsdf.TabularBSDF(self.tt_xml_path)
        tin = 0
        pin = 0
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Th"])
        self.assertAlmostEqual(direct_hemi, 2.6489e-02, places=5)
        tin = 10
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Th"])
        self.assertAlmostEqual(direct_hemi, 2.6200e-02, places=5)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Th"])
        self.assertAlmostEqual(direct_hemi, 1.8129e-02, places=5)
        tin = 60
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Th"])
        self.assertAlmostEqual(direct_hemi, 2.7647e-03, places=5)

    def test_hemispherical_reflectance_tt(self):
        sd_data = radbsdf.TabularBSDF(self.tt_xml_path)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Rh"])
        self.assertAlmostEqual(direct_hemi, 8.3643e-02, places=5)

    def test_specualr_transmittance_tt(self):
        sd_data = radbsdf.TabularBSDF(self.tt_xml_path)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Ts"])
        self.assertAlmostEqual(direct_hemi, 1.8129e-02, places=5)

    def test_diffuse_transmittance_tt(self):
        sd_data = radbsdf.TabularBSDF(self.tt_xml_path)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Td"])
        self.assertAlmostEqual(direct_hemi, 0, places=5)

    def test_specualr_reflectance_tt(self):
        sd_data = radbsdf.TabularBSDF(self.tt_xml_path)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Rs"])
        self.assertAlmostEqual(direct_hemi, 2.5439e-02, places=5)

    def test_diffuse_reflectance_tt(self):
        sd_data = radbsdf.TabularBSDF(self.tt_xml_path)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Rd"])
        self.assertAlmostEqual(direct_hemi, 5.8203e-02, places=5)

    def test_hemispherical_scattering_kf(self):
        sd_data = radbsdf.TabularBSDF(self.kf_xml_path)
        tin = 0
        pin = 0
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Sh"])
        self.assertAlmostEqual(direct_hemi, 8.8811e-01, places=5)
        tin = 10
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Sh"])
        self.assertAlmostEqual(direct_hemi, 8.1932e-01, places=5)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Sh"])
        self.assertAlmostEqual(direct_hemi, 5.6807e-01, places=5)
        tin = 60
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Sh"])
        self.assertAlmostEqual(direct_hemi, 3.6459e-01, places=5)

    def test_hemispherical_transmittance_kf(self):
        sd_data = radbsdf.TabularBSDF(self.kf_xml_path)
        tin = 0
        pin = 0
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Th"])
        self.assertAlmostEqual(direct_hemi, 8.6138e-01, places=5)
        tin = 10
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Th"])
        self.assertAlmostEqual(direct_hemi, 7.8790e-01, places=5)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Th"])
        self.assertAlmostEqual(direct_hemi, 5.1824e-01, places=5)
        tin = 60
        pin = 90
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Th"])
        self.assertAlmostEqual(direct_hemi, 1.0589e-01, places=5)
        tin = 60
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Th"])
        self.assertAlmostEqual(direct_hemi, 2.9852e-01, places=5)

    def test_hemispherical_reflectance_kf(self):
        sd_data = radbsdf.TabularBSDF(self.kf_xml_path)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Rh"])
        self.assertAlmostEqual(direct_hemi, 4.9825e-02, places=5)

    def test_specualr_transmittance_kf(self):
        sd_data = radbsdf.TabularBSDF(self.kf_xml_path)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Ts"])
        self.assertAlmostEqual(direct_hemi, 5.1824e-01, places=5)

    def test_diffuse_transmittance_kf(self):
        sd_data = radbsdf.TabularBSDF(self.kf_xml_path)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Td"])
        self.assertAlmostEqual(direct_hemi, 0, places=5)

    def test_specualr_reflectance_kf(self):
        sd_data = radbsdf.TabularBSDF(self.kf_xml_path)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Rs"])
        self.assertAlmostEqual(direct_hemi, 4.9825e-02, places=5)

    def test_diffuse_reflectance_kf(self):
        sd_data = radbsdf.TabularBSDF(self.kf_xml_path)
        tin = 30
        pin = 270
        ivec = vec_from_deg(tin, pin)
        direct_hemi = sd_data.get_direct_hemi(ivec, radbsdf.SFLAGS["Rd"])
        self.assertAlmostEqual(direct_hemi, 0, places=5)

if __name__ == "__main__":
    unittest.main()

