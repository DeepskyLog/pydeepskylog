import logging
import requests
import time
from typing import Dict, List, Any, Optional
from pydeepskylog.exceptions import (
    APIConnectionError, APITimeoutError, APIAuthenticationError, APIResponseError, InvalidParameterError
)
import threading
from functools import wraps
from pydeepskylog.sanitization import sanitize_string

DSL_API_BASE_URL: str = "https://test.deepskylog.org/api/"  # Change this as needed

# Simple in-memory cache: {url: (timestamp, data)}
_DSL_API_CACHE: Dict[str, tuple[float, Any]] = {}
_DSL_API_CACHE_TTL: int = 300  # seconds (5 minutes)

# Rate limiting parameters
_DSL_API_RATE_LIMIT = 1  # max requests
_DSL_API_RATE_PERIOD = 1.0  # seconds

_rate_lock = threading.Lock()
_rate_timestamps = []

def rate_limited(max_calls: int, period: float):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with _rate_lock:
                now = time.time()
                # Remove timestamps outside the window
                while _rate_timestamps and _rate_timestamps[0] <= now - period:
                    _rate_timestamps.pop(0)
                if len(_rate_timestamps) >= max_calls:
                    sleep_time = period - (now - _rate_timestamps[0])
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                _rate_timestamps.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

def dsl_instruments(username: str) -> Dict[str, Any]:
    """
    Retrieve all defined astronomical instruments for a DeepskyLog user via the DeepskyLog API.

    This function queries the DeepskyLog API for the specified user and returns a dictionary
    containing all telescopes and observing instruments registered in their account. The data
    typically includes specifications such as instrument type, diameter, focal length, and other
    relevant properties.

    Args:
        username (str): The DeepskyLog username whose instruments are to be retrieved.

    Returns:
        Dict[str, Any]: A dictionary mapping instrument IDs to their specification dictionaries,
        as returned by the DeepskyLog API.

    Raises:
        APIConnectionError: If the API server cannot be reached.
        APITimeoutError: If the API request times out.
        APIAuthenticationError: If authentication fails for the user.
        APIResponseError: If the API response is invalid or malformed.
        InvalidParameterError: If the username is invalid.

    Example:
        >>> instruments = dsl_instruments("astro_user")
        >>> for inst_id, inst in instruments.items():
        ...     print(inst["name"], inst["diameter"])
    """
    username = sanitize_string(username, max_length=64)
    return _dsl_api_call("instrument", username)

def dsl_eyepieces(username: str) -> Dict[str, Any]:
    """
    Retrieve all defined eyepieces for a DeepskyLog user via the DeepskyLog API.

    This function queries the DeepskyLog API for the specified user and returns a dictionary
    containing all eyepieces registered in their account. The data typically includes specifications
    such as focal length, apparent field of view, and whether the eyepiece is active.

    Args:
        username (str): The DeepskyLog username whose eyepieces are to be retrieved.

    Returns:
        Dict[str, Any]: A dictionary mapping eyepiece IDs to their specification dictionaries,
        as returned by the DeepskyLog API.

    Raises:
        APIConnectionError: If the API server cannot be reached.
        APITimeoutError: If the API request times out.
        APIAuthenticationError: If authentication fails for the user.
        APIResponseError: If the API response is invalid or malformed.
        InvalidParameterError: If the username is invalid.

    Example:
        >>> eyepieces = dsl_eyepieces("astro_user")
        >>> for ep_id, ep in eyepieces.items():
        ...     print(ep["name"], ep["focal_length_mm"])
    """
    username = sanitize_string(username, max_length=64)
    return _dsl_api_call("eyepieces", username)

def dsl_lenses(username: str) -> Dict[str, Any]:
    """
    Retrieve all defined lenses for a DeepskyLog user via the DeepskyLog API.

    This function queries the DeepskyLog API for the specified user and returns a dictionary
    containing all lenses registered in their account. The data typically includes specifications
    such as lens type, focal length, and other relevant properties.

    Args:
        username (str): The DeepskyLog username whose lenses are to be retrieved.

    Returns:
        Dict[str, Any]: A dictionary mapping lens IDs to their specification dictionaries,
        as returned by the DeepskyLog API.

    Raises:
        APIConnectionError: If the API server cannot be reached.
        APITimeoutError: If the API request times out.
        APIAuthenticationError: If authentication fails for the user.
        APIResponseError: If the API response is invalid or malformed.
        InvalidParameterError: If the username is invalid.

    Example:
        >>> lenses = dsl_lenses("astro_user")
        >>> for lens_id, lens in lenses.items():
        ...     print(lens["name"], lens["focal_length_mm"])
    """
    username = sanitize_string(username, max_length=64)
    return _dsl_api_call("lenses", username)

def dsl_filters(username: str) -> Dict[str, Any]:
    """
    Retrieve all defined filters for a DeepskyLog user via the DeepskyLog API.

    This function queries the DeepskyLog API for the specified user and returns a dictionary
    containing all filters registered in their account. The data typically includes specifications
    such as filter type, bandpass, and other relevant properties.

    Args:
        username (str): The DeepskyLog username whose filters are to be retrieved.

    Returns:
        Dict[str, Any]: A dictionary mapping filter IDs to their specification dictionaries,
        as returned by the DeepskyLog API.

    Raises:
        APIConnectionError: If the API server cannot be reached.
        APITimeoutError: If the API request times out.
        APIAuthenticationError: If authentication fails for the user.
        APIResponseError: If the API response is invalid or malformed.
        InvalidParameterError: If the username is invalid.

    Example:
        >>> filters = dsl_filters("astro_user")
        >>> for filter_id, flt in filters.items():
        ...     print(flt["name"], flt["type"])
    """
    username = sanitize_string(username, max_length=64)
    return _dsl_api_call("filters", username)


def calculate_magnifications(instrument: Dict[str, Any], eyepieces: List[Dict[str, Any]]) -> List[float]:
    """
    Compute all possible magnifications for a given telescope (instrument) and a list of eyepieces.

    This function determines the set of magnifications achievable with the provided telescope and eyepieces.
    If the instrument specifies a fixed magnification (e.g., for binoculars), that value is returned as a single-item list.
    Otherwise, the function calculates the magnification for each active eyepiece using the formula:

        magnification = (telescope diameter) * (focal ratio) / (eyepiece focal length in mm)

    Only eyepieces marked as active (`eyepieceactive` is True) are considered.

    Args:
        instrument (Dict[str, Any]): Dictionary with telescope specifications. Expected keys:
            - "fixedMagnification" (float or None): Fixed magnification, if applicable.
            - "diameter" (float): Telescope diameter (typically in mm).
            - "fd" (float): Telescope focal ratio (focal length / diameter).
        eyepieces (List[Dict[str, Any]]): List of eyepiece dictionaries. Each should have:
            - "eyepieceactive" (bool): Whether the eyepiece is active.
            - "focal_length_mm" (float): Eyepiece focal length in millimeters.

    Returns:
        List[float]: List of possible magnifications for the telescope and eyepieces.

    Example:
        >>> mags = calculate_magnifications(instrument, eyepieces)
        >>> print(mags)
    """
    magnifications: List[float] = []
    # Check if the instrument has a fixed magnification
    if instrument["fixedMagnification"]:
        magnifications.append(instrument["fixedMagnification"])
        return magnifications

    for eyepiece in eyepieces:
        if eyepiece["eyepieceactive"]:
            magnifications.append(instrument["diameter"] * instrument["fd"] / eyepiece["focal_length_mm"])

    return magnifications

def convert_instrument_type_to_int(instrument_type: str) -> int:
    """
    Convert an instrument type string to its corresponding integer code.

    This function maps a human-readable instrument type (e\.g\., "Refractor", "Binoculars") to an integer value
    as defined by the DeepskyLog system\. The mapping is used for API communication and data storage consistency\.

    Args:
        instrument_type \(str\): The instrument type as a string \(e\.g\., "Refractor", "Binoculars"\)\.

    Returns:
        int: The integer code corresponding to the instrument type\.

    Raises:
        KeyError: If the instrument type string is not recognized\.

    Example:
        >>> convert_instrument_type_to_int\("Refractor"\)
        2
    """
    instrument_types: Dict[str, int] = {
        "Naked Eye": 0,
        "Binoculars": 1,
        "Refractor": 2,
        "Reflector": 3,
        "Finderscope": 4,
        "Other": 5,
        "Cassegrain": 6,
        "Kutter": 7,
        "Maksutov": 8,
        "Schmidt Cassegrain": 9,
    }

    return instrument_types[instrument_type]

def convert_instrument_type_to_string(instrument_type: int) -> str:
    """
    Convert an instrument type integer code to its corresponding string representation.

    This function maps an integer instrument type code (as used by the DeepskyLog system) to a human-readable
    instrument type string (e\.g\., "Refractor", "Binoculars")\. This mapping is used for displaying instrument
    types and for interpreting API data.

    Args:
        instrument_type \(int\): The instrument type code as an integer \(e\.g\., 2 for "Refractor", 1 for "Binoculars"\)\.

    Returns:
        str: The string representation of the instrument type\.

    Raises:
        KeyError: If the instrument type code is not recognized\.

    Example:
        >>> convert_instrument_type_to_string\(2\)
        'Refractor'
    """
    instrument_types: Dict[str, int] = {
        0: "Naked Eye",
        1: "Binoculars",
        2: "Refractor",
        3: "Reflector",
        4: "Finderscope",
        5: "Other",
        6: "Cassegrain",
        7: "Kutter",
        8: "Maksutov",
        9: "Schmidt Cassegrain",
    }

    return instrument_types[instrument_type]

@rate_limited(_DSL_API_RATE_LIMIT, _DSL_API_RATE_PERIOD)
def _dsl_api_call(api_call: str, username: str) -> Dict[str, Any]:
    """
    Make a GET request to the DeepskyLog API for a specific resource and user.

    This function constructs the appropriate API URL for the requested resource (e\.g\., instruments, eyepieces)
    and user, sends a GET request, and returns the parsed JSON response\. It includes in-memory caching to reduce
    redundant API calls and handles various error conditions, raising custom exceptions for connection, timeout,
    authentication, and response issues\.

    Args:
        api_call \(str\): The resource endpoint to query \(e\.g\., "instrument", "eyepieces", "lenses", "filters"\)\.
        username \(str\): The DeepskyLog username for which to retrieve data\.

    Returns:
        Dict\[str, Any\]: The parsed JSON response from the API, typically a dictionary mapping IDs to resource data\.

    Raises:
        APIConnectionError: If the API server cannot be reached\.
        APITimeoutError: If the API request times out\.
        APIAuthenticationError: If authentication fails for the user\.
        APIResponseError: If the API response is invalid, malformed, or missing expected data\.
        InvalidParameterError: If the username or parameters are invalid\.

    Example:
        >>> data = _dsl_api_call\("instrument", "astro_user"\)
        >>> print\(data\)
    """
    username = sanitize_string(username, max_length=64)
    api_url: str = f"{DSL_API_BASE_URL}{api_call}/{username}"
    now: float = time.time()
    logger: logging = logging.getLogger(__name__)

    # Check cache
    cache_entry = _DSL_API_CACHE.get(api_url)
    if cache_entry:
        timestamp, data = cache_entry
        if now - timestamp < _DSL_API_CACHE_TTL:
            return data

    try:
        response = requests.get(api_url, timeout=10, verify=True)
        if response.status_code in (401, 403):
            logger.error(f"Authentication failed for user '{username}' (status {response.status_code})")
            raise APIAuthenticationError(f"Authentication failed for user '{username}' (status {response.status_code})")
        response.raise_for_status()
        try:
            data = response.json()
        except ValueError:
            logger.error("Failed to decode JSON response from DeepskyLog API")
            raise APIResponseError("Failed to decode JSON response from DeepskyLog API")
        # Validate that the response is a dict or list
        if not isinstance(data, (dict, list)):
            logger.error("Unexpected JSON structure: expected dict or list")
            raise APIResponseError("Unexpected JSON structure: expected dict or list")

        # Further validation: check for required fields based on api_call
        if api_call in ("instrument", "eyepieces", "lenses", "filters"):
            if not data:
                logger.error(f"No data returned for {api_call}")
                raise APIResponseError(f"No data returned for {api_call}")
            # Optionally, check for expected keys in the first item
            sample = next(iter(data.values()), None) if isinstance(data, dict) else data[0]
            if not isinstance(sample, dict):
                logger.error(f"Malformed data for {api_call}: expected dict entries")
                raise APIResponseError(f"Malformed data for {api_call}: expected dict entries")
        # Store in cache
        _DSL_API_CACHE[api_url] = (now, data)
        return data

    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to DeepskyLog API server")
        raise APIConnectionError("Failed to connect to DeepskyLog API server")
    except requests.exceptions.Timeout:
        logger.error("Request to DeepskyLog API timed out")
        raise APITimeoutError("Request to DeepskyLog API timed out")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise APIResponseError(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred during the API request: {e}")
        raise APIResponseError(f"An error occurred during the API request: {e}")
