import re
from typing import Any

def sanitize_string(value: Any, max_length: int = 256, allow_unicode: bool = False) -> str:
    """
    Sanitize a string input by removing leading/trailing whitespace, dangerous characters,
    and enforcing a maximum length. Optionally restrict to ASCII.

    Args:
        value (Any): The input value to sanitize.
        max_length (int): Maximum allowed length of the string.
        allow_unicode (bool): If False, restricts to ASCII characters.

    Returns:
        str: The sanitized string.

    Raises:
        ValueError: If the input is not a string or exceeds allowed length after sanitization.
    """
    if not isinstance(value, str):
        raise ValueError("Input must be a string")
    value = value.strip()
    if not allow_unicode:
        value = re.sub(r'[^\x20-\x7E]', '', value)  # Remove non-ASCII
    value = re.sub(r'[<>;"\'`\\]', '', value)  # Remove potentially dangerous characters
    if len(value) > max_length:
        raise ValueError(f"Input exceeds maximum length of {max_length}")
    return value