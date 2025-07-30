import unittest
from pydeepskylog.exceptions import (
    PyDeepSkyLogError,
    APIConnectionError,
    APITimeoutError,
    APIAuthenticationError,
    APIResponseError,
    InvalidParameterError,
)

class TestExceptions(unittest.TestCase):
    def test_pydeepskylogerror_inheritance(self):
        with self.assertRaises(PyDeepSkyLogError):
            raise PyDeepSkyLogError("Base error")

    def test_api_connection_error(self):
        with self.assertRaises(APIConnectionError):
            raise APIConnectionError("Connection failed")

    def test_api_timeout_error(self):
        with self.assertRaises(APITimeoutError):
            raise APITimeoutError("Timeout")

    def test_api_authentication_error(self):
        with self.assertRaises(APIAuthenticationError):
            raise APIAuthenticationError("Auth failed")

    def test_api_response_error(self):
        with self.assertRaises(APIResponseError):
            raise APIResponseError("Bad response")

    def test_invalid_parameter_error(self):
        with self.assertRaises(InvalidParameterError):
            raise InvalidParameterError("Invalid parameter")

    def test_inheritance_chain(self):
        # All custom exceptions should inherit from PyDeepSkyLogError and Exception
        for exc in [
            APIConnectionError,
            APITimeoutError,
            APIAuthenticationError,
            APIResponseError,
            InvalidParameterError,
        ]:
            self.assertTrue(issubclass(exc, PyDeepSkyLogError))
            self.assertTrue(issubclass(exc, Exception))

if __name__ == "__main__":
    unittest.main()