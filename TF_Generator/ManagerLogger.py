import logging
import sys
import os

file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
app_directory = os.path.abspath(os.path.join(folder_path, os.pardir))
# app_directory = os.path.abspath(os.path.join(file_path, "../.."))
# print(app_directory)

APP_DIRECTORY = app_directory


class LoggerManager:
    """
    Class for managing logging operations.

    Attributes:
        log_directory (str): Path to the directory where log files will be stored.
        log_file_name (str): Name of the log file.
        log_file_path (str): Full path to the log file.
        log_level (int): Logging level.

    Methods:
        __init__(log_directory: str = LOG_DIRECTORY,
                 log_file_name: str = LOG_FILE_NAME,
                 log_level: int = logging.DEBUG):
            Initializes the LoggerManager instance.

        _setup_logger():
            Set up the logger with a file handler.

        log_error(message: str):
            Log an error message.

        log_debug(message: str, *args, **kwargs):
            Log a debug message.
    """

    DEFAULT_APP_DIRECTORY = APP_DIRECTORY
    LOG_DIRECTORY = os.path.join(DEFAULT_APP_DIRECTORY, "log_files")
    LOG_FILE_NAME = "CreatorOHLCV.log"

    def __init__(
        self,
        log_directory=LOG_DIRECTORY,
        log_file_name=LOG_FILE_NAME,
        log_level=logging.DEBUG,
    ):
        self.log_directory = log_directory
        self.log_file_name = log_file_name
        self.log_file_path = os.path.join(log_directory, log_file_name)
        self.log_level = log_level

        self._setup_logger()
        """
        Initializes the LoggerManager instance.

        Parameters:
            log_directory (str): Path to the directory where log files will be stored.
            log_file_name (str): Name of the log file.
            log_level (int): Logging level.
        """

    def _setup_logger(self):
        """
        Set up the logger with a file handler.
        """
        os.makedirs(self.log_directory, exist_ok=True)
        self.logger = logging.getLogger(self.log_file_name)
        self.logger.setLevel(self.log_level)
        log_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setFormatter(log_formatter)

        # Clear existing handlers to avoid duplicate logs
        self.logger.handlers.clear()
        self.logger.addHandler(file_handler)

    def log_error(self, message):
        """
        Logs an error message and prints it.

        Parameters:
            message (str): Error message.
        """
        self.logger.error(message)
        print(message)

    def log_debug(self, message, *args, **kwargs):
        """
        Log a debug message.

        Parameters:
            message (str): Debug message.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.logger.debug(message, *args, **kwargs)
