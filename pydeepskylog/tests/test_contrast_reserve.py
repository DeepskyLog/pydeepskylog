import unittest

import pydeepskylog as pds


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
        
        # Test input validation
        # Test non-numeric magnitude
        with self.assertRaises(ValueError) as context:
            pds.surface_brightness("invalid", 100, 100)
        self.assertEqual(str(context.exception), "Magnitude must be a number")
        
        # Test non-numeric object_diameter1
        with self.assertRaises(ValueError) as context:
            pds.surface_brightness(10, "invalid", 100)
        self.assertEqual(str(context.exception), "Object diameter 1 must be a number")
        
        # Test non-numeric object_diameter2
        with self.assertRaises(ValueError) as context:
            pds.surface_brightness(10, 100, "invalid")
        self.assertEqual(str(context.exception), "Object diameter 2 must be a number")
        
        # Test non-positive object_diameter1
        with self.assertRaises(ValueError) as context:
            pds.surface_brightness(10, 0, 100)
        self.assertEqual(str(context.exception), "Object diameter 1 must be positive")
        
        with self.assertRaises(ValueError) as context:
            pds.surface_brightness(10, -10, 100)
        self.assertEqual(str(context.exception), "Object diameter 1 must be positive")
        
        # Test non-positive object_diameter2
        with self.assertRaises(ValueError) as context:
            pds.surface_brightness(10, 100, 0)
        self.assertEqual(str(context.exception), "Object diameter 2 must be positive")
        
        with self.assertRaises(ValueError) as context:
            pds.surface_brightness(10, 100, -10)
        self.assertEqual(str(context.exception), "Object diameter 2 must be positive")

    def test_contrast_reserve(self):
        # Berk 59
        # SQM of the location: 22
        diameter = 457
        sqm = 22

        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 118, None, 11, 600, 600), 0.13, delta=0.01)

        # SQM of the location: 20.15
        sqm = 20.15
        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 473, None, 11, 600, 600), -0.35, delta=0.01)

        # M 65
        # SQM of the location: 22
        sqm = 22

        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 66, None, 9.2, 540, 138), 1.18, delta=0.01)

        # SQM of the location: 20.15
        sqm = 20.15

        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 66, None, 9.2, 540, 138), 0.70, delta=0.01)

        # M 82
        sqm = 22

        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 66, None, 8.6, 630, 306), 1.20, delta=0.01)

        # SQM of the location: 20.34
        sqm = 20.15

        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 66, None, 8.6, 630, 306), 0.70, delta=0.01)
        
        # Test cases with None parameters
        # These test cases should return None when certain parameters are None
        self.assertIsNone(pds.contrast_reserve(sqm, diameter, 118, None, None, 600, 600))
        self.assertIsNone(pds.contrast_reserve(sqm, diameter, 118, None, 11, None, 600))
        self.assertIsNone(pds.contrast_reserve(sqm, diameter, 118, None, 11, 600, None))
        
        # Test with surface brightness provided directly
        # When providing surface brightness directly, the calculation is different
        # The expected value is calculated based on the formula: -0.4 * (surf_brightness + 8.89 - sqm)
        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 118, 21.1119, None, 600, 600), -2.54, delta=0.01)
        
        # Test with object_diameter1 < object_diameter2 (swap logic)
        self.assertAlmostEqual(pds.contrast_reserve(sqm, diameter, 66, None, 9.2, 138, 540), 0.70, delta=0.01)
        
        # Test edge cases for boundary conditions
        # Very low SQM to trigger sb_ia < 0 condition (line 198)
        very_low_sqm = 1
        result = pds.contrast_reserve(very_low_sqm, diameter, 66, None, 9.2, 540, 138)
        self.assertIsNotNone(result)
        
        # Very small angle to trigger i < 0 condition (lines 216-217)
        very_small_magnification = 0.0001
        result = pds.contrast_reserve(sqm, diameter, very_small_magnification, None, 9.2, 540, 138)
        self.assertIsNotNone(result)
        
        # Test extreme values to trigger max_log conditions (lines 239, 242)
        # These are difficult to trigger directly, but we can at least ensure the function runs
        extreme_sqm = 30  # Very dark sky
        result = pds.contrast_reserve(extreme_sqm, diameter, 66, None, 9.2, 540, 138)
        self.assertIsNotNone(result)
        
        extreme_sqm = 0  # Very bright sky
        result = pds.contrast_reserve(extreme_sqm, diameter, 66, None, 9.2, 540, 138)
        self.assertIsNotNone(result)
        
        # Test input validation
        # Test non-numeric sqm
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve("invalid", diameter, 66, None, 9.2, 540, 138)
        self.assertEqual(str(context.exception), "SQM must be a number")
        
        # Test non-numeric telescope_diameter
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, "invalid", 66, None, 9.2, 540, 138)
        self.assertEqual(str(context.exception), "Telescope diameter must be a number")
        
        # Test non-numeric magnification
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, "invalid", None, 9.2, 540, 138)
        self.assertEqual(str(context.exception), "Magnification must be a number")
        
        # Test non-positive telescope_diameter
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, 0, 66, None, 9.2, 540, 138)
        self.assertEqual(str(context.exception), "Telescope diameter must be positive")
        
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, -100, 66, None, 9.2, 540, 138)
        self.assertEqual(str(context.exception), "Telescope diameter must be positive")
        
        # Test non-positive magnification
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, 0, None, 9.2, 540, 138)
        self.assertEqual(str(context.exception), "Magnification must be positive")
        
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, -10, None, 9.2, 540, 138)
        self.assertEqual(str(context.exception), "Magnification must be positive")
        
        # Test non-numeric surf_brightness
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, 66, "invalid", 9.2, 540, 138)
        self.assertEqual(str(context.exception), "Surface brightness must be a number or None")
        
        # Test non-numeric magnitude when surf_brightness is None
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, 66, None, "invalid", 540, 138)
        self.assertEqual(str(context.exception), "Magnitude must be a number or None")
        
        # Test non-numeric object_diameter1
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, 66, None, 9.2, "invalid", 138)
        self.assertEqual(str(context.exception), "Object diameter 1 must be a number or None")
        
        # Test non-numeric object_diameter2
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, 66, None, 9.2, 540, "invalid")
        self.assertEqual(str(context.exception), "Object diameter 2 must be a number or None")
        
        # Test non-positive object_diameter1
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, 66, None, 9.2, 0, 138)
        self.assertEqual(str(context.exception), "Object diameter 1 must be positive")
        
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, 66, None, 9.2, -10, 138)
        self.assertEqual(str(context.exception), "Object diameter 1 must be positive")
        
        # Test non-positive object_diameter2
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, 66, None, 9.2, 540, 0)
        self.assertEqual(str(context.exception), "Object diameter 2 must be positive")
        
        with self.assertRaises(ValueError) as context:
            pds.contrast_reserve(sqm, diameter, 66, None, 9.2, 540, -10)
        self.assertEqual(str(context.exception), "Object diameter 2 must be positive")

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
            sqm, diameter, None, 11, 600, 600, available_magnifications), 133)

        # SQM of the location: 20.15
        sqm = 20.15
        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, None, 11, 600, 600, available_magnifications), 473)

        # M 65
        # SQM of the location: 22
        sqm = 22

        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, None, 9.2, 540, 138, available_magnifications), 66)

        # SQM of the location: 20.15
        sqm = 20.15

        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, None, 9.2, 540, 138, available_magnifications), 66)

        # M 82
        sqm = 22

        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, None, 8.6, 630, 306, available_magnifications), 66)

        # SQM of the location: 20.34
        sqm = 20.15

        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, None, 8.6, 630, 306, available_magnifications), 66)
            
        # Test with specific parameters from original test code
        sqm = 20.15
        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, 15.5, 11, 600, 600, available_magnifications), 473)
            
        # Test with empty magnifications list
        empty_magnifications = []
        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, None, 11, 600, 600, empty_magnifications), 0)
            
        # Test with a single magnification
        single_magnification = [100]
        self.assertEqual(pds.optimal_detection_magnification(
            sqm, diameter, None, 11, 600, 600, single_magnification), 100)
            
        # Test input validation
        # Test non-numeric sqm
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification("invalid", diameter, None, 11, 600, 600, available_magnifications)
        self.assertEqual(str(context.exception), "SQM must be a number")
        
        # Test non-numeric telescope_diameter
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, "invalid", None, 11, 600, 600, available_magnifications)
        self.assertEqual(str(context.exception), "Telescope diameter must be a number")
        
        # Test non-positive telescope_diameter
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, 0, None, 11, 600, 600, available_magnifications)
        self.assertEqual(str(context.exception), "Telescope diameter must be positive")
        
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, -100, None, 11, 600, 600, available_magnifications)
        self.assertEqual(str(context.exception), "Telescope diameter must be positive")
        
        # Test non-numeric surf_brightness
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, "invalid", 11, 600, 600, available_magnifications)
        self.assertEqual(str(context.exception), "Surface brightness must be a number or None")
        
        # Test non-numeric magnitude when surf_brightness is None
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, "invalid", 600, 600, available_magnifications)
        self.assertEqual(str(context.exception), "Magnitude must be a number or None")
        
        # Test non-numeric object_diameter1
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, 11, "invalid", 600, available_magnifications)
        self.assertEqual(str(context.exception), "Object diameter 1 must be a number or None")
        
        # Test non-numeric object_diameter2
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, 11, 600, "invalid", available_magnifications)
        self.assertEqual(str(context.exception), "Object diameter 2 must be a number or None")
        
        # Test non-positive object_diameter1
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, 11, 0, 600, available_magnifications)
        self.assertEqual(str(context.exception), "Object diameter 1 must be positive")
        
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, 11, -10, 600, available_magnifications)
        self.assertEqual(str(context.exception), "Object diameter 1 must be positive")
        
        # Test non-positive object_diameter2
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, 11, 600, 0, available_magnifications)
        self.assertEqual(str(context.exception), "Object diameter 2 must be positive")
        
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, 11, 600, -10, available_magnifications)
        self.assertEqual(str(context.exception), "Object diameter 2 must be positive")
        
        # Test non-list magnifications
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, 11, 600, 600, "invalid")
        self.assertEqual(str(context.exception), "Magnifications must be a list")
        
        # Test non-numeric magnification in list
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, 11, 600, 600, [66, "invalid", 158])
        self.assertEqual(str(context.exception), "Each magnification must be a number")
        
        # Test non-positive magnification in list
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, 11, 600, 600, [66, 0, 158])
        self.assertEqual(str(context.exception), "Each magnification must be positive")
        
        with self.assertRaises(ValueError) as context:
            pds.optimal_detection_magnification(sqm, diameter, None, 11, 600, 600, [66, -10, 158])
        self.assertEqual(str(context.exception), "Each magnification must be positive")


if __name__ == '__main__':
    unittest.main()
