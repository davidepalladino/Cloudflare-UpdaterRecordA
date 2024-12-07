import logging

from enum import Enum


class LogGravity(Enum):
    """
    An enumeration representing different levels of log severity.

    Attributes:
        INFO (int): Represents informational messages with a gravity level of 1.
        WARNING (int): Represents warning messages with a gravity level of 2.
        ERROR (int): Represents error messages with a gravity level of 3.
        CRITICAL (int): Represents critical error messages with a gravity level of 4.
    """
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

def log(message: str, gravity: LogGravity) -> None:
    """
    Logs a message with a specific log level and prints it to the console with a prefix.

    Args:
        message (str): The message to be logged and printed.
        gravity (LogGravity): The severity level of the log. It determines the log level and prefix.

    Log Levels:
        - LogType.INFO: Logs informational messages. Prefix: "INFO".
        - LogType.WARNING: Logs warnings. Prefix: "WARNING".
        - LogType.ERROR: Logs error messages. Prefix: "ERROR".
        - LogType.CRITICAL: Logs critical errors. Prefix: "CRITICAL".

    Prints:
        Logs are printed to the console in the format: "<PREFIX>: <message>".
    """
    if gravity == LogGravity.INFO:
        prefix = "INFO"
        logging.info(message)
    elif gravity == LogGravity.WARNING:
        prefix = "WARNING"
        logging.warning(message)
    elif gravity == LogGravity.ERROR:
        prefix = "ERROR"
        logging.error(message)
    elif gravity == LogGravity.CRITICAL:
        prefix = "CRITICAL"
        logging.critical(message)
    else:
        prefix = "UNKNOWN"

    print("{0}: {1}".format(prefix, message))