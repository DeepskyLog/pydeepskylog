# pydeepskylog/logging_config.py
import logging

def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure the global logging settings for the pydeepskylog package.

    This function sets up the Python logging system with a standard format, date/time display,
    and the specified log level. It is intended to be called once at application startup to
    ensure consistent logging behavior across the package.

    Args:
        level (int, optional): The logging level to use (e.g., logging.INFO, logging.DEBUG).
            Defaults to logging.INFO.

    Raises:
        ValueError: If the provided log level is not an integer.

    Example:
        >>> from pydeepskylog.logging_config import configure_logging
        >>> configure_logging(logging.DEBUG)
    """
    if not isinstance(level, int):
        raise ValueError("Log level must be an integer from the logging module.")
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True
    )