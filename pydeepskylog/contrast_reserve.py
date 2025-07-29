import logging
import math
from pydeepskylog.config import ContrastReserveConfig


def surface_brightness(magnitude: float, object_diameter1: float, object_diameter2: float) -> float:
    """
    Calculates the surface brightness of the target.  This is needed to calculate the contrast of the target.
    :param magnitude: The magnitude of the object
    :param object_diameter1: The diameter along the major axis of the object in arc seconds
    :param object_diameter2: The diameter along the minor axis of the object in arc seconds
    :return: The surface brightness of the object in magnitudes per square arc second
    :raises ValueError: If any parameter is not a number or if object diameters are not positive
    """
    # Validate inputs
    if not isinstance(magnitude, (int, float)):
        raise ValueError("Magnitude must be a number")
    if not isinstance(object_diameter1, (int, float)):
        raise ValueError("Object diameter 1 must be a number")
    if not isinstance(object_diameter2, (int, float)):
        raise ValueError("Object diameter 2 must be a number")
    
    # Check for positive diameters
    if object_diameter1 <= 0:
        raise ValueError("Object diameter 1 must be positive")
    if object_diameter2 <= 0:
        raise ValueError("Object diameter 2 must be positive")
        
    return magnitude + (2.5 * math.log10(2827.0 * (object_diameter1 / 60) * (object_diameter2 / 60)))


def validate_contrast_reserve_inputs(
        sqm: float, telescope_diameter: float, magnification: float, 
        surf_brightness: float, magnitude: float,
        object_diameter1: float, object_diameter2: float
) -> None:
    """
    Validates the inputs for the contrast_reserve function.
    
    :param sqm: The sky quality meter reading
    :param telescope_diameter: The diameter of the telescope in mm
    :param magnification: The magnification of the telescope
    :param surf_brightness: The surface brightness of the object in magnitudes per square arc second
    :param magnitude: The magnitude of the object to observe
    :param object_diameter1: The diameter along the major axis of the object in arc seconds
    :param object_diameter2: The diameter along the minor axis of the object in arc seconds
    :raises ValueError: If parameters have invalid types or values
    """
    # Validate required numeric inputs
    if not isinstance(sqm, (int, float)):
        raise ValueError("SQM must be a number")
    if not isinstance(telescope_diameter, (int, float)):
        raise ValueError("Telescope diameter must be a number")
    if not isinstance(magnification, (int, float)):
        raise ValueError("Magnification must be a number")
    
    # Check for positive values
    if telescope_diameter <= 0:
        raise ValueError("Telescope diameter must be positive")
    if magnification <= 0:
        raise ValueError("Magnification must be positive")
        
    # Validate surf_brightness if provided
    if surf_brightness is not None and not isinstance(surf_brightness, (int, float)):
        raise ValueError("Surface brightness must be a number or None")
        
    # Validate magnitude if provided and needed
    if surf_brightness is None and magnitude is not None:
        if not isinstance(magnitude, (int, float)):
            raise ValueError("Magnitude must be a number or None")
            
    # Validate object diameters if provided
    if object_diameter1 is not None and not isinstance(object_diameter1, (int, float)):
        raise ValueError("Object diameter 1 must be a number or None")
    if object_diameter2 is not None and not isinstance(object_diameter2, (int, float)):
        raise ValueError("Object diameter 2 must be a number or None")
        
    # Check for positive diameters if provided
    if object_diameter1 is not None and object_diameter1 <= 0:
        raise ValueError("Object diameter 1 must be positive")
    if object_diameter2 is not None and object_diameter2 <= 0:
        raise ValueError("Object diameter 2 must be positive")


def calculate_initial_parameters(
        sqm: float, telescope_diameter: float, 
        object_diameter1: float, object_diameter2: float
) -> tuple:
    """
    Calculates initial parameters needed for contrast reserve calculation.
    
    :param sqm: The sky quality meter reading
    :param telescope_diameter: The diameter of the telescope in mm
    :param object_diameter1: The diameter along the major axis of the object in arc seconds
    :param object_diameter2: The diameter along the minor axis of the object in arc seconds
    :return: A tuple containing (aperture_in_inches, sbb1, object_diameter1_in_arc_minutes, object_diameter2_in_arc_minutes)
    """
    logger = logging.getLogger()
    
    aperture_in_inches = telescope_diameter / 25.4
    
    # Minimum useful magnification
    sbb1 = sqm - (5 * math.log10(2.833 * aperture_in_inches))
    
    if object_diameter1 is None or object_diameter2 is None:
        # If the object diameters are not given, we cannot calculate the contrast reserve
        logger.error("Cannot calculate contrast reserve, missing object diameters")
        return None, None, None, None
        
    object_diameter1_in_arc_minutes = object_diameter1 / 60.0
    object_diameter2_in_arc_minutes = object_diameter2 / 60.0
    
    # Ensure object_diameter1 is the smaller one
    if object_diameter1_in_arc_minutes > object_diameter2_in_arc_minutes:
        object_diameter1_in_arc_minutes, object_diameter2_in_arc_minutes = (
            object_diameter2_in_arc_minutes, object_diameter1_in_arc_minutes)
            
    return aperture_in_inches, sbb1, object_diameter1_in_arc_minutes, object_diameter2_in_arc_minutes


def calculate_log_object_contrast(
        sqm: float, surf_brightness: float, magnitude: float,
        object_diameter1: float, object_diameter2: float
) -> float:
    """
    Calculates the log object contrast.
    
    :param sqm: The sky quality meter reading
    :param surf_brightness: The surface brightness of the object in magnitudes per square arc second
    :param magnitude: The magnitude of the object to observe
    :param object_diameter1: The diameter along the major axis of the object in arc seconds
    :param object_diameter2: The diameter along the minor axis of the object in arc seconds
    :return: The log object contrast
    """
    logger = logging.getLogger()
    
    if surf_brightness:
        # If the surface brightness is given, use it to calculate the log object contrast
        # Convert surf_brightness to magnitudes per square arc second
        log_object_contrast = -0.4 * (surf_brightness + 8.89 - sqm)
    else:
        # Check if the magnitude, object_diameter1, and object_diameter2 are given
        if magnitude is None:
            # If not, we cannot calculate the log object contrast
            logger.error("Cannot calculate log object contrast, missing parameters")
            return None
        log_object_contrast = -0.4 * (surface_brightness(magnitude, object_diameter1, object_diameter2) - sqm)
            
    return log_object_contrast


def calculate_threshold_contrast(sbb: float, ang: float) -> float:
    """
    Calculates the threshold contrast using LTC array interpolation.
    
    :param sbb: The sky background brightness
    :param ang: The angular size in arc minutes
    :return: The log threshold contrast
    """
    max_log = 37
    log_angle = math.log10(ang)
    i = 0
    
    # Get integer of the surface brightness
    int_sb = int(sbb)
    
    # surface brightness index A
    sb_ia = int_sb - 4
    
    # min index must be at least 0
    if sb_ia < 0:
        sb_ia = 0
    
    # max sb_ia index cannot > 22 so that max sb_ib <= 23
    if sb_ia > ContrastReserveConfig.LTC_SIZE - 2:
        sb_ia = ContrastReserveConfig.LTC_SIZE - 2
    
    # surface brightness index B
    sb_ib = sb_ia + 1
    
    while i < ContrastReserveConfig.ANGLE_SIZE and log_angle > ContrastReserveConfig.ANGLE[i]:
        i = i + 1
    
    i += 1
    
    # found 1st Angle[] value > LogAng, so back up 2
    i -= 2
    
    if i < 0:
        i = 0
        log_angle = ContrastReserveConfig.ANGLE[0]
    
    if i == ContrastReserveConfig.ANGLE_SIZE - 1:
        i = ContrastReserveConfig.ANGLE_SIZE - 2
    
    # ie, if log_angle = 4 and angle[i] = 3 and Angle[i+1] = 5, interpolated_angle = .5, or .5 of the way between
    # angle[i] and angle[i + 1]
    interpolated_angle = (log_angle - ContrastReserveConfig.ANGLE[i]) / (ContrastReserveConfig.ANGLE[i + 1] - ContrastReserveConfig.ANGLE[i])
    
    # add 1 to i because first entry in LTC is sky background brightness
    interpolated_a = ContrastReserveConfig.LTC[sb_ia][i + 1] + interpolated_angle * (ContrastReserveConfig.LTC[sb_ia][i + 2] - ContrastReserveConfig.LTC[sb_ia][i + 1])
    interpolated_b = ContrastReserveConfig.LTC[sb_ib][i + 1] + interpolated_angle * (ContrastReserveConfig.LTC[sb_ib][i + 2] - ContrastReserveConfig.LTC[sb_ib][i + 1])
    
    if sbb < ContrastReserveConfig.LTC[0][0]:
        sbb = ContrastReserveConfig.LTC[0][0]
    
    if int_sb >= ContrastReserveConfig.LTC[ContrastReserveConfig.LTC_SIZE - 1][0]:
        log_threshold_contrast = interpolated_b + (sbb - ContrastReserveConfig.LTC[ContrastReserveConfig.LTC_SIZE - 1][0]) * (interpolated_b - interpolated_a)
    else:
        log_threshold_contrast = interpolated_a + (sbb - int_sb) * (interpolated_b - interpolated_a)
    
    if log_threshold_contrast > max_log:
        log_threshold_contrast = max_log
    elif log_threshold_contrast < -max_log:
        log_threshold_contrast = -max_log
        
    return log_threshold_contrast


def contrast_reserve(
        sqm: float, telescope_diameter: float, magnification: float, surf_brightness: float, magnitude: float,
        object_diameter1: float, object_diameter2: float
) -> float:
    """
    Calculate the contrast reserve
    If the contrast difference is < -0.2, the object is not visible
        -0.2 < contrast diff < 0.1 : questionable
        0.10 < contrast diff < 0.35 : Difficult
        0.35 < contrast diff < 0.5 : Quite difficult to see
        0.50 < contrast diff < 1.0 : Easy to see
        1.00 < contrast diff : Very easy to see.

    :param sqm: The sky quality meter reading
    :param telescope_diameter: The diameter of the telescope in mm
    :param magnification: The magnification of the telescope
    :param surf_brightness: The surface brightness of the object in magnitudes per square arc second
    :param magnitude: The magnitude of the object to observe
    :param object_diameter1: The diameter along the major axis of the object in arc seconds
    :param object_diameter2: The diameter along the minor axis of the object in arc seconds

    :return: The contrast reserve of the object
    :raises ValueError: If parameters have invalid types or values
    """
    # Log a string using python logger
    logger = logging.getLogger()
    logger.info("Calculating the contrast reserve")
    
    # Validate inputs
    validate_contrast_reserve_inputs(
        sqm, telescope_diameter, magnification, 
        surf_brightness, magnitude, object_diameter1, object_diameter2
    )
    
    # Calculate initial parameters
    aperture_in_inches, sbb1, object_diameter1_in_arc_minutes, object_diameter2_in_arc_minutes = calculate_initial_parameters(
        sqm, telescope_diameter, object_diameter1, object_diameter2
    )
    
    # If any of the initial parameters are None, we cannot proceed
    if None in (aperture_in_inches, sbb1, object_diameter1_in_arc_minutes, object_diameter2_in_arc_minutes):
        return None
    
    # Calculate log object contrast
    log_object_contrast = calculate_log_object_contrast(
        sqm, surf_brightness, magnitude, object_diameter1, object_diameter2
    )
    
    # If log_object_contrast is None, we cannot proceed
    if log_object_contrast is None:
        return None
    
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
        sqm: float, telescope_diameter: float, surf_brightness: float, magnitude: float, object_diameter1: float, object_diameter2: float,
        magnifications: list) -> float:
    """
    Calculate the best magnification to use for the object to detect it

    :param sqm: The sky quality meter reading
    :param telescope_diameter: The diameter of the telescope in mm
    :param surf_brightness: The surface brightness of the object in magnitudes per square arc second
    :param magnitude: The magnitude of the object to observe
    :param object_diameter1: The diameter along the major axis of the object in arc seconds
    :param object_diameter2: The diameter along the minor axis of the object in arc seconds
    :param magnifications: The list of magnifications available for the telescope
    :return: The best magnification to use for the object
    :raises ValueError: If parameters have invalid types or values
    """
    # Validate required numeric inputs
    if not isinstance(sqm, (int, float)):
        raise ValueError("SQM must be a number")
    if not isinstance(telescope_diameter, (int, float)):
        raise ValueError("Telescope diameter must be a number")
    
    # Check for positive telescope diameter
    if telescope_diameter <= 0:
        raise ValueError("Telescope diameter must be positive")
        
    # Validate surf_brightness if provided
    if surf_brightness is not None and not isinstance(surf_brightness, (int, float)):
        raise ValueError("Surface brightness must be a number or None")
        
    # Validate magnitude if provided and needed
    if surf_brightness is None and magnitude is not None:
        if not isinstance(magnitude, (int, float)):
            raise ValueError("Magnitude must be a number or None")
            
    # Validate object diameters if provided
    if object_diameter1 is not None and not isinstance(object_diameter1, (int, float)):
        raise ValueError("Object diameter 1 must be a number or None")
    if object_diameter2 is not None and not isinstance(object_diameter2, (int, float)):
        raise ValueError("Object diameter 2 must be a number or None")
        
    # Check for positive diameters if provided
    if object_diameter1 is not None and object_diameter1 <= 0:
        raise ValueError("Object diameter 1 must be positive")
    if object_diameter2 is not None and object_diameter2 <= 0:
        raise ValueError("Object diameter 2 must be positive")
        
    # Validate magnifications list
    if not isinstance(magnifications, list):
        raise ValueError("Magnifications must be a list")
    
    # Validate each magnification in the list
    for mag in magnifications:
        if not isinstance(mag, (int, float)):
            raise ValueError("Each magnification must be a number")
        if mag <= 0:
            raise ValueError("Each magnification must be positive")
    
    best_contrast = -999
    best_x = 0

    for magnification in magnifications:
        contrast = contrast_reserve(
            sqm, telescope_diameter, magnification, surf_brightness, magnitude, object_diameter1, object_diameter2)
        if contrast > best_contrast:
            best_contrast = contrast
            best_x = magnification

    return best_x