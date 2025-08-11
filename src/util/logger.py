"""Importing the libraries."""

import logging

"""
This script aims to define a logger with a standard logging message configuration.
Logging messages are employed to track application behavior, errors, and events.
They facilitate debugging, provide insight into program flow, and aid in monitoring and diagnosing issues.
Logging enhances code quality, troubleshooting, and maintenance.
"""


def setup_logger(level="INFO"):
    """Configures the logging system."""

    if level == "INFO":
        logging_level = logging.INFO
    elif level == "DEBUG":
        logging_level = logging.DEBUG
    elif level == "WARNING":
        logging_level = logging.WARNING
    elif level == "ERROR":
        logging_level = logging.ERROR

    # Configure logging settings
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(filename)s]:%(lineno)d - %(message)s",
        level=logging_level,
    )

    # Create a logger instance
    logger = logging.getLogger(__name__)
    return logger


# Example Usage:
# from logger import setup_logger

# logger = setup_logger(level="DEBUG")

# def main():
#     logger.info("Logging system initialized successfully!")
#     logger.error("An error occurred!")
#     logger.warning("A warning message!")
#     logger.debug("Debugging message!")


# if __name__ == "__main__":
#     main()
