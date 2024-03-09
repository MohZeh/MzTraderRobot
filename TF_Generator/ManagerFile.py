import pandas as pd
import sys
import os

file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
app_directory = os.path.abspath(os.path.join(folder_path, os.pardir))
# app_directory = os.path.abspath(os.path.join(file_path, "../.."))
# print(app_directory)

sys.path.append(app_directory)
from TF_Generator.OrganizerDataFrame import DataFrameOrg


class FileManager:
    """
    Class for managing OHLCV (Open, High, Low, Close, Volume) DataFrame files, including saving and reading.

    Methods:
        - __init__(data_directory: str, logger=None): Initializes the FileManager instance.
        - _setup_file_manager(): Sets up the FileManager by initializing necessary instances.
        - _save_df_ohlcv(file_name: str, ohlcv_dataframe: pd.DataFrame) -> None: Saves the OHLCV DataFrame to a CSV file.
        - _read_df_ohlcv(file_name: str) -> pd.DataFrame | None: Reads the existing OHLCV DataFrame from a CSV file.
        - __del__(): Destructor, performs cleanup tasks when the instance is deleted.
    """

    def __init__(self, data_directory: str, logger=None):
        """
        Initialize FileManager class.

        Parameters:
            data_directory (str): The directory path where OHLCV DataFrame files will be stored.
            logger: Optional logger instance for logging messages.
        """
        self.data_directory = data_directory
        self.logger = logger

        if self.logger is None:
            pass
        self.logger.logger.warning(f"--- Start : Class {self.__class__.__name__} ---")

        self._setup_file_manager()

    def _setup_file_manager(self):
        """
        Sets up the FileManager by initializing necessary instances.
        """
        # Initialize DataFrame Organizer
        self.df_organizer_instance = DataFrameOrg(logger=self.logger)

    def _save_df_ohlcv(self, file_name: str, ohlcv_dataframe: pd.DataFrame) -> None:
        """
        Saves the OHLCV DataFrame to a CSV file.

        Parameters:
            file_name (str): The name of the file to be saved.
            ohlcv_dataframe (pd.DataFrame): The OHLCV DataFrame to be saved.
        """
        if self.logger:
            self.logger.logger.info("_save_df_ohlcv (function)")

        # Ensure the data directory exists
        os.makedirs(self.data_directory, exist_ok=True)
        # Construct the file path
        file_path = os.path.join(self.data_directory, f"{file_name}.csv")
        # Save the DataFrame to a CSV file
        ohlcv_dataframe.to_csv(file_path)

    def _read_df_ohlcv(self, file_name: str) -> pd.DataFrame | None:
        """
        Reads the existing OHLCV DataFrame from a CSV file.

        Parameters:
            file_name (str): The name of the file to be read.

        Returns:
            pd.DataFrame | None: The read OHLCV DataFrame or None if the file does not exist.
        """
        if self.logger:
            self.logger.logger.info("read_df_ohlcv (function)")

        # Construct the file path
        file_path = os.path.join(self.data_directory, f"{file_name}.csv")

        # Check if the file exists
        if os.path.exists(file_path):
            if self.logger:
                self.logger.logger.info(
                    "The CSV DataFrame file exists and is being read."
                )
            # Read the DataFrame from the CSV file
            existing_ohlcv_df = pd.read_csv(file_path)

            # Index the DataFrame
            existing_ohlcv_df = self.df_organizer_instance._index_dataframe(
                ohlcv_dataframe=existing_ohlcv_df
            )
            if self.logger:
                self.logger.log_debug(
                    f"existing_ohlcv_df: True \n{existing_ohlcv_df}\n"
                )
            return existing_ohlcv_df
        if self.logger:
            self.logger.logger.info("existing_ohlcv_df does not exists (return: None)")
        return

    def __del__(self):
        """
        Destructor, logs a message when the instance is deleted.
        """
        if self.logger:
            self.logger.logger.info(f"Call __del__ (Class : {self.__class__.__name__})")
