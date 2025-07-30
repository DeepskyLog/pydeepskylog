import unittest
from unittest.mock import patch, Mock
import pydeepskylog.deepskylog_interface as dsl

class TestDeepskylogInterface(unittest.TestCase):
    def setUp(self):
        # Clear cache before each test
        dsl._DSL_API_CACHE.clear()

    @patch('pydeepskylog.deepskylog_interface.requests.get')
    def test_dsl_instruments_success(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(return_value={'1': {'id': 1, 'name': 'Scope'}})
        )
        result = dsl.dsl_instruments('user')
        self.assertIn('1', result)
        self.assertEqual(result['1']['name'], 'Scope')

    @patch('pydeepskylog.deepskylog_interface.requests.get')
    def test_dsl_eyepieces_success(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(return_value={'2': {'id': 2, 'name': 'Plossl'}})
        )
        result = dsl.dsl_eyepieces('user')
        self.assertIn('2', result)
        self.assertEqual(result['2']['name'], 'Plossl')

    @patch('pydeepskylog.deepskylog_interface.requests.get')
    def test_api_authentication_error(self, mock_get):
        mock_get.return_value = Mock(status_code=401, raise_for_status=Mock())
        with self.assertRaises(PermissionError):
            dsl.dsl_instruments('user')

    @patch('pydeepskylog.deepskylog_interface.requests.get')
    def test_api_connection_error(self, mock_get):
        mock_get.side_effect = dsl.requests.exceptions.ConnectionError
        with self.assertRaises(ConnectionError):
            dsl.dsl_instruments('user')

    @patch('pydeepskylog.deepskylog_interface.requests.get')
    def test_api_timeout(self, mock_get):
        mock_get.side_effect = dsl.requests.exceptions.Timeout
        with self.assertRaises(ConnectionError):
            dsl.dsl_instruments('user')

    @patch('pydeepskylog.deepskylog_interface.requests.get')
    def test_api_malformed_json(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=Mock(side_effect=ValueError))
        with self.assertRaises(RuntimeError):
            dsl.dsl_instruments('user')

    def test_calculate_magnifications(self):
        instrument = {"fixedMagnification": None, "diameter": 100, "fd": 8}
        eyepieces = [
            {"eyepieceactive": True, "focal_length_mm": 20},
            {"eyepieceactive": False, "focal_length_mm": 10},
            {"eyepieceactive": True, "focal_length_mm": 10},
        ]
        mags = dsl.calculate_magnifications(instrument, eyepieces)
        self.assertEqual(mags, [40.0, 80.0])

    def test_calculate_magnifications_fixed(self):
        instrument = {"fixedMagnification": 50, "diameter": 100, "fd": 8}
        eyepieces = [
            {"eyepieceactive": True, "focal_length_mm": 20},
        ]
        mags = dsl.calculate_magnifications(instrument, eyepieces)
        self.assertEqual(mags, [50])

if __name__ == '__main__':
    unittest.main()