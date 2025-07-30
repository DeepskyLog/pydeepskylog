import logging
from typing import Any, Optional, Sequence
from pydeepskylog.exceptions import InvalidParameterError

logger = logging.getLogger(__name__)

def validate_number(value: Any, name: str, allow_none: bool = False) -> None:
    if value is None and allow_none:
        return
    if not isinstance(value, (int, float)):
        logger.error(f"{name} must be a number")
        raise InvalidParameterError(f"{name} must be a number")

def validate_positive(value: Any, name: str, allow_none: bool = False) -> None:
    validate_number(value, name, allow_none)
    if value is None and allow_none:
        return
    if value <= 0:
        logger.error(f"{name} must be positive")
        raise InvalidParameterError(f"{name} must be positive")

def validate_in_range(value: Any, name: str, min_value: float, max_value: float) -> None:
    validate_number(value, name)
    if not (min_value <= value <= max_value):
        logger.error(f"{name} must be between {min_value} and {max_value}")
        raise InvalidParameterError(f"{name} must be between {min_value} and {max_value}")

def validate_sequence(seq: Any, name: str, item_type: type = float) -> None:
    if not isinstance(seq, Sequence):
        logger.error(f"{name} must be a sequence")
        raise InvalidParameterError(f"{name} must be a sequence")
    for item in seq:
        if not isinstance(item, item_type):
            logger.error(f"Each item in {name} must be of type {item_type.__name__}")
            raise InvalidParameterError(f"Each item in {name} must be of type {item_type.__name__}")