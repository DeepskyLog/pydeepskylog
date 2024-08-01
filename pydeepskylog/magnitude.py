import math


def nelm_to_sqm(nelm: float, fst_offset=0.0) -> float:
    """
    Calculate the SQM value from the NELM (Naked Eye Limiting Magnitude) value. In these calculations, the NELM value is
    maximum 6.7.

    :param nelm: The Naked Eye Limiting Magnitude
    :param fst_offset: The offset between the real Nelm and the Nelm for the observer

    :return: The SQM value
    """
    sqm = 21.58 - 5 * math.log10(math.pow(10, 1.586 - (nelm + fst_offset) / 5.0) - 1.0)

    if sqm > 22.0:
        return 22.0
    else:
        return sqm


def nelm_to_bortle(nelm: float) -> int:
    """
    Calculate the Bortle scale value from the NELM (Naked Eye Limiting Magnitude) value. In these calculations, the NELM
    value is maximum 6.7.
    :param nelm: The Naked Eye Limiting Magnitude
    :return: The Bortle scale value (1 - 9)
    """
    if nelm < 3.6:
        return 9
    elif nelm < 3.9:
        return 8
    elif nelm < 4.4:
        return 7
    elif nelm < 4.9:
        return 6
    elif nelm < 5.8:
        return 5
    elif nelm < 6.3:
        return 4
    elif nelm < 6.4:
        return 3
    elif nelm < 6.5:
        return 2
    else:
        return 1


def sqm_to_bortle(sqm: float) -> int:
    """
    Calculate the Bortle scale value from the SQM (Sky Quality Meter) value.

    :param sqm: The Sky Quality Meter value
    :return: The Bortle scale value (1 - 9)
    """
    if sqm <= 17.5:
        return 9
    elif sqm <= 18.0:
        return 8
    elif sqm <= 18.5:
        return 7
    elif sqm <= 19.1:
        return 6
    elif sqm <= 20.4:
        return 5
    elif sqm <= 21.3:
        return 4
    elif sqm <= 21.5:
        return 3
    elif sqm <= 21.7:
        return 2
    else:
        return 1


def sqm_to_nelm(sqm: float, fst_offset=0.0) -> float:
    """
    Calculate the Naked Eye Limiting Magnitude from the SQM (Sky Quality Meter) value.
    :param sqm: The SQM value
    :param fst_offset: The offset between the real Nelm and the Nelm for the observer

    :return: The Naked Eye Limiting Magnitude
    """
    nelm = 7.93 - 5 * math.log10(1 + math.pow(10, 4.316 - sqm / 5.0))

    if nelm < 2.5:
        nelm = 2.5

    return nelm - fst_offset


def bortle_to_nelm(bortle: int, fst_offset=0.0) -> float:
    """
    Calculate the NELM value if the bortle scale is given.

    :param bortle: The bortle scale
    :param fst_offset: The offset between the real Nelm and the Nelm for the observer

    :return: The NELM value
    """

    if bortle == 1:
        return 6.6 - fst_offset
    elif bortle == 2:
        return 6.5 - fst_offset
    elif bortle == 3:
        return 6.4 - fst_offset
    elif bortle == 4:
        return 6.1 - fst_offset
    elif bortle == 5:
        return 5.4 - fst_offset
    elif bortle == 6:
        return 4.7 - fst_offset
    elif bortle == 7:
        return 4.2 - fst_offset
    elif bortle == 8:
        return 3.8 - fst_offset
    elif bortle == 9:
        return 3.6 - fst_offset
    else:
        return 0.0


def bortle_to_sqm(bortle: int) -> float:
    """
    Calculate the SQM value if the bortle scale is given.

    :param bortle: The bortle scale
    :return: The SQM value
    """
    if bortle == 1:
        return 21.85
    elif bortle == 2:
        return 21.6
    elif bortle == 3:
        return 21.4
    elif bortle == 4:
        return 20.85
    elif bortle == 5:
        return 19.75
    elif bortle == 6:
        return 18.8
    elif bortle == 7:
        return 18.25
    elif bortle == 8:
        return 17.75
    elif bortle == 9:
        return 17.5
    else:
        return 0.0
