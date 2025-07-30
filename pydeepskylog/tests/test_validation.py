import unittest
from pydeepskylog.validation import (
    validate_number, validate_positive, validate_in_range, validate_sequence
)
from pydeepskylog.exceptions import InvalidParameterError

class TestValidation(unittest.TestCase):
    def test_validate_number_valid(self):
        validate_number(1, "test")
        validate_number(1.5, "test")
        validate_number(None, "test", allow_none=True)

    def test_validate_number_invalid(self):
        with self.assertRaises(InvalidParameterError):
            validate_number("a", "test")
        with self.assertRaises(InvalidParameterError):
            validate_number(None, "test", allow_none=False)

    def test_validate_positive_valid(self):
        validate_positive(1, "test")
        validate_positive(1.5, "test")
        validate_positive(0.1, "test")
        validate_positive(None, "test", allow_none=True)

    def test_validate_positive_invalid(self):
        with self.assertRaises(InvalidParameterError):
            validate_positive(-1, "test")
        with self.assertRaises(InvalidParameterError):
            validate_positive(0, "test")
        with self.assertRaises(InvalidParameterError):
            validate_positive("a", "test")
        with self.assertRaises(InvalidParameterError):
            validate_positive(None, "test", allow_none=False)

    def test_validate_in_range_valid(self):
        validate_in_range(5, "test", 0, 10)
        validate_in_range(0, "test", 0, 10)
        validate_in_range(10, "test", 0, 10)

    def test_validate_in_range_invalid(self):
        with self.assertRaises(InvalidParameterError):
            validate_in_range(-1, "test", 0, 10)
        with self.assertRaises(InvalidParameterError):
            validate_in_range(11, "test", 0, 10)
        with self.assertRaises(InvalidParameterError):
            validate_in_range("a", "test", 0, 10)

    def test_validate_sequence_valid(self):
        validate_sequence([1.0, 2.0, 3.0], "test")
        validate_sequence((1.0, 2.0), "test")
        validate_sequence([], "test")
        validate_sequence([1, 2], "test", item_type=int)

    def test_validate_sequence_invalid(self):
        with self.assertRaises(InvalidParameterError):
            validate_sequence("not a sequence", "test")
        with self.assertRaises(InvalidParameterError):
            validate_sequence([1, "a"], "test")
        with self.assertRaises(InvalidParameterError):
            validate_sequence([1.0, 2], "test", item_type=int)

if __name__ == "__main__":
    unittest.main()