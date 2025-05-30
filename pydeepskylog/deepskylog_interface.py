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
                - "fixedMagnification": The fixed magnification of the telescope.  Should be 0 if there is no fixed magnification.
                - "diameter": The diameter of the telescope.
                - "fd": The focal length of the telescope.
        eyepieces (dict): A dictionary containing the eyepieces' specifications.
            Each eyepiece is expected to have:
                - "eyepieceactive": A boolean indicating if the eyepiece is active.
                - "focalLength": The focal length of the eyepiece.

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
            magnifications.append(instrument["diameter"] * instrument["fd"] / eyepiece["focalLength"])

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
        username (str): The username of the DeepskyLog uphpser.

    Returns:
        dict: The response from the API call, parsed as a JSON dictionary.
    """
    api_url = "https://test.deepskylog.org/api/" + api_call + "/" + username
    response = requests.get(api_url)
    return response.json()
