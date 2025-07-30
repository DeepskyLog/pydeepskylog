"""
Configuration file for pydeepskylog package.
Contains constants and configuration values used across the package.
"""
from typing import List

# Constants for contrast reserve calculations
class ContrastReserveConfig:
    """
    Configuration class for contrast reserve calculations.
    Contains constants used in the contrast_reserve.py module.
    """
    # ANGLE: Logarithmic angular size grid
    # ANGLE is a 1D array of log10(angular size in arcminutes) values.
    # Each entry defines a grid point for the angular size axis in the LTC table.
    # Used for interpolation of threshold contrast as a function of object angular size.
    ANGLE: List[float] = [
        -0.2255, 0.5563, 0.9859, 1.260,
        1.742, 2.083, 2.556,
    ]

    ANGLE_SIZE: int = len(ANGLE)

    # LTC: Log Threshold Contrast Table
    # LTC is a 2D array where each row corresponds to a specific sky background brightness (integer values from 4 to 23).
    # Each column corresponds to a log10(angular size) value as defined in the ANGLE array.
    # LTC[sb][i] gives the log threshold contrast for sky brightness index sb and angle index i.
    # Used for interpolating the minimum contrast required for detection at given sky brightness and object size.
    LTC: List[List[float]] = [
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

    LTC_SIZE: int = len(LTC)
