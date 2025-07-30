# pydeepskylog/exceptions.py
class PyDeepSkyLogError(Exception):
    """Base exception for pydeepskylog errors."""

class APIConnectionError(PyDeepSkyLogError):
    """Raised when API connection fails."""

class APITimeoutError(PyDeepSkyLogError):
    """Raised when API request times out."""

class APIAuthenticationError(PyDeepSkyLogError):
    """Raised when API authentication fails."""

class APIResponseError(PyDeepSkyLogError):
    """Raised for invalid or unexpected API responses."""

class InvalidParameterError(PyDeepSkyLogError):
    """Raised for invalid function parameters."""