import unittest

import pydeepskylog as pds


class TestMagnitude(unittest.TestCase):

    def test_convert_nelm_to_sqm(self):

        self.assertEqual(pds.nelm_to_sqm(6.7), 22.0)

        self.assertAlmostEqual(pds.nelm_to_sqm(3.0), 16.88, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(4.0), 18.03, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(4.5), 18.65, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(5.0), 19.30, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(5.5), 20.01, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(5.8), 20.47, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(6.0), 20.80, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(6.2), 21.15, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(6.4), 21.53, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(6.5), 21.73, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(6.6), 21.94, delta=0.01)

        self.assertAlmostEqual(pds.nelm_to_sqm(7.6, -1.0), 21.94, delta=0.01)

    def test_convert_sqm_to_nelm(self):

        self.assertAlmostEqual(pds.sqm_to_nelm(22.0), 6.62, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(21.94), 6.6, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(21.73), 6.5, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(21.53), 6.4, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(21.15), 6.2, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(20.80), 6.0, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(20.47), 5.8, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(20.01), 5.5, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(19.30), 5.0, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(18.65), 4.5, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(18.03), 4.0, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(16.88), 3.0, delta=0.01)

    def test_convert_nelm_to_sqm_and_back(self):
        self.assertAlmostEqual(pds.nelm_to_sqm(5.5), 20.01, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(20.01), 5.5, delta=0.01)


if __name__ == '__main__':
    unittest.main()
