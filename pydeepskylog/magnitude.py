import math


def nelm_to_sqm(nelm: float, fst_offset:float=0.0) -> float:
    """
    Calculate the SQM value from the NELM (Naked Eye Limiting Magnitude) value. In these calculations, the NELM value is
    maximum 6.7.

    Formula:
        SQM = 21.58 - 5 * log10(10^(1.586 - (NELM + fst_offset)/5) - 1)
    This formula estimates the sky brightness (SQM) from the limiting magnitude visible to the naked eye.

    :param nelm: The Naked Eye Limiting Magnitude
    :param fst_offset: The offset between the real Nelm and the Nelm for the observer

    :return: The SQM value
    """
    if not isinstance(nelm, (int, float)):
        raise ValueError("NELM must be a number")
    if not isinstance(fst_offset, (int, float)):
        raise ValueError("fst_offset must be a number")
    if nelm < 0 or nelm > 6.7:
        raise ValueError("NELM must be between 0 and 6.7")
    try:
        exponent = 1.586 - (nelm + fst_offset) / 5.0
        base = math.pow(10, exponent) - 1.0
        if base <= 0:
            raise ValueError("Invalid calculation: log10 argument must be positive")
        sqm = 21.58 - 5 * math.log10(base)
    except (ValueError, OverflowError) as e:
        raise ValueError(f"Error in SQM calculation: {e}")
    return min(sqm, 22.0)


def nelm_to_bortle(nelm: float) -> int:
    """
    Calculate the Bortle scale value from the NELM (Naked Eye Limiting Magnitude) value. In these calculations, the NELM
    value is maximum 6.7.

    The Bortle scale is mapped from NELM using threshold values based on observational standards.

    :param nelm: The Naked Eye Limiting Magnitude
    :return: The Bortle scale value (1 - 9)
    """
    if not isinstance(nelm, (int, float)):
        raise ValueError("NELM must be a number")

    if nelm < 0 or nelm > 6.7:
        raise ValueError("NELM must be between 0 and 6.7")
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

    The Bortle scale is mapped from SQM using threshold values based on observational standards.

    :param sqm: The Sky Quality Meter value
    :return: The Bortle scale value (1 - 9)
    """
    if not isinstance(sqm, (int, float)):
        raise ValueError("SQM must be a number")
    if sqm < 0 or sqm > 22:
        raise ValueError("SQM must be between 0 and 22")
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


def sqm_to_nelm(sqm: float, fst_offset: float=0.0) -> float:
    """
    Calculate the Naked Eye Limiting Magnitude from the SQM (Sky Quality Meter) value.

    Formula:
        NELM = 7.93 - 5 * log10(1 + 10^(4.316 - SQM/5))
    This formula estimates the faintest star visible to the naked eye from the measured sky brightness.

    :param sqm: The SQM value
    :param fst_offset: The offset between the real Nelm and the Nelm for the observer
    :return: The Naked Eye Limiting Magnitude
    """
    if not isinstance(sqm, (int, float)):
        raise ValueError("SQM must be a number")
    if not isinstance(fst_offset, (int, float)):
        raise ValueError("fst_offset must be a number")
    if sqm < 0 or sqm > 22:
        raise ValueError("SQM must be between 0 and 22")
    try:
        base = 1 + math.pow(10, 4.316 - sqm / 5.0)
        if base <= 0:
            raise ValueError("Invalid calculation: log10 argument must be positive")
        nelm = 7.93 - 5 * math.log10(base)
    except (ValueError, OverflowError) as e:
        raise ValueError(f"Error in NELM calculation: {e}")
    if nelm < 2.5:
        nelm = 2.5
    return nelm - fst_offset


def bortle_to_nelm(bortle: int, fst_offset: float=0.0) -> float:
    """
    Calculate the NELM value if the bortle scale is given.

    Uses a lookup table to map Bortle scale values to typical NELM values.

    :param bortle: The bortle scale
    :param fst_offset: The offset between the real Nelm and the Nelm for the observer
    :return: The NELM value
    """
    if not isinstance(bortle, int):
        raise ValueError("Bortle must be an integer")
    if not 1 <= bortle <= 9:
        raise ValueError("Bortle must be between 1 and 9")
    if not isinstance(fst_offset, (int, float)):
        raise ValueError("fst_offset must be a number")
    # Lookup dictionary mapping Bortle scale to NELM values
    bortle_nelm_map = {
        1: 6.6,
        2: 6.5,
        3: 6.4,
        4: 6.1,
        5: 5.4,
        6: 4.7,
        7: 4.2,
        8: 3.8,
        9: 3.6
    }
    
    return bortle_nelm_map[bortle] - fst_offset


def bortle_to_sqm(bortle: int) -> float:
    """
    Calculate the SQM value if the bortle scale is given.

    Uses a lookup table to map Bortle scale values to typical NELM values.

    :param bortle: The bortle scale
    :return: The SQM value
    """
    if not isinstance(bortle, int):
        raise ValueError("Bortle must be an integer")
    if not 1 <= bortle <= 9:
        raise ValueError("Bortle must be between 1 and 9")
    # Lookup dictionary mapping Bortle scale to SQM values
    bortle_sqm_map = {
        1: 21.85,
        2: 21.6,
        3: 21.4,
        4: 20.85,
        5: 19.75,
        6: 18.8,
        7: 18.25,
        8: 17.75,
        9: 17.5
    }

    return bortle_sqm_map[bortle]
