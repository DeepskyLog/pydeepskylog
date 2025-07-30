import unittest
import math
import pydeepskylog as pds
from pydeepskylog.exceptions import InvalidParameterError


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

    def test_nelm_to_sqm_valid(self):
        # Test known values and upper/lower bounds
        self.assertAlmostEqual(pds.nelm_to_sqm(6.7), 22.0, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(0.0), 13.7, delta=0.1)
        self.assertAlmostEqual(pds.nelm_to_sqm(5.0), 19.30, delta=0.01)
        self.assertAlmostEqual(pds.nelm_to_sqm(6.0), 20.80, delta=0.01)
        # Test with fst_offset
        self.assertAlmostEqual(pds.nelm_to_sqm(6.7, -1.0), 20.31, delta=0.01)

    def test_nelm_to_sqm_invalid(self):
        # Out of range
        with self.assertRaises(InvalidParameterError):
            pds.nelm_to_sqm(-1)
        with self.assertRaises(InvalidParameterError):
            pds.nelm_to_sqm(7)
        # Wrong type
        with self.assertRaises(InvalidParameterError):
            pds.nelm_to_sqm("bad")
        with self.assertRaises(InvalidParameterError):
            pds.nelm_to_sqm(5.0, "bad")

    def test_nelm_to_bortle_valid(self):
        self.assertEqual(pds.nelm_to_bortle(6.7), 1)
        self.assertEqual(pds.nelm_to_bortle(6.5), 1)
        self.assertEqual(pds.nelm_to_bortle(6.4), 2)
        self.assertEqual(pds.nelm_to_bortle(6.3), 3)
        self.assertEqual(pds.nelm_to_bortle(5.8), 4)
        self.assertEqual(pds.nelm_to_bortle(4.9), 5)
        self.assertEqual(pds.nelm_to_bortle(4.4), 6)
        self.assertEqual(pds.nelm_to_bortle(3.9), 7)
        self.assertEqual(pds.nelm_to_bortle(3.6), 8)
        self.assertEqual(pds.nelm_to_bortle(3.0), 9)

    def test_nelm_to_bortle_invalid(self):
        with self.assertRaises(InvalidParameterError):
            pds.nelm_to_bortle(-1)
        with self.assertRaises(InvalidParameterError):
            pds.nelm_to_bortle(7)
        with self.assertRaises(InvalidParameterError):
            pds.nelm_to_bortle("bad")

    def test_sqm_to_bortle_valid(self):
        self.assertEqual(pds.sqm_to_bortle(22.0), 1)
        self.assertEqual(pds.sqm_to_bortle(21.7), 2)
        self.assertEqual(pds.sqm_to_bortle(21.5), 3)
        self.assertEqual(pds.sqm_to_bortle(21.3), 4)
        self.assertEqual(pds.sqm_to_bortle(20.4), 5)
        self.assertEqual(pds.sqm_to_bortle(19.1), 6)
        self.assertEqual(pds.sqm_to_bortle(18.5), 7)
        self.assertEqual(pds.sqm_to_bortle(18.0), 8)
        self.assertEqual(pds.sqm_to_bortle(17.5), 9)
        self.assertEqual(pds.sqm_to_bortle(0.0), 9)

    def test_sqm_to_bortle_invalid(self):
        with self.assertRaises(InvalidParameterError):
            pds.sqm_to_bortle(-1)
        with self.assertRaises(InvalidParameterError):
            pds.sqm_to_bortle(23)
        with self.assertRaises(InvalidParameterError):
            pds.sqm_to_bortle("bad")

    def test_sqm_to_nelm_valid(self):
        self.assertAlmostEqual(pds.sqm_to_nelm(22.0), 6.62, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(21.94), 6.6, delta=0.01)
        self.assertAlmostEqual(pds.sqm_to_nelm(16.88), 3.0, delta=0.01)
        # Test with fst_offset
        self.assertAlmostEqual(pds.sqm_to_nelm(21.94, 1.0), 5.6, delta=0.01)

    def test_sqm_to_nelm_invalid(self):
        with self.assertRaises(InvalidParameterError):
            pds.sqm_to_nelm(-1)
        with self.assertRaises(InvalidParameterError):
            pds.sqm_to_nelm(23)
        with self.assertRaises(InvalidParameterError):
            pds.sqm_to_nelm("bad")
        with self.assertRaises(InvalidParameterError):
            pds.sqm_to_nelm(21.0, "bad")

    def test_bortle_to_nelm_valid(self):
        expected = {1: 6.6, 2: 6.5, 3: 6.4, 4: 6.1, 5: 5.4, 6: 4.7, 7: 4.2, 8: 3.8, 9: 3.6}
        for bortle, nelm in expected.items():
            self.assertEqual(pds.bortle_to_nelm(bortle), nelm)
            self.assertEqual(pds.bortle_to_nelm(bortle, 1.0), nelm - 1.0)

    def test_bortle_to_nelm_invalid(self):
        with self.assertRaises(InvalidParameterError):
            pds.bortle_to_nelm(0)
        with self.assertRaises(InvalidParameterError):
            pds.bortle_to_nelm(10)
        with self.assertRaises(InvalidParameterError):
            pds.bortle_to_nelm("bad")
        with self.assertRaises(InvalidParameterError):
            pds.bortle_to_nelm(5, "bad")

    def test_bortle_to_sqm_valid(self):
        expected = {1: 21.85, 2: 21.6, 3: 21.4, 4: 20.85, 5: 19.75, 6: 18.8, 7: 18.25, 8: 17.75, 9: 17.5}
        for bortle, sqm in expected.items():
            self.assertEqual(pds.bortle_to_sqm(bortle), sqm)

    def test_bortle_to_sqm_invalid(self):
        with self.assertRaises(InvalidParameterError):
            pds.bortle_to_sqm(0)
        with self.assertRaises(InvalidParameterError):
            pds.bortle_to_sqm(10)
        with self.assertRaises(InvalidParameterError):
            pds.bortle_to_sqm("bad")

    def test_nelm_to_sqm_and_back(self):
        # Round-trip conversion
        for nelm in [3.0, 4.0, 5.0, 6.0, 6.7]:
            sqm = pds.nelm_to_sqm(nelm)
            nelm2 = pds.sqm_to_nelm(sqm)
            self.assertAlmostEqual(nelm, nelm2, delta=0.08)

    def test_bortle_to_nelm(self):
        """Test the bortle_to_nelm function with valid Bortle values."""
        for bortle in range(1, 10):
            nelm = pds.bortle_to_nelm(bortle)
            self.assertGreater(nelm, 0.0, f"Expected positive NELM value for Bortle {bortle}, got {nelm}")

    def test_bortle_to_nelm_with_offset(self):
        """Test the bortle_to_nelm function with fst_offset parameter."""
        offset = 1.0
        for bortle in range(1, 10):
            nelm = pds.bortle_to_nelm(bortle, offset)
            nelm_without_offset = pds.bortle_to_nelm(bortle)
            self.assertEqual(nelm, nelm_without_offset - offset,
                             f"Offset not correctly applied for Bortle {bortle}")

    def test_bortle_to_nelm_invalid(self):
        """Test the bortle_to_nelm function with invalid Bortle values."""
        for invalid_bortle in [0, 10]:
            with self.assertRaises(InvalidParameterError):
                nelm = pds.bortle_to_nelm(invalid_bortle)

    def test_bortle_to_sqm(self):
        """Test the bortle_to_sqm function with valid Bortle values."""
        for bortle in range(1, 10):
            sqm = pds.bortle_to_sqm(bortle)
            self.assertGreater(sqm, 0.0,
                               f"Expected positive SQM value for Bortle {bortle}, got {sqm}")

    def test_bortle_to_sqm_invalid(self):
        """Test the bortle_to_sqm function with invalid Bortle values."""
        for invalid_bortle in [0, 10]:
            with self.assertRaises(InvalidParameterError):
                sqm = pds.bortle_to_sqm(invalid_bortle)

    def test_bortle_to_nelm_specific_values(self):
        """Test specific values for bortle_to_nelm to ensure correct mapping."""
        expected_values = {
            1: 6.6,
            2: 6.5,
            3: 6.4,
            4: 6.1,
            5: 5.4,
            6: 4.7,
            7: 4.2,
            8: 3.8,
            9: 3.6
        }

        for bortle, expected_nelm in expected_values.items():
            self.assertEqual(pds.bortle_to_nelm(bortle), expected_nelm,
                             f"Bortle {bortle} should map to NELM {expected_nelm}")

    def test_bortle_to_sqm_specific_values(self):
        """Test specific values for bortle_to_sqm to ensure correct mapping."""
        expected_values = {
            1: 21.85,
            2: 21.6,
            3: 21.4,
            4: 20.85,
            5: 19.75,
            6: 18.8,
            7: 18.25,
            8: 17.75,
            9: 17.5
        }

        for bortle, expected_sqm in expected_values.items():
            self.assertEqual(pds.bortle_to_sqm(bortle), expected_sqm,
                             f"Bortle {bortle} should map to SQM {expected_sqm}")


if __name__ == '__main__':
    unittest.main()
