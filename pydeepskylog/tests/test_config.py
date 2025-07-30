import unittest
from pydeepskylog.config import ContrastReserveConfig

class TestContrastReserveConfig(unittest.TestCase):
    def test_angle_type_and_length(self):
        self.assertIsInstance(ContrastReserveConfig.ANGLE, list)
        self.assertEqual(len(ContrastReserveConfig.ANGLE), ContrastReserveConfig.ANGLE_SIZE)
        for val in ContrastReserveConfig.ANGLE:
            self.assertIsInstance(val, float)

    def test_ltc_type_and_shape(self):
        self.assertIsInstance(ContrastReserveConfig.LTC, list)
        self.assertEqual(len(ContrastReserveConfig.LTC), ContrastReserveConfig.LTC_SIZE)
        for row in ContrastReserveConfig.LTC:
            self.assertIsInstance(row, list)
            self.assertEqual(len(row), len(ContrastReserveConfig.ANGLE) + 1)
            self.assertIsInstance(row[0], int)
            for val in row[1:]:
                self.assertIsInstance(val, float)

    def test_ltc_edge_values(self):
        # Check first and last row/column values
        self.assertEqual(ContrastReserveConfig.LTC[0][0], 4)
        self.assertEqual(ContrastReserveConfig.LTC[-1][0], 27)
        self.assertIsInstance(ContrastReserveConfig.LTC[0][-1], float)
        self.assertIsInstance(ContrastReserveConfig.LTC[-1][-1], float)

    def test_angle_out_of_bounds(self):
        with self.assertRaises(IndexError):
            _ = ContrastReserveConfig.ANGLE[ContrastReserveConfig.ANGLE_SIZE]
        with self.assertRaises(IndexError):
            _ = ContrastReserveConfig.LTC[ContrastReserveConfig.LTC_SIZE]

    def test_ltc_row_length(self):
        for row in ContrastReserveConfig.LTC:
            self.assertEqual(len(row), len(ContrastReserveConfig.ANGLE) + 1)

if __name__ == "__main__":
    unittest.main()