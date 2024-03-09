from datetime import datetime
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


class TimeManager:
    """
    Class for managing time-related calculations based on the provided timeframe and number of candles.

    Attributes:
        - SECONDS_TIME_UNIT (dict): Mapping of time units to seconds.

    Methods:
        - __init__(timeframe: str, exchange: str, num_candles: int, logger=None): Initializes the TimeManager instance.
        - _setup_time_manager(): Sets up TimeManager using InputsManager.
        - _seconds_time_unit(time_unit: str = None) -> int: Gets the seconds for the specified time unit.
        - _totaltime_seconds(actual_candles: int) -> int: Calculates the total time in seconds.
        - _end_time_now() -> int: Gets the current end time in timestamp and datetime formats.
        - _start_time_new() -> int: Calculates the new start time in timestamp and datetime formats.
        - _start_time_exists(existing_ohlcv_df: pd.DataFrame) -> int: Calculates the existing start time after the last timestamp in the provided DataFrame.
        - _time_exists_info(existing_ohlcv_df: pd.DataFrame) -> Tuple[int, int]: Gets the first and last timestamps from the existing DataFrame.
        ### - __del__(): Destructor, logs a message when the instance is deleted.
    """

    SECONDS_TIME_UNIT = {"min": 60, "H": 3600, "D": 86400}

    def __init__(self, timeframe: str, exchange: str, num_candles: int, logger=None):
        """
        Initialize TimeManager class.

        Parameters:
            timeframe (str): Input timeframe string.
            exchange (str): Name of the exchange for which the input is being standardized.
            num_candles (int): Number of candles.
            logger: LoggerManager instance.
        """
        self.timeframe = timeframe
        self.exchange = exchange
        self.num_candles = num_candles
        self.logger = logger

        if self.logger:
            self.logger.logger.warning(
                f"--- Start : Class {self.__class__.__name__} ---"
            )

        self._setup_time_manager()

    def _setup_time_manager(self):
        """
        Set up TimeManager using InputsManager.
        """
        reg_input_values_instance = InputsManager(
            timeframe=self.timeframe,
            exchange=self.exchange,
            num_candles=self.num_candles,
            logger=self.logger,
        )

        self.time_unit = reg_input_values_instance._time_unit()
        actual_candles = reg_input_values_instance._actual_candles()

        self._seconds_time_unit(time_unit=self.time_unit)
        self._totaltime_seconds(actual_candles=actual_candles)

    def _seconds_time_unit(self, time_unit: str = None) -> int:
        """
        Gets the seconds for the specified time unit.

        Parameters:
            time_unit (str): Time unit.

        Returns:
            int: Seconds for the specified time unit.
        """
        if self.logger:
            self.logger.logger.info("_seconds_time_unit (function)")

        if time_unit is None:
            time_unit = self.time_unit

        self.seconds_time_unit = self.SECONDS_TIME_UNIT[time_unit]
        return self.seconds_time_unit

    def _totaltime_seconds(self, actual_candles: int) -> int:
        """
        Calculates the total time in seconds.

        Parameters:
            actual_candles (int): Actual number of candles.

        Returns:
            int: Total time in seconds.
        """
        if self.logger:
            self.logger.logger.info("_totaltime_seconds (function)")

        self.totaltime_seconds = actual_candles * self.seconds_time_unit

        if self.logger:
            self.logger.log_debug(f"totaltime_seconds: {self.totaltime_seconds}")

        return self.totaltime_seconds

    def _end_time_now(self) -> int:
        """
        Gets the current end time in timestamp and datetime formats.

        Returns:
            int: End time in timestamp format.
        """
        if self.logger:
            self.logger.logger.info("_end_time_now (function)")

        current_timestamp = int(datetime.now().timestamp())

        end_timestamp_now = current_timestamp - (
            current_timestamp % self.seconds_time_unit
        )

        if self.logger:
            self.logger.log_debug(f"_end_time_now (TimeStamp): {end_timestamp_now}")

        end_datetime_now = datetime.fromtimestamp(end_timestamp_now)

        if self.logger:
            self.logger.log_debug(f"_end_time_now (Datetime): {end_datetime_now}")

        return end_timestamp_now

    def _start_time_new(self) -> int:
        """
        Calculates the new start time in timestamp and datetime formats.

        Returns:
            int: New start time in timestamp format.
        """
        if self.logger:
            self.logger.logger.info("_start_time_new (function)")

        end_timestamp_now = self._end_time_now()
        start_timestamp_new = end_timestamp_now - self.totaltime_seconds

        if self.logger:
            self.logger.log_debug(f"_start_time_new (TimeStamp): {start_timestamp_new}")

        start_datetime_new = datetime.fromtimestamp(start_timestamp_new)

        if self.logger:
            self.logger.log_debug(f"_start_time_new (Datetime): {start_datetime_new}")

        candles_start_time_new = int(
            (end_timestamp_now - start_timestamp_new) / self.seconds_time_unit
        )

        if self.logger:
            self.logger.log_debug(
                f"The number of candles to receive for _start_time_new: {candles_start_time_new}"
            )

        return start_timestamp_new

    def _start_time_exists(self, existing_ohlcv_df: pd.DataFrame) -> int:
        """
        Calculates the existing start time after the last timestamp in the provided DataFrame.

        Parameters:
            existing_ohlcv_df (pd.DataFrame): Existing OHLCV DataFrame.

        Returns:
            int: Existing start time in timestamp format.
        """
        if self.logger:
            self.logger.logger.info("_start_time_existing (function)")

        end_timestamp_now = self._end_time_now()
        start_timestamp_new = self._start_time_new()

        first_timestamp_exists, last_timestamp_exists = self._time_exists_info(
            existing_ohlcv_df
        )

        time_difference = int(
            (end_timestamp_now - last_timestamp_exists) / self.seconds_time_unit
        )

        if self.logger:
            self.logger.log_debug(
                f"time_difference : {time_difference} {self.time_unit}"
            )

        if start_timestamp_new + self.seconds_time_unit < first_timestamp_exists:
            return start_timestamp_new
        else:
            start_timestamp_exists = last_timestamp_exists + self.seconds_time_unit

            if self.logger:
                self.logger.log_debug(
                    f"start_timestamp_exists (TimeStamp): {start_timestamp_exists}"
                )

            start_datetime_exists = datetime.fromtimestamp(start_timestamp_exists)

            if self.logger:
                self.logger.log_debug(
                    f"start_timestamp_exists (Datetime): {start_datetime_exists}"
                )

            candle_start_time_exists = int(
                (end_timestamp_now - start_timestamp_exists) / self.seconds_time_unit
            )

            if self.logger:
                self.logger.log_debug(
                    f"The number of candles to be made after the existing candles: {candle_start_time_exists}"
                )

            return start_timestamp_exists

    def _time_exists_info(self, existing_ohlcv_df: pd.DataFrame) -> (int, int):
        """
        Gets the first and last timestamps from the existing DataFrame.

        Parameters:
            existing_ohlcv_df (pd.DataFrame): Existing OHLCV DataFrame.

        Returns:
            Tuple[int, int]: First and last timestamps in timestamp format.
        """
        if self.logger:
            self.logger.logger.info("_time_exists_info (function)")

        first_timestamp_exists = int(
            pd.to_datetime(existing_ohlcv_df.index[0]).timestamp()
        )

        if self.logger:
            self.logger.log_debug(f"FirstTimeExist: {first_timestamp_exists}")

        last_timestamp_exists = int(
            pd.to_datetime(existing_ohlcv_df.index[-1]).timestamp()
        )

        if self.logger:
            self.logger.log_debug(f"LastTimeExist: {last_timestamp_exists}")

        return first_timestamp_exists, last_timestamp_exists

    # def __del__(self):
    #     """
    #     Destructor, logs a message when the instance is deleted.
    #     """
    #     self.logger.logger.info(f"Call __del__ (Class : {self.__class__.__name__})")
