import unittest

import pydeepskylog as pds


class TestBortleConversions(unittest.TestCase):

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
            nelm = pds.bortle_to_nelm(invalid_bortle)
            self.assertEqual(nelm, 0.0, 
                            f"Expected 0.0 for invalid Bortle {invalid_bortle}, got {nelm}")

    def test_bortle_to_sqm(self):
        """Test the bortle_to_sqm function with valid Bortle values."""
        for bortle in range(1, 10):
            sqm = pds.bortle_to_sqm(bortle)
            self.assertGreater(sqm, 0.0, 
                              f"Expected positive SQM value for Bortle {bortle}, got {sqm}")

    def test_bortle_to_sqm_invalid(self):
        """Test the bortle_to_sqm function with invalid Bortle values."""
        for invalid_bortle in [0, 10]:
            sqm = pds.bortle_to_sqm(invalid_bortle)
            self.assertEqual(sqm, 0.0, 
                            f"Expected 0.0 for invalid Bortle {invalid_bortle}, got {sqm}")

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