import math
import logging
from pydeepskylog.exceptions import InvalidParameterError
from pydeepskylog.validation import validate_in_range, validate_number

logger: logging = logging.getLogger(__name__)


def nelm_to_sqm(nelm: float, fst_offset:float=0.0) -> float:
    """
    Convert Naked Eye Limiting Magnitude (NELM) to Sky Quality Meter (SQM) value.

    This function estimates the sky brightness (SQM, in magnitudes per square arcsecond) from the limiting magnitude
    visible to the naked eye (NELM), optionally applying an observer-specific offset. The calculation is based on
    established astronomical formulas and is valid for NELM values up to 6.7.

    The formula used is:
        SQM = 21.58 - 5 * log10(10^(1.586 - (NELM + fst_offset)/5) - 1)

    Args:
        nelm (float): Naked Eye Limiting Magnitude (maximum faintness visible to the naked eye).
        fst_offset (float, optional): Observer-specific offset to adjust the NELM value. Defaults to 0.0.

    Returns:
        float: Estimated SQM value (sky brightness in mag/arcsec²), capped at 22.0.

    Raises:
        InvalidParameterError: If input values are out of range or result in invalid calculations.

    Example:
        >>> sqm = nelm_to_sqm(6.2)
        >>> print(sqm)
    """
    validate_number(fst_offset, "fst_offset", allow_none=False)
    validate_number(nelm, "nelm", allow_none=False)
    validate_in_range(nelm + fst_offset, "NELM + fst_offset", 0, 6.7)

    try:
        exponent = 1.586 - (nelm + fst_offset) / 5.0
        base = math.pow(10, exponent) - 1.0
        if base <= 0:
            logger.error("Invalid calculation: log10 argument must be positive")
            raise InvalidParameterError("Invalid calculation: log10 argument must be positive")
        sqm = 21.58 - 5 * math.log10(base)
    except (InvalidParameterError, OverflowError) as e:
        logger.error(f"Error in SQM calculation: {e}")
        raise InvalidParameterError(f"Error in SQM calculation: {e}")
    return min(sqm, 22.0)


def nelm_to_bortle(nelm: float) -> int:
    """
    Convert Naked Eye Limiting Magnitude (NELM) to the Bortle scale value.

    This function maps the limiting magnitude visible to the naked eye (NELM) to the corresponding Bortle scale class,
    which is a qualitative measure of night sky darkness. The mapping uses established threshold values based on
    observational standards and is valid for NELM values up to 6.7.

    Args:
        nelm (float): Naked Eye Limiting Magnitude (maximum faintness visible to the naked eye).

    Returns:
        int: The Bortle scale value (1 to 9), where 1 indicates the darkest skies and 9 the brightest.

    Raises:
        InvalidParameterError: If the NELM value is out of the valid range (0 to 6.7).

    Example:
        >>> bortle = nelm_to_bortle(6.2)
        >>> print(bortle)
    """
    validate_in_range(nelm, "NELM", 0, 6.7)

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
    Convert Sky Quality Meter (SQM) value to the Bortle scale class.

    This function maps the measured sky brightness (SQM, in magnitudes per square arcsecond) to the corresponding
    Bortle scale value, which qualitatively describes night sky darkness. The mapping uses established threshold
    values based on observational standards and is valid for SQM values up to 22.

    Args:
        sqm (float): Sky Quality Meter value (sky brightness in mag/arcsec²).

    Returns:
        int: The Bortle scale value (1 to 9), where 1 indicates the darkest skies and 9 the brightest.

    Raises:
        InvalidParameterError: If the SQM value is out of the valid range (0 to 22).

    Example:
        >>> bortle = sqm_to_bortle(21.0)
        >>> print(bortle)
    """
    validate_in_range(sqm, "SQM", 0, 22)

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
    Convert Sky Quality Meter (SQM) value to Naked Eye Limiting Magnitude (NELM).

    This function estimates the faintest star visible to the naked eye (NELM) from the measured sky brightness (SQM),
    optionally applying an observer-specific offset. The calculation is based on established astronomical formulas
    and is valid for SQM values up to 22.

    The formula used is:
        NELM = 7.93 - 5 * log10(1 + 10^(4.316 - SQM/5))

    Args:
        sqm (float): Sky Quality Meter value (sky brightness in mag/arcsec²).
        fst_offset (float, optional): Observer-specific offset to adjust the NELM value. Defaults to 0.0.

    Returns:
        float: Estimated NELM value (maximum faintness visible to the naked eye).

    Raises:
        InvalidParameterError: If input values are out of range or result in invalid calculations.

    Example:
        >>> nelm = sqm_to_nelm(21.0)
        >>> print(nelm)
    """
    validate_in_range(sqm, "SQM", 0, 22)
    validate_number(fst_offset, "fst_offset", allow_none=False)

    try:
        base = 1 + math.pow(10, 4.316 - sqm / 5.0)
        if base <= 0:
            raise InvalidParameterError("Invalid calculation: log10 argument must be positive")
        nelm = 7.93 - 5 * math.log10(base)
    except (InvalidParameterError, OverflowError) as e:
        logger.error(f"Error in NELM calculation: {e}")
        raise InvalidParameterError(f"Error in NELM calculation: {e}")
    if nelm < 2.5:
        nelm = 2.5
    return nelm - fst_offset


def bortle_to_nelm(bortle: int, fst_offset: float=0.0) -> float:
    """
    Convert Bortle scale value to Naked Eye Limiting Magnitude (NELM).

    This function maps a given Bortle scale class (a qualitative measure of night sky darkness)
    to a typical Naked Eye Limiting Magnitude (NELM) value, optionally applying an observer-specific offset.
    The mapping uses a lookup table based on observational standards.

    Args:
        bortle (int): The Bortle scale value (1 to 9), where 1 indicates the darkest skies and 9 the brightest.
        fst_offset (float, optional): Observer-specific offset to adjust the NELM value. Defaults to 0.0.

    Returns:
        float: Estimated NELM value (maximum faintness visible to the naked eye).

    Raises:
        InvalidParameterError: If the Bortle value is out of the valid range (1 to 9) or if parameters are invalid.

    Example:
        >>> nelm = bortle_to_nelm(4)
        >>> print(nelm)
    """
    validate_in_range(bortle, "Bortle", 1, 9)
    validate_number(fst_offset, "fst_offset", allow_none=False)

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
    Convert Bortle scale value to Sky Quality Meter (SQM) value.

    This function maps a given Bortle scale class (a qualitative measure of night sky darkness)
    to a typical Sky Quality Meter (SQM) value, representing sky brightness in magnitudes per square arcsecond.
    The mapping uses a lookup table based on observational standards.

    Args:
        bortle (int): The Bortle scale value (1 to 9), where 1 indicates the darkest skies and 9 the brightest.

    Returns:
        float: Estimated SQM value (sky brightness in mag/arcsec²).

    Raises:
        InvalidParameterError: If the Bortle value is out of the valid range (1 to 9).

    Example:
        >>> sqm = bortle_to_sqm(4)
        >>> print(sqm)
    """
    validate_in_range(bortle, "bortle", 1, 9)

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
