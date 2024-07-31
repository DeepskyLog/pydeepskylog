import logging
import math

_LTCSize = 24
_angleSize = 7
_angle = [
    -0.2255, 0.5563, 0.9859, 1.260,
    1.742, 2.083, 2.556,
]
_LTC = [
    [
        4, -0.3769, -1.8064, -2.3368, -2.4601,
        -2.5469, -2.5610, -2.5660,
    ],
    [
        5, -0.3315, -1.7747, -2.3337, -2.4608,
        -2.5465, -2.5607, -2.5658,
    ],
    [
        6, -0.2682, -1.7345, -2.3310, -2.4605,
        -2.5467, -2.5608, -2.5658,
    ],
    [
        7, -0.1982, -1.6851, -2.3140, -2.4572,
        -2.5481, -2.5615, -2.5665,
    ],
    [
        8, -0.1238, -1.6252, -2.2791, -2.4462,
        -2.5463, -2.5597, -2.5646,
    ],
    [
        9, -0.0424, -1.5529, -2.2297, -2.4214,
        -2.5343, -2.5501, -2.5552,
    ],
    [
        10, 0.0498, -1.4655, -2.1659, -2.3763,
        -2.5047, -2.5269, -2.5333,
    ],
    [
        11, 0.1596, -1.3581, -2.0810, -2.3036,
        -2.4499, -2.4823, -2.4937,
    ],
    [
        12, 0.2934, -1.2256, -1.9674, -2.1965,
        -2.3631, -2.4092, -2.4318,
    ],
    [
        13, 0.4557, -1.0673, -1.8186, -2.0531,
        -2.2445, -2.3083, -2.3491,
    ],
    [
        14, 0.6500, -0.8841, -1.6292, -1.8741,
        -2.0989, -2.1848, -2.2505,
    ],
    [
        15, 0.8808, -0.6687, -1.3967, -1.6611,
        -1.9284, -2.0411, -2.1375,
    ],
    [
        16, 1.1558, -0.3952, -1.1264, -1.4176,
        -1.7300, -1.8727, -2.0034,
    ],
    [
        17, 1.4822, -0.0419, -0.8243, -1.1475,
        -1.5021, -1.6768, -1.8420,
    ],
    [
        18, 1.8559, 0.3458, -0.4924, -0.8561,
        -1.2661, -1.4721, -1.6624,
    ],
    [
        19, 2.2669, 0.6960, -0.1315, -0.5510,
        -1.0562, -1.2892, -1.4827,
    ],
    [
        20, 2.6760, 1.0880, 0.2060, -0.3210,
        -0.8800, -1.1370, -1.3620,
    ],
    [
        21, 2.7766, 1.2065, 0.3467, -0.1377,
        -0.7361, -0.9964, -1.2439,
    ],
    [
        22, 2.9304, 1.3821, 0.5353, 0.0328,
        -0.5605, -0.8606, -1.1187,
    ],
    [
        23, 3.1634, 1.6107, 0.7708, 0.2531,
        -0.3895, -0.7030, -0.9681,
    ],
    [
        24, 3.4643, 1.9034, 1.0338, 0.4943,
        -0.2033, -0.5259, -0.8288,
    ],
    [
        25, 3.8211, 2.2564, 1.3265, 0.7605,
        0.0172, -0.2992, -0.6394,
    ],
    [
        26, 4.2210, 2.6320, 1.6990, 1.1320,
        0.2860, -0.0510, -0.4080,
    ],
    [
        27, 4.6100, 3.0660, 2.1320, 1.5850,
        0.6520, 0.2410, -0.1210,
    ],
]


def surface_brightness(magnitude: float, object_diameter1: float, object_diameter2: float) -> float:
    """
    Calculates the surface brightness of the target.  This is needed to calculate the contrast of the target.
    :param magnitude: The magnitude of the object
    :param object_diameter1: The diameter along the major axis of the object in arc seconds
    :param object_diameter2: The diameter along the minor axis of the object in arc seconds
    :return: The surface brightness of the object in magnitudes per square arc second
    """
    return magnitude + (2.5 * math.log10(2827.0 * (object_diameter1 / 60) * (object_diameter2 / 60)))


def contrast_reserve(
        sqm: float, telescope_diameter: float, magnification: float, magnitude: float,
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
    :param magnitude: The magnitude of the object to observe
    :param object_diameter1: The diameter along the major axis of the object in arc seconds
    :param object_diameter2: The diameter along the minor axis of the object in arc seconds

    :return: The contrast reserve of the object
    """
    # Log a string using python logger
    logger = logging.getLogger()
    logger.info("Calculating the contrast reserve")

    aperture_in_inches = telescope_diameter / 25.4

    # Minimum useful magnification
    sbb1: float = sqm - (5 * math.log10(2.833 * aperture_in_inches))

    object_diameter1_in_arc_minutes = object_diameter1 / 60.0
    object_diameter2_in_arc_minutes = object_diameter2 / 60.0

    if object_diameter1_in_arc_minutes > object_diameter2_in_arc_minutes:
        object_diameter1_in_arc_minutes, object_diameter2_in_arc_minutes = (
            object_diameter2_in_arc_minutes, object_diameter1_in_arc_minutes)

    max_log = 37

    # Log Object contrast
    log_object_contrast = -0.4 * (surface_brightness(magnitude, object_diameter1, object_diameter2) - sqm)

    # The preparations are finished, we can now start the calculations
    x = magnification

    sbb = sbb1 + 5 * math.log10(x)

    # 2-dimensional interpolation of LTC array
    ang = x * object_diameter1_in_arc_minutes
    log_angle = math.log10(ang)
    sb = sbb
    i = 0

    # int of surface brightness
    # Get integer of the surface brightness
    int_sb = int(sb)

    # surface brightness index A
    sb_ia = int_sb - 4

    # min index must be at least 0
    if sb_ia < 0:
        sb_ia = 0

    # max sb_ia index cannot > 22 so that max sb_ib <= 23
    if sb_ia > _LTCSize - 2:
        sb_ia = _LTCSize - 2

    # surface brightness index B
    sb_ib = sb_ia + 1

    while i < _angleSize and log_angle > _angle[i]:
        i = i + 1

    i += 1

    # found 1st Angle[] value > LogAng, so back up 2
    i -= 2

    if i < 0:
        i = 0
        log_angle = _angle[0]

    if i == _angleSize - 1:
        i = _angleSize - 2

    # ie, if log_angle = 4 and angle[i] = 3 and Angle[i+1] = 5, interpolated_angle = .5, or .5 of the way between
    # angle[i] and angle[i + 1]
    interpolated_angle = (log_angle - _angle[i]) / (_angle[i + 1] - _angle[i])

    # add 1 to i because first entry in LTC is sky background brightness
    interpolated_a = _LTC[sb_ia][i + 1] + interpolated_angle * (_LTC[sb_ia][i + 2] - _LTC[sb_ia][i + 1])
    interpolated_b = _LTC[sb_ib][i + 1] + interpolated_angle * (_LTC[sb_ib][i + 2] - _LTC[sb_ib][i + 1])

    if sb < _LTC[0][0]:
        sb = _LTC[0][0]

    if int_sb >= _LTC[_LTCSize - 1][0]:
        log_threshold_contrast = interpolated_b + (sb - _LTC[_LTCSize - 1][0]) * (interpolated_b - interpolated_a)
    else:
        log_threshold_contrast = interpolated_a + (sb - int_sb) * (interpolated_b - interpolated_a)

    if log_threshold_contrast > max_log:
        log_threshold_contrast = max_log
    else:
        if log_threshold_contrast < -max_log:
            log_threshold_contrast = -max_log

    log_contrast_difference = log_object_contrast - log_threshold_contrast

    return log_contrast_difference


def optimal_detection_magnification(
        sqm: float, telescope_diameter: float, magnitude: float, object_diameter1: float, object_diameter2: float,
        magnifications: list) -> float:
    """
    Calculate the best magnification to use for the object to detect it

    :param sqm: The sky quality meter reading
    :param telescope_diameter: The diameter of the telescope in mm
    :param magnitude: The magnitude of the object to observe
    :param object_diameter1: The diameter along the major axis of the object in arc seconds
    :param object_diameter2: The diameter along the minor axis of the object in arc seconds
    :param magnifications: The list of magnifications available for the telescope
    :return: The best magnification to use for the object
    """
    best_contrast = -999
    best_x = 0

    for magnification in magnifications:
        contrast = contrast_reserve(
            sqm, telescope_diameter, magnification, magnitude, object_diameter1, object_diameter2)
        if contrast > best_contrast:
            best_contrast = contrast
            best_x = magnification

    return best_x


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Calculate the surface brightness of an object
    print(surface_brightness(15, 8220, 8220))

    # Calculate the contrast reserve of an object
    print(contrast_reserve(22, 457, 118, 11, 600, 600))

    available_magnifications = [
        66, 103, 158, 257, 411,
        76, 118, 182, 296, 473,
        133, 206, 317, 514, 823,
    ]

    print(optimal_detection_magnification(20.15, 457, 11, 600, 600, available_magnifications))
