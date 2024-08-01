import unittest

import pydeepskylog.contrast_reserve as pds


class TestContrastReserve(unittest.TestCase):

    def test_surface_brightness(self):
        sb = pds.surface_brightness(15, 8220, 8220)
        self.assertAlmostEqual(sb, 34.3119, delta=0.001)

        sb = pds.surface_brightness(8, 10800, 10800)
        self.assertAlmostEqual(sb, 27.9047, delta=0.001)

        sb = pds.surface_brightness(14.82, 55.98, 27.48)
        self.assertAlmostEqual(sb, 22.5252, delta=0.001)

        sb = pds.surface_brightness(12.4, 72, 54)
        self.assertAlmostEqual(sb, 21.1119, delta=0.001)

        sb = pds.surface_brightness(7.4, 3.5, 3.5)
        self.assertAlmostEqual(sb, 9.8579, delta=0.001)

        sb = pds.surface_brightness(8, 17, 17)
        self.assertAlmostEqual(sb, 13.8898, delta=0.001)

        sb = pds.surface_brightness(18.3, 46.998, 46.998)
        self.assertAlmostEqual(sb, 26.398, delta=0.001)

        sb = pds.surface_brightness(11, 600, 600)
        self.assertAlmostEqual(sb, 24.6283, delta=0.001)

        sb = pds.surface_brightness(9.2, 540, 138)
        self.assertAlmostEqual(sb, 21.1182, delta=0.001)

    def test_contrast_reserve(self):
        # Berk 59
        # SQM of the location: 22
        diameter = 457
        sqm = 22

        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 118, 11, 600, 600), 0.13, delta=0.01)

        # SQM of the location: 20.15
        sqm = 20.15
        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 473, 11, 600, 600), -0.35, delta=0.01)

        # M 65
        # SQM of the location: 22
        sqm = 22

        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 66, 9.2, 540, 138), 1.18, delta=0.01)

        # SQM of the location: 20.15
        sqm = 20.15

        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 66, 9.2, 540, 138), 0.70, delta=0.01)

        # M 82
        sqm = 22

        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 66, 8.6, 630, 306), 1.20, delta=0.01)

        # SQM of the location: 20.34
        sqm = 20.15

        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 66, 8.6, 630, 306), 0.70, delta=0.01)

    def test_best_magnification(self):
        available_magnifications = [
            66, 103, 158, 257, 411,
            76, 118, 182, 296, 473,
            133, 206, 317, 514, 823,
        ]

        # Berk 59
        # SQM of the location: 22
        diameter = 457
        sqm = 22

        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, 11, 600, 600, available_magnifications), 133)

        # SQM of the location: 20.15
        sqm = 20.15
        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, 11, 600, 600, available_magnifications), 473)

        # M 65
        # SQM of the location: 22
        sqm = 22

        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, 9.2, 540, 138, available_magnifications), 66)

        # SQM of the location: 20.15
        sqm = 20.15

        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, 9.2, 540, 138, available_magnifications), 66)

        # M 82
        sqm = 22

        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, 8.6, 630, 306, available_magnifications), 66)

        # SQM of the location: 20.34
        sqm = 20.15

        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, 8.6, 630, 306, available_magnifications), 66)


if __name__ == '__main__':
    unittest.main()
