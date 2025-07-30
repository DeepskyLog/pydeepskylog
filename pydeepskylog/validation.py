"""
Validation utilities for the pydeepskylog package.

This module provides helper functions to validate input parameters for various
astronomical calculations and API interfaces. These functions ensure that values
are of the correct type, within valid ranges, and meet specific requirements
(e.g., positivity, sequence type). If validation fails, an InvalidParameterError
is raised with a descriptive message.

Functions:
    - validate_number: Ensure a value is a number (int or float).
    - validate_positive: Ensure a value is a positive number.
    - validate_in_range: Ensure a value falls within a specified range.
    - validate_sequence: Ensure a value is a sequence of a specified type.

All validation errors are logged and raise InvalidParameterError exceptions.
"""
import logging
from typing import Any, Optional, Sequence
from pydeepskylog.exceptions import InvalidParameterError

logger = logging.getLogger(__name__)

def validate_number(value: Any, name: str, allow_none: bool = False) -> None:
    """
    Validate that a value is a number (int or float).

    This function checks whether the provided value is an integer or floating-point number.
    If `allow_none` is True, the function allows the value to be None and returns without error.
    If the value is not a valid number, an InvalidParameterError is raised with a descriptive message.

    Args:
        value (Any): The value to validate.
        name (str): The name of the parameter (used in error messages).
        allow_none (bool, optional): Whether None is accepted as a valid value. Defaults to False.

    Raises:
        InvalidParameterError: If the value is not a number (int or float), or is None when not allowed.

    Example:
        >>> validate_number(5.2, "Magnitude")
        >>> validate_number(None, "Surface brightness", allow_none=True)
    """
    if value is None and allow_none:
        return
    if not isinstance(value, (int, float)):
        logger.error(f"{name} must be a number")
        raise InvalidParameterError(f"{name} must be a number")

def validate_positive(value: Any, name: str, allow_none: bool = False) -> None:
    """
    Validate that a value is a positive number (greater than zero).

    This function checks whether the provided value is a positive integer or floating-point number.
    If `allow_none` is True, the function allows the value to be None and returns without error.
    If the value is not positive, or not a valid number, an InvalidParameterError is raised with a descriptive message.

    Args:
        value (Any): The value to validate.
        name (str): The name of the parameter (used in error messages).
        allow_none (bool, optional): Whether None is accepted as a valid value. Defaults to False.

    Raises:
        InvalidParameterError: If the value is not a positive number, or is None when not allowed.

    Example:
        >>> validate_positive(10, "Telescope diameter")
        >>> validate_positive(None, "Object size", allow_none=True)
    """
    validate_number(value, name, allow_none)
    if value is None and allow_none:
        return
    if value <= 0:
        logger.error(f"{name} must be positive")
        raise InvalidParameterError(f"{name} must be positive")

def validate_in_range(value: Any, name: str, min_value: float, max_value: float) -> None:
    """
    Validate that a value falls within a specified numeric range.

    This function checks whether the provided value is a number (int or float) and
    whether it lies within the inclusive range defined by `min_value` and `max_value`.
    If the value is outside this range or not a valid number, an InvalidParameterError
    is raised with a descriptive message.

    Args:
        value (Any): The value to validate.
        name (str): The name of the parameter (used in error messages).
        min_value (float): The minimum allowed value (inclusive).
        max_value (float): The maximum allowed value (inclusive).

    Raises:
        InvalidParameterError: If the value is not a number or is outside the specified range.

    Example:
        >>> validate_in_range(5.5, "Magnitude", 0, 10)
    """
    validate_number(value, name)
    if not (min_value <= value <= max_value):
        logger.error(f"{name} must be between {min_value} and {max_value}")
        raise InvalidParameterError(f"{name} must be between {min_value} and {max_value}")

def validate_sequence(seq: Any, name: str, item_type: type = float) -> None:
    """
    Validate that a value is a sequence containing items of a specified type.

    This function checks whether the provided value is a sequence (such as a list or tuple)
    and that each item in the sequence is of the specified type (default: float).
    If the value is not a sequence, or any item is not of the required type,
    an InvalidParameterError is raised with a descriptive message.

    Args:
        seq (Any): The value to validate as a sequence.
        name (str): The name of the parameter (used in error messages).
        item_type (type, optional): The expected type of each item in the sequence. Defaults to float.

    Raises:
        InvalidParameterError: If the value is not a sequence or contains items of the wrong type.

    Example:
        >>> validate_sequence([1.0, 2.5, 3.7], "Magnification list")
        >>> validate_sequence((1, 2, 3), "Integer sequence", item_type=int)
    """
    if not isinstance(seq, Sequence):
        logger.error(f"{name} must be a sequence")
        raise InvalidParameterError(f"{name} must be a sequence")
    for item in seq:
        if not isinstance(item, item_type):
            logger.error(f"Each item in {name} must be of type {item_type.__name__}")
            raise InvalidParameterError(f"Each item in {name} must be of type {item_type.__name__}")