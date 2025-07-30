import requests

def dsl_instruments(username: str) -> dict:
    """
    Get all defined instruments of a DeepskyLog user.

    This function retrieves the instruments defined by a specific user in the DeepskyLog system.

    Args:
        username (str): The username of the DeepskyLog user.

    Returns:
        dict: A dictionary containing the instruments' specifications, in JSON format.
    """
    return _dsl_api_call("instrument", username)

def dsl_eyepieces(username: str) -> dict:
    """
    Get all defined eyepieces of a DeepskyLog user.

    This function retrieves the eyepieces defined by a specific user in the DeepskyLog system.

    Args:
        username (str): The username of the DeepskyLog user.

    Returns:
        dict: A dictionary containing the eyepieces' specifications, in JSON format.
    """
    return _dsl_api_call("eyepieces", username)

def dsl_lenses(username: str) -> dict:
    """
    Get all defined lenses of a DeepskyLog user.

    This function retrieves the lenses defined by a specific user in the DeepskyLog system.

    Args:
        username (str): The username of the DeepskyLog user.

    Returns:
        dict: A dictionary containing the lenses' specifications, in JSON format.
    """
    return _dsl_api_call("lenses", username)

def dsl_filters(username: str) -> dict:
    """
    Get all defined filters of a DeepskyLog user.

    This function retrieves the filters defined by a specific user in the DeepskyLog system.

    Args:
        username (str): The username of the DeepskyLog user.

    Returns:
        dict: A dictionary containing the filters' specifications, in JSON format.
    """
    return _dsl_api_call("filters", username)


def calculate_magnifications(instrument: dict, eyepieces: dict) -> list:
    """
    Calculate possible magnifications for a given telescope and eyepieces.

    This function calculates the possible magnifications for a telescope
    based on its specifications and the eyepieces provided. If the telescope
    has a fixed magnification, it returns that value. Otherwise, it calculates
    the magnifications for each active eyepiece.

    Args:
        instrument (dict): A dictionary containing the telescope's specifications.
            Expected keys are:
                - "fixedMagnification": The fixed magnification of the telescope.  Should be None if there is no fixed magnification.
                - "diameter": The diameter of the telescope.
                - "fd": The focal ratio of the telescope.
        eyepieces (dict): A dictionary containing the eyepieces' specifications.
            Each eyepiece is expected to have:
                - "eyepieceactive": A boolean indicating if the eyepiece is active.
                - "focal_length_mm": The focal length of the eyepiece.

    Returns:
        list: A list of possible magnifications for the telescope.
    """
    magnifications = []
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
    Convert an instrument type string to an integer.
    :param instrument_type: The instrument type as a string.
    :return: The instrument type as an integer.
    """
    instrument_types = {
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
    Convert an instrument type string to a string.
    :param instrument_type: The instrument type as an integer.
    :return: The instrument type as a string.
    """
    instrument_types = {
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

def _dsl_api_call(api_call: str, username: str) -> dict:
    """
    Make an API call to the DeepskyLog system.

    This function constructs the API URL based on the provided API call and username,
    sends a GET request to the DeepskyLog system, and returns the response in JSON format.

    Args:
        api_call (str): The specific API endpoint to call (e.g., "instruments", "eyepieces").
        username (str): The username of the DeepskyLog user.

    Returns:
        dict: The response from the API call, parsed as a JSON dictionary.
    """
    api_url = "https://test.deepskylog.org/api/" + api_call + "/" + username
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code in (401, 403):
            raise PermissionError(f"Authentication failed for user '{username}' (status {response.status_code})")
        response.raise_for_status()
        try:
            data = response.json()
        except ValueError:
            raise RuntimeError("Failed to decode JSON response from DeepskyLog API")
        # Validate that the response is a dict or list
        if not isinstance(data, (dict, list)):
            raise RuntimeError("Unexpected JSON structure: expected dict or list")

        # Example transformation: if data is a list, convert to dict with IDs as keys if possible
        if isinstance(data, list):
            # Try to use 'id' or 'ID' as key if present
            if data and isinstance(data[0], dict) and ('id' in data[0] or 'ID' in data[0]):
                key_name = 'id' if 'id' in data[0] else 'ID'
                data = {str(item[key_name]): item for item in data if key_name in item}
            else:
                # Otherwise, return as-is
                pass

        # Further validation: check for required fields based on api_call
        if api_call in ("instrument", "eyepieces", "lenses", "filters"):
            if not data:
                raise RuntimeError(f"No data returned for {api_call}")
            # Optionally, check for expected keys in the first item
            sample = next(iter(data.values()), None) if isinstance(data, dict) else data[0]
            if not isinstance(sample, dict):
                raise RuntimeError(f"Malformed data for {api_call}: expected dict entries")

        return data

    except requests.exceptions.ConnectionError:
        raise ConnectionError("Failed to connect to DeepskyLog API server")
    except requests.exceptions.Timeout:
        raise ConnectionError("Request to DeepskyLog API timed out")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"An error occurred during the API request: {e}")
