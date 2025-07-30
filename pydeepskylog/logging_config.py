# pydeepskylog/logging_config.py
import logging

def configure_logging(level: int = logging.INFO) -> None:
    if not isinstance(level, int):
        raise ValueError("Log level must be an integer from the logging module.")
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True
    )