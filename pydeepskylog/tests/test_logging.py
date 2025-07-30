import unittest
import logging
from pydeepskylog import logging_config

class TestLoggingConfig(unittest.TestCase):
    def setUp(self):
        # Remove all handlers before each test
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.root.setLevel(logging.NOTSET)

    def test_configure_logging_default(self):
        # Should not raise
        logging_config.configure_logging()

    def test_configure_logging_custom_level(self):
        # Should not raise for valid custom level
        logging_config.configure_logging(logging.DEBUG)
        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.DEBUG)

    def test_configure_logging_multiple_calls(self):
        # Should not raise if called multiple times
        logging_config.configure_logging(logging.WARNING)
        logging_config.configure_logging(logging.ERROR)
        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.ERROR)

    def test_configure_logging_invalid_level(self):
        # Should raise ValueError for invalid log level
        with self.assertRaises(ValueError):
            logging_config.configure_logging("not_a_level")

if __name__ == "__main__":
    unittest.main()