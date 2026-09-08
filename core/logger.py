"""
Logging System
=============
Structured logging for JARVIS.
Separate logs for different concerns.
"""

import logging
import os
from datetime import datetime


class JarvisLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
            os.makedirs(self.logs_dir, exist_ok=True)

            self.main_logger = self._create_logger("swaraj", "swaraj.log")
            self.error_logger = self._create_logger("errors", "errors.log")
            self.startup_logger = self._create_logger("startup", "startup.log")
            self.voice_logger = self._create_logger("voice", "voice.log")

    def _create_logger(self, name, filename):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        filepath = os.path.join(self.logs_dir, filename)
        handler = logging.FileHandler(filepath, encoding="utf-8")
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s | %(name)-8s | %(levelname)-7s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logger.addHandler(console)

        return logger

    def info(self, message):
        self.main_logger.info(message)

    def error(self, message):
        self.error_logger.error(message)
        self.main_logger.error(message)

    def warning(self, message):
        self.main_logger.warning(message)

    def debug(self, message):
        self.main_logger.debug(message)

    def startup(self, message):
        self.startup_logger.info(message)

    def voice(self, message):
        self.voice_logger.info(message)

    def log_exception(self, context, exception):
        self.error_logger.error(f"{context}: {type(exception).__name__}: {exception}")


logger = JarvisLogger()
