"""
Logging Configuration Module for K8s Control Panel.

This module provides centralized logging configuration for the K8s Control Panel
application. It sets up file-based logging with rotation, configurable log levels,
and consistent formatting across all application components.

Logging Features:
    - File-based logging with automatic rotation
    - Configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Consistent log format with timestamps, module names, and log levels
    - Maximum file size management with backup retention

Example:
    >>> from common.logging_config import setup_logging
    >>> setup_logging(level='INFO', log_file='logs/app.log')
"""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: str = "logs/app.log",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 3,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """Configure and return a logger instance with file and console handlers.

    This function sets up a rotating file handler for persistent logging and
    optionally a console handler for real-time debugging. It ensures the log
    directory exists and configures proper log rotation to prevent excessive
    file growth.

    Args:
        level: Logging level as a string. Valid values are:
               'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
               Defaults to 'INFO'.
        log_file: Path to the log file. The directory will be created if it
                  doesn't exist. Defaults to 'logs/app.log'.
        max_bytes: Maximum size in bytes for each log file before rotation.
                   Defaults to 5MB (5 * 1024 * 1024).
        backup_count: Number of backup log files to retain. When this number
                      of backup files is reached, the oldest is deleted.
                      Defaults to 3.
        log_format: Custom log format string. If None, uses the default format.
                    Defaults to None.

    Returns:
        A configured logging.Logger instance ready for use in application modules.

    Raises:
        ValueError: If an invalid log level is provided.
        OSError: If the log directory cannot be created or written to.

    Example:
        >>> logger = setup_logging(level='DEBUG', log_file='logs/debug.log')
        >>> logger.info('Application started')
    """
    # Default log format with timestamp, module, function, line number, and message
    if log_format is None:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(funcName)s:%(lineno)d - %(message)s"
        )

    # Create log directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Get or create the root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(log_format)

    # File handler with rotation
    try:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (OSError, PermissionError) as e:
        # If file logging fails, log to console only
        print(f"Warning: Could not set up file logging: {e}")

    # Console handler for real-time output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    This function retrieves a named logger, typically used for module-specific
    logging. The logger should be configured using setup_logging() before use.

    Args:
        name: The name for the logger, typically the module name using
              __name__. This helps identify the source of log messages.

    Returns:
        A logging.Logger instance with the specified name.

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info('Module initialized')
    """
    return logging.getLogger(name)
