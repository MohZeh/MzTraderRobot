import pandas as pd
import sys
import os


file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
app_directory = os.path.abspath(os.path.join(folder_path, os.pardir))
# app_directory = os.path.abspath(os.path.join(file_path, "../.."))
# print(app_directory)

sys.path.append(app_directory)
from TF_Generator.ManagerInputs import InputsManager


class TimeFrameOrg:
    """
    Class for organizing and converting OHLCV (Open, High, Low, Close, Volume) DataFrame to a new timeframe.

    Methods:
        - __init__(ohlcv_dataframe: pd.DataFrame = None, new_timeframe: str = None, logger=None): Initializes the TimeFrameOrganizer instance.
        - _calculate_time_unit(ohlcv_dataframe: pd.DataFrame) -> str: Calculates the time unit based on the time difference between consecutive timestamps in the DataFrame.
        - _can_converted(ohlcv_dataframe: pd.DataFrame, new_timeframe: str) -> bool: Checks if conversion is possible between the initial and new timeframes.
        - convert_timeframe(ohlcv_dataframe: pd.DataFrame = None, new_timeframe: str = None) -> pd.DataFrame: Converts the OHLCV DataFrame to the desired time frame.
        - __del__(): Destructor, logs a message when the instance is deleted.
    """

    def __init__(
        self,
        exchange: str,
        ohlcv_dataframe: pd.DataFrame = None,
        new_timeframe: str = None,
        logger=None,
    ):
        """
        Initialize TimeFrameOrganizer class.

        Parameters:
            ohlcv_dataframe (pd.DataFrame): OHLCV DataFrame with the initial time frame.
            new_timeframe (str): Desired time frame for conversion.
            logger: LoggerManager instance.
        """
        self.exchange = exchange
        self.ohlcv_dataframe = ohlcv_dataframe
        self.new_timeframe = new_timeframe
        self.logger = logger

        # Log class initialization
        if self.logger is not None:
            self.logger.logger.warning(
                f"--- Start : Class {self.__class__.__name__} ---"
            )

    def _calculate_time_unit(self, ohlcv_dataframe: pd.DataFrame) -> str:
        """
        Calculates the time unit based on the time difference between consecutive timestamps in the DataFrame.

        Parameters:
            ohlcv_dataframe (pd.DataFrame): DataFrame with timestamps.

        Returns:
            str: Calculated time unit ('min', 'H', or 'D').
        """
        # Extract last 10 rows from the DataFrame
        ohlcv_dataframe = ohlcv_dataframe.iloc[-10:]

        # Default to 'min' if the DataFrame is empty or has insufficient data
        if ohlcv_dataframe.empty or len(ohlcv_dataframe) < 2:
            return "min"

        # Calculate the time difference between consecutive timestamps
        time_diff = ohlcv_dataframe.index.to_series().diff()

        # Convert the time difference to minutes
        time_diff_minutes = time_diff.max().total_seconds() / 60

        time_unit_mapping = {
            time_diff_minutes < 60: "min",
            60 <= time_diff_minutes < (24 * 60): "H",
            time_diff_minutes >= (24 * 60): "D",
        }

        time_unit = time_unit_mapping[True]

        return time_unit

    def _can_converted(self, ohlcv_dataframe: pd.DataFrame, new_timeframe: str) -> bool:
        """
        Checks if conversion is possible between the initial and new timeframes.

        Parameters:
            ohlcv_dataframe (pd.DataFrame): Initial OHLCV DataFrame.
            new_timeframe (str): New timeframe for conversion.

        Returns:
            bool: True if conversion is possible, False otherwise.
        """
        if self.logger is not None:
            self.logger.logger.info("_check_timeframe (function)")

        ### Calculate the time unit of the initial DataFrame
        init_time_unit = self._calculate_time_unit(ohlcv_dataframe=ohlcv_dataframe)

        ### Obtain the time unit of the new timeframe
        new_inputs = InputsManager(
            timeframe=new_timeframe, exchange=self.exchange, logger=self.logger
        )
        new_time_unit = new_inputs._time_unit()

        ### Check if the time units match
        if init_time_unit != new_time_unit:
            if self.logger is not None:
                self.logger.log_error("----- Error: mismatch (time unit) ! ------\n")
            return False

        return True

    def convert_timeframe(
        self, ohlcv_dataframe: pd.DataFrame = None, new_timeframe: str = None
    ) -> pd.DataFrame:
        """
        Converts the OHLCV DataFrame to the desired time frame.

        Parameters:
            ohlcv_dataframe (pd.DataFrame): OHLCV dataframe with the initial time frame.
            new_timeframe (str): Desired time frame for conversion.

        Returns:
            pd.DataFrame: OHLCV dataframe with aggregated data for the desired time frame.
        """
        ### Check if the provided DataFrame and timeframe are None
        if ohlcv_dataframe is None:
            if self.ohlcv_dataframe is None or self.ohlcv_dataframe.empty:
                if self.logger is not None:
                    self.logger.logger.error(
                        "OHLCV dataframe is not provided or initialized."
                    )
                return None
            ohlcv_dataframe = self.ohlcv_dataframe

        if new_timeframe is None:
            if self.new_timeframe is None or self.new_timeframe.empty:
                if self.logger is not None:
                    self.logger.logger.error(
                        "New timeframe is not provided or initialized."
                    )
                return None
            new_timeframe = self.new_timeframe

        ### Check for insufficient data in the OHLCV dataframe
        if len(ohlcv_dataframe) < 2:
            if self.logger is not None:
                self.logger.logger.error("Insufficient data in the OHLCV dataframe.")
            return None

        ### Check if conversion is possible
        if not self._can_converted(
            ohlcv_dataframe=ohlcv_dataframe, new_timeframe=new_timeframe
        ):
            return None

        if self.logger is not None:
            self.logger.logger.info("convert_timeframe (function)")

        # Resample the data to the desired time frame
        converted_dataframe = ohlcv_dataframe.resample(f"{new_timeframe}").agg(
            {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
            }
        )

        # Drop rows with NaN values (introduced by resampling)
        converted_dataframe = converted_dataframe.dropna()

        return converted_dataframe

    def __del__(self):
        """
        Destructor, logs a message when the instance is deleted.
        """
        if self.logger is not None:
            self.logger.logger.info(f"Call __del__ (Class : {self.__class__.__name__})")
