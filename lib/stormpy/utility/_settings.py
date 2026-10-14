"""Global settings of Storm, e.g. logging and timeouts."""

from __future__ import annotations

from stormpy import developer
from stormpy.developer import LogLevel


def set_log_level(level: LogLevel) -> None:
    """
    Set the log level of Storm.

    :param level: The new log level, e.g. ``LogLevel.DEBUG``.
    """
    developer.set_log_level(level)


def set_timeout(seconds: int) -> None:
    """
    Set a timeout after which the computations of Storm are aborted.

    :param seconds: Timeout in seconds.
    """
    developer.set_timeout_alarm(seconds)


def reset_timeout() -> None:
    """Reset (i.e., disable) a previously set timeout."""
    developer.reset_timeout_alarm()
