import logging
import math
from typing import Optional, Tuple, List
from pydeepskylog.config import ContrastReserveConfig
from pydeepskylog.exceptions import InvalidParameterError
from pydeepskylog.validation import (
    validate_number, validate_positive, validate_sequence
)

def surface_brightness(magnitude: float, object_diameter1: float, object_diameter2: float) -> float:
    """
    Calculate the surface brightness of an astronomical object.  This is needed to calculate the contrast of the target.

    Surface brightness (SB) is the brightness of an extended object per unit area, expressed in magnitudes per square arcsecond.
    It is calculated using the formula:

        SB = m + 2.5 * log10(2827 * (D1 / 60) * (D2 / 60))

    where:
        - m is the integrated magnitude of the object,
        - D1 and D2 are the major and minor axis diameters in arcseconds,
        - 2827 is the number of square arcseconds in one square arcminute.

    This formula converts the total magnitude into a per-area brightness, which is important for visual detection thresholds.

    Args:
        magnitude (float): Integrated magnitude of the object.
        object_diameter1 (float): Major axis diameter in arcseconds.
        object_diameter2 (float): Minor axis diameter in arcseconds.

    Returns:
        float: Surface brightness in magnitudes per square arcsecond.

    Raises:
        InvalidParameterError: If any parameter is invalid.
    """
    # Validate inputs
    logger: logging = logging.getLogger(__name__)

    validate_number(magnitude, "Magnitude")
    validate_positive(object_diameter1, "Object diameter 1")
    validate_positive(object_diameter2, "Object diameter 2")

    return magnitude + (2.5 * math.log10(2827.0 * (object_diameter1 / 60) * (object_diameter2 / 60)))


def validate_contrast_reserve_inputs(
        sqm: float, telescope_diameter: float, magnification: float, 
        surf_brightness: Optional[float], magnitude: Optional[float],
        object_diameter1: Optional[float], object_diameter2: Optional[float]
) -> None:
    """
    Validate the inputs for the contrast reserve calculation.

    This function ensures that all required parameters for the contrast reserve calculation
    are of valid types and within acceptable ranges. It checks for the presence of required
    parameters and validates optional parameters if provided.

    Args:
        sqm (float): The sky quality meter reading, representing the sky brightness in magnitudes per square arcsecond.
        telescope_diameter (float): The diameter of the telescope in millimeters.
        magnification (float): The magnification of the telescope.
        surf_brightness (Optional[float]): The surface brightness of the object in magnitudes per square arcsecond.
        magnitude (Optional[float]): The integrated magnitude of the object.
        object_diameter1 (Optional[float]): The major axis diameter of the object in arcseconds.
        object_diameter2 (Optional[float]): The minor axis diameter of the object in arcseconds.

    Raises:
        InvalidParameterError: If any parameter is invalid (e.g., out of range, incorrect type).
    """
    # Validate required numeric inputs
    logger: logging = logging.getLogger(__name__)

    validate_number(sqm, "SQM")
    validate_positive(telescope_diameter, "Telescope diameter")
    validate_positive(magnification, "Magnification")
    validate_number(surf_brightness, "Surface brightness", allow_none=True)
    validate_number(magnitude, "Magnitude", allow_none=True)
    validate_positive(object_diameter1, "Object diameter 1", allow_none=True)
    validate_positive(object_diameter2, "Object diameter 2", allow_none=True)


def calculate_initial_parameters(
        sqm: float, telescope_diameter: float, 
        object_diameter1: float, object_diameter2: float
) -> Tuple[float, float, float, float]:
    """
    Calculate initial parameters for contrast reserve calculations.

    This function computes intermediate values such as the telescope aperture in inches,
    the sky background brightness at minimum magnification, and the object's angular size
    in arcminutes.

    Args:
        sqm (float): The sky quality meter reading in magnitudes per square arcsecond.
        telescope_diameter (float): The diameter of the telescope in millimeters.
        object_diameter1 (float): The major axis diameter of the object in arcseconds.
        object_diameter2 (float): The minor axis diameter of the object in arcseconds.

    Returns:
        Tuple[float, float, float, float]: A tuple containing:
            - Aperture in inches.
            - Sky background brightness at minimum magnification.
            - Major axis diameter in arcminutes.
            - Minor axis diameter in arcminutes.

    Raises:
        InvalidParameterError: If object diameters are not provided or invalid.
    """
    logger: logging = logging.getLogger(__name__)

    aperture_in_inches = telescope_diameter / 25.4
    
    # Minimum useful magnification
    sbb1 = sqm - (5 * math.log10(2.833 * aperture_in_inches))
    # Validate objectdiameters
    if object_diameter1 is None or object_diameter2 is None:
        # If the object diameters are not given, we cannot calculate the contrast reserve
        logger.error("Cannot calculate contrast reserve, missing object diameters")
        raise InvalidParameterError("Object diameters must be provided to calculate contrast reserve")

    object_diameter1_in_arc_minutes = object_diameter1 / 60.0
    object_diameter2_in_arc_minutes = object_diameter2 / 60.0
    
    # Ensure object_diameter1 is the smaller one
    if object_diameter1_in_arc_minutes > object_diameter2_in_arc_minutes:
        object_diameter1_in_arc_minutes, object_diameter2_in_arc_minutes = (
            object_diameter2_in_arc_minutes, object_diameter1_in_arc_minutes)
            
    return aperture_in_inches, sbb1, object_diameter1_in_arc_minutes, object_diameter2_in_arc_minutes


def calculate_log_object_contrast(
        sqm: float, surf_brightness: Optional[float], magnitude: Optional[float],
        object_diameter1: Optional[float], object_diameter2: Optional[float]
) -> float:
    """
    Calculate the logarithmic object contrast.

    The object contrast is a measure of the difference in brightness between the object
    and the background sky. This function computes the logarithmic contrast using either
    the surface brightness or the integrated magnitude and object dimensions.

    Args:
        sqm (float): The sky quality meter reading in magnitudes per square arcsecond.
        surf_brightness (Optional[float]): The surface brightness of the object in magnitudes per square arcsecond.
        magnitude (Optional[float]): The integrated magnitude of the object.
        object_diameter1 (Optional[float]): The major axis diameter of the object in arcseconds.
        object_diameter2 (Optional[float]): The minor axis diameter of the object in arcseconds.

    Returns:
        float: The logarithmic object contrast.

    Raises:
        InvalidParameterError: If required parameters are missing or invalid.
    """
    logger: logging = logging.getLogger(__name__)

    if surf_brightness:
        # If the surface brightness is given, use it to calculate the log object contrast
        # Convert surf_brightness to magnitudes per square arc second
        log_object_contrast = -0.4 * (surf_brightness + 8.89 - sqm)
    else:
        # Check if the magnitude, object_diameter1, and object_diameter2 are given
        if magnitude is None:
            # If not, we cannot calculate the log object contrast
            logger.error("Cannot calculate log object contrast, missing parameters")
            raise InvalidParameterError("Magnitude must be provided if surface brightness is not given")
        log_object_contrast = -0.4 * (surface_brightness(magnitude, object_diameter1, object_diameter2) - sqm)
            
    return log_object_contrast


def calculate_threshold_contrast(sky_background_brightness: float, angular_size_arcmin: float) -> float:
    max_log_contrast = 37
    log_angular_size = math.log10(angular_size_arcmin)
    """
    Interpolate the log threshold contrast for object detection based on sky brightness and object angular size.

    This function uses the Log Threshold Contrast (LTC) table and a logarithmic angular size grid to estimate
    the minimum contrast (in log units) required for visual detection of an astronomical object, given the
    sky background brightness and the object's angular size.

    The threshold contrast is determined by bilinear interpolation in the LTC table, where:
        - The rows correspond to integer sky background brightness values (in magnitudes per square arcsecond).
        - The columns correspond to log10(angular size in arcminutes).

    Args:
        sky_background_brightness (float): Sky background brightness in magnitudes per square arcsecond.
        angular_size_arcmin (float): Angular size of the object in arcminutes.

    Returns:
        float: The interpolated log threshold contrast required for detection.

    Raises:
        InvalidParameterError: If input parameters are invalid.

    Mathematical context:
        The function finds the appropriate indices in the LTC table for the given sky brightness and
        log(angular size), then performs linear interpolation along both axes to estimate the threshold.
        This value is used to compare with the object's actual contrast to assess detectability.
    """
    angle_index = 0

    # Get integer part of the sky background brightness
    int_sky_brightness = int(sky_background_brightness)

    # Calculate the index for the LTC table (row for sky brightness)
    sky_brightness_index_a = int_sky_brightness - 4

    # Ensure index is within bounds
    if sky_brightness_index_a < 0:
        sky_brightness_index_a = 0
    if sky_brightness_index_a > ContrastReserveConfig.LTC_SIZE - 2:
        sky_brightness_index_a = ContrastReserveConfig.LTC_SIZE - 2

    sky_brightness_index_b = sky_brightness_index_a + 1

    # Find the correct interval in ANGLE for interpolation
    while angle_index < ContrastReserveConfig.ANGLE_SIZE and log_angular_size > ContrastReserveConfig.ANGLE[angle_index]:
        angle_index += 1

    angle_index += 1
    angle_index -= 2

    if angle_index < 0:
        angle_index = 0
        log_angular_size = ContrastReserveConfig.ANGLE[0]

    if angle_index == ContrastReserveConfig.ANGLE_SIZE - 1:
        angle_index = ContrastReserveConfig.ANGLE_SIZE - 2


    # Interpolate between ANGLE grid points
    angle_fraction = (
        (log_angular_size - ContrastReserveConfig.ANGLE[angle_index]) /
        (ContrastReserveConfig.ANGLE[angle_index + 1] - ContrastReserveConfig.ANGLE[angle_index])
    )

    # Interpolate threshold contrast for both sky brightness indices
    interpolated_contrast_a = (
        ContrastReserveConfig.LTC[sky_brightness_index_a][angle_index + 1] +
        angle_fraction * (
            ContrastReserveConfig.LTC[sky_brightness_index_a][angle_index + 2] -
            ContrastReserveConfig.LTC[sky_brightness_index_a][angle_index + 1]
        )
    )
    interpolated_contrast_b = (
        ContrastReserveConfig.LTC[sky_brightness_index_b][angle_index + 1] +
        angle_fraction * (
            ContrastReserveConfig.LTC[sky_brightness_index_b][angle_index + 2] -
            ContrastReserveConfig.LTC[sky_brightness_index_b][angle_index + 1]
        )
    )

    if sky_background_brightness < ContrastReserveConfig.LTC[0][0]:
        sky_background_brightness = ContrastReserveConfig.LTC[0][0]

    if int_sky_brightness >= ContrastReserveConfig.LTC[ContrastReserveConfig.LTC_SIZE - 1][0]:
        log_threshold_contrast = (
            interpolated_contrast_b +
            (sky_background_brightness - ContrastReserveConfig.LTC[ContrastReserveConfig.LTC_SIZE - 1][0]) *
            (interpolated_contrast_b - interpolated_contrast_a)
        )
    else:
        log_threshold_contrast = (
            interpolated_contrast_a +
            (sky_background_brightness - int_sky_brightness) *
            (interpolated_contrast_b - interpolated_contrast_a)
        )

    if log_threshold_contrast > max_log_contrast:
        log_threshold_contrast = max_log_contrast
    elif log_threshold_contrast < -max_log_contrast:
        log_threshold_contrast = -max_log_contrast

    return log_threshold_contrast


def contrast_reserve(
        sqm: float, telescope_diameter: float, magnification: float, surf_brightness: Optional[float],
        magnitude: Optional[float], object_diameter1: Optional[float], object_diameter2: Optional[float]
) -> float:
    """
    Calculate the contrast reserve for visual detection of an astronomical object.

    The contrast reserve quantifies how much the object's contrast exceeds the minimum threshold required for detection,
    based on the observer's sky brightness, telescope, magnification, and object properties.

    The calculation involves:
        1. Computing the object's log contrast relative to the sky background, using either its surface brightness or
           integrated magnitude and size.
        2. Estimating the sky background brightness and the object's angular size at the given magnification.
        3. Interpolating the log threshold contrast from the Log Threshold Contrast (LTC) table, which models human
           visual detection limits as a function of sky brightness and object size.
        4. Subtracting the threshold from the object's log contrast to yield the contrast reserve.

    Interpretation of the result:
        - If contrast reserve < -0.2: Object is not visible.
        - -0.2 <= contrast reserve < 0.1: Questionable detection.
        - 0.1 <= contrast reserve < 0.35: Difficult.
        - 0.35 <= contrast reserve < 0.5: Quite difficult to see.
        - 0.5 <= contrast reserve < 1.0: Easy to see.
        - >= 1.0: Very easy to see.

    Args:
        sqm (float): Sky Quality Meter reading (sky brightness) in magnitudes per square arcsecond.
        telescope_diameter (float): Diameter of the telescope in millimeters.
        magnification (float): Magnification used.
        surf_brightness (Optional[float]): Surface brightness of the object in magnitudes per square arcsecond.
        magnitude (Optional[float]): Integrated magnitude of the object (required if surface brightness is not given).
        object_diameter1 (Optional[float]): Major axis diameter of the object in arcseconds.
        object_diameter2 (Optional[float]): Minor axis diameter of the object in arcseconds.

    Returns:
        float: The contrast reserve (difference between object and threshold log contrast).

    Raises:
        InvalidParameterError: If any parameter is missing or invalid.

    Mathematical context:
        - Log object contrast is computed as:
            logC = -0.4 * (SB + 8.89 - SQM)
          or, if surface brightness is not given, SB is derived from magnitude and size.
        - Threshold contrast is interpolated from the LTC table using sky brightness and log10(angular size).
        - Contrast reserve = log object contrast - log threshold contrast.
    """
    # Log a string using python logger
    logger: logging = logging.getLogger(__name__)
    logger.info("Calculating the contrast reserve")
    
    # Validate inputs
    validate_contrast_reserve_inputs(
        sqm, telescope_diameter, magnification, 
        surf_brightness, magnitude, object_diameter1, object_diameter2
    )
    
    # Calculate initial parameters
    try:
        aperture_in_inches, sbb1, object_diameter1_in_arc_minutes, object_diameter2_in_arc_minutes = calculate_initial_parameters(
            sqm, telescope_diameter, object_diameter1, object_diameter2
        )
    except InvalidParameterError as e:
        raise

    # Calculate log object contrast
    log_object_contrast = calculate_log_object_contrast(
        sqm, surf_brightness, magnitude, object_diameter1, object_diameter2
    )

    # Calculate sky background brightness with magnification
    sbb = sbb1 + 5 * math.log10(magnification)
    
    # Calculate angular size with magnification
    ang = magnification * object_diameter1_in_arc_minutes
    
    # Calculate threshold contrast
    log_threshold_contrast = calculate_threshold_contrast(sbb, ang)
    
    # Calculate contrast difference
    log_contrast_difference = log_object_contrast - log_threshold_contrast
    
    return log_contrast_difference


def optimal_detection_magnification(
        sqm: float, telescope_diameter: float, surf_brightness: Optional[float],
        magnitude: Optional[float], object_diameter1: Optional[float], object_diameter2: Optional[float],
        magnifications: List[float]) -> float:
    """
    Determine the optimal magnification for visually detecting an astronomical object.

    This function evaluates a list of possible magnifications and selects the one that maximizes the contrast reserve,
    i.e., the difference between the object's contrast and the minimum threshold required for detection. The calculation
    considers the observer's sky brightness (SQM), telescope diameter, object properties, and available magnifications.

    The process involves:
        1. For each magnification, compute the contrast reserve using the object's surface brightness or integrated
           magnitude and size, the telescope's parameters, and the sky background.
        2. The contrast reserve is calculated as the difference between the object's log contrast and the threshold
           contrast interpolated from the Log Threshold Contrast (LTC) table.
        3. The magnification yielding the highest contrast reserve is returned as optimal for detection.

    Args:
        sqm (float): Sky Quality Meter reading (sky brightness) in magnitudes per square arcsecond.
        telescope_diameter (float): Diameter of the telescope in millimeters.
        surf_brightness (Optional[float]): Surface brightness of the object in magnitudes per square arcsecond.
        magnitude (Optional[float]): Integrated magnitude of the object (required if surface brightness is not given).
        object_diameter1 (Optional[float]): Major axis diameter of the object in arcseconds.
        object_diameter2 (Optional[float]): Minor axis diameter of the object in arcseconds.
        magnifications (List[float]): List of available magnifications to evaluate.

    Returns:
        float: The magnification that provides the highest contrast reserve (i.e., optimal for detection).

    Raises:
        InvalidParameterError: If any parameter is missing or invalid.

    Mathematical context:
        - For each magnification, the function computes the contrast reserve using the `contrast_reserve` function.
        - The optimal magnification is the one that maximizes this value, improving the likelihood of visual detection.
    """
    # Validate required numeric inputs
    logger: logging = logging.getLogger(__name__)

    validate_number(sqm, "SQM")
    validate_positive(telescope_diameter, "Telescope diameter")

    # Validate surf_brightness if provided
    if surf_brightness is not None:
        validate_number(surf_brightness, "Surface brightness")

    # Validate magnitude if provided and needed
    if surf_brightness is None and magnitude is not None:
        validate_number(magnitude, "Magnitude")

    # Validate object diameters if provided
    if object_diameter1 is not None and not isinstance(object_diameter1, (int, float)):
        validate_positive(object_diameter1, "Object diameter 1")
    if object_diameter2 is not None and not isinstance(object_diameter2, (int, float)):
        validate_positive(object_diameter2, "Object diameter 2")

    # Validate magnifications list
    if not isinstance(magnifications, list):
        logger.error("Magnifications parameter is not a list")
        raise InvalidParameterError("Magnifications must be a list")
    
    # Validate each magnification in the list
    for mag in magnifications:
        validate_positive(mag, "Each magnification")

    best_contrast = -999
    best_x = 0

    for magnification in magnifications:
        contrast = contrast_reserve(
            sqm, telescope_diameter, magnification, surf_brightness, magnitude, object_diameter1, object_diameter2)
        if contrast > best_contrast:
            best_contrast = contrast
            best_x = magnification

    return best_x