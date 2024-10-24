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
    return _dsl_api_call("instruments", username)

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
    response = requests.get(api_url)
    return response.json()
