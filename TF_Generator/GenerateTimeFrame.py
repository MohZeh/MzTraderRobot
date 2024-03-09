import pandas as pd
import logging
import time
import sys
import re
import os

file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
app_directory = os.path.abspath(os.path.join(folder_path, os.pardir))
# app_directory = os.path.abspath(os.path.join(file_path, "../.."))
# print(app_directory)

sys.path.append(app_directory)
from TF_Generator.OrganizerDataFrame import DataFrameOrg
from TF_Generator.OrganizerTimeFrame import TimeFrameOrg
from TF_Generator.ManagerInputs import InputsManager
from TF_Generator.ManagerLogger import LoggerManager
from TF_Generator.HistoryFetch import HistoryOHLCV
from TF_Generator.ManagerTime import TimeManager
from TF_Generator.ManagerFile import FileManager
from datetime import datetime

APP_DIRECTORY = app_directory


class GenerateOHLCV:
    """
    Class for generating OHLCV (Open, High, Low, Close, Volume) data.

    Attributes:
        - symbol (str): Market symbol.
        - timeframe (str): Timeframe for the OHLCV data.
        - exchange (str): Exchange name.
        - num_candles (int): Number of candles to fetch.
        - data_directory (str): Directory path to store the OHLCV DataFrame files.
        - enable_logging (bool): Flag to enable or disable logging.

    Methods:
        - __init__(symbol: str, timeframe: str, exchange: str, num_candles: int, data_directory: str, enable_logging: bool): Initializes the GenerateOHLCV instance.
        - __enter__(): Enter method for context management.
        - __exit__(exc_type, exc_value, traceback): Exit method for context management.
        - __del__(): Destructor, logs a message when the instance is deleted.
        - _fetch_market_history(symbol: str, interval: int, startTime: int, endTime: int) -> pd.DataFrame: Fetches market data from an external API.
        - _create_new_data(start_timestamp: int = None, end_timestamp: int = None) -> pd.DataFrame: Creates new OHLCV data.
        - _update_existing_data(existing_ohlcv_df: pd.DataFrame) -> pd.DataFrame: Updates existing OHLCV data.
        - dataframe_release(existing_ohlcv_df: pd.DataFrame = None) -> pd.DataFrame: Releases OHLCV DataFrame, either by updating or creating new data.
        - timeframe_release(ohlcv_dataframe: pd.DataFrame = None, new_timeframe: str = None) -> pd.DataFrame: Releases OHLCV DataFrame with a specified timeframe.
    """

    DEFAULT_APP_DIRECTORY = APP_DIRECTORY

    def __init__(
        self,
        symbol: str,
        timeframe: str,
        exchange: str,
        num_candles: int,
        data_directory=DEFAULT_APP_DIRECTORY,
        enable_logging=True,
    ):
        """
        Initialize GenerateOHLCV class.

        Parameters:
            - symbol (str): Market symbol.
            - timeframe (str): Timeframe for the OHLCV data.
            - exchange (str): Exchange name.
            - num_candles (int): Number of candles to fetch.
            - data_directory (str): Directory path to store the OHLCV DataFrame files.
            - enable_logging (bool): Flag to enable or disable logging.
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.exchange = exchange
        self.num_candles = num_candles
        self.data_directory = data_directory
        self.enable_logging = enable_logging

        if self.enable_logging:
            self.logger = LoggerManager()
        self.logger.logger.warning(f"--- Start : Class {self.__class__.__name__} ---")

        self._setupCreatorOHLCV()

    def _define_variables(self):
        """
        Initialize or reset instance variables.
        """
        self.dataframe_organizer = None
        self.start_timestamp = None
        self.end_timestamp = None
        self.exit_flag = None
        self.ohlcv_df = None
        self.ohlcv_tf = None
        self.file_name_df = None
        self.file_name_tf = None

    def _define_instance(self):
        """
        Initialize or reset instance variables.
        """
        self.reg_input_values_instance = None
        self.time_manager_instance = None
        self.file_manager_instance = None
        self.df_organizer_instance = None
        self.tf_organizer_instance = None

    def _setup_instance(self):
        self.file_manager_instance = FileManager(
            data_directory=os.path.join(self.data_directory, self.exchange),
            logger=self.logger,
        )
        self.reg_input_values_instance = InputsManager(
            timeframe=self.timeframe,
            exchange=self.exchange,
            num_candles=self.num_candles,
            logger=self.logger,
        )
        self.time_manager_instance = TimeManager(
            timeframe=self.timeframe,
            exchange=self.exchange,
            num_candles=self.num_candles,
            logger=self.logger,
        )
        self.df_organizer_instance = DataFrameOrg(logger=self.logger)
        self.tf_organizer_instance = TimeFrameOrg(
            exchange=self.exchange, logger=self.logger
        )

    def _setupCreatorOHLCV(self):
        self._define_variables()
        self._define_instance()
        self._setup_instance()
        self.time_uint = self.reg_input_values_instance._time_unit()
        self.file_name_df = f"{self.symbol}-1{self.time_uint}_df"
        self.ohlcv_df = self.file_manager_instance._read_df_ohlcv(
            file_name=self.file_name_df
        )

    def __enter__(self):
        """
        Enter method for context management.
        """
        self.logger.logger.info("--- run with (with statement) ---")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit method for context management.
        """
        self.exit_flag = True
        if self.ohlcv_df is not None:
            self.file_manager_instance._save_df_ohlcv(
                file_name=self.file_name_df, ohlcv_dataframe=self.ohlcv_df
            )
            if self.ohlcv_tf is not None:
                self.file_manager_instance._save_df_ohlcv(
                    file_name=self.file_name_tf, ohlcv_dataframe=self.ohlcv_tf
                )
            self.logger.log_debug("File saved & Exit class")
            self.logger.logger.info(
                f"Call __exit__ (Class : {self.__class__.__name__})"
            )

    def __del__(self):
        """
        Destructor, logs a message when the instance is deleted.
        """
        if self.exit_flag is None:
            if self.ohlcv_df is not None:
                self.file_manager_instance._save_df_ohlcv(
                    file_name=self.file_name_df, ohlcv_dataframe=self.ohlcv_df
                )
                if self.ohlcv_tf is not None:
                    self.file_manager_instance._save_df_ohlcv(
                        file_name=self.file_name_tf, ohlcv_dataframe=self.ohlcv_tf
                    )
                self.logger.log_debug("File saved & Exit class")
                self.logger.logger.info(
                    f"Call __del__ (Class : {self.__class__.__name__})"
                )

    def _fetch_market_history(
        self,
        symbol: str,
        interval: int,
        startTime: int,
        endTime: int,
    ) -> pd.DataFrame:
        """
        Fetches market data from Wallex Market Info API.

        Returns:
        - pd.DataFrame: Market data.
        """
        self.logger.logger.info("_fetch_market_history (function)")

        client = HistoryOHLCV()
        try:
            market_history = client.get_ohlcv_history(
                exchange=self.exchange,
                symbol=symbol,
                interval=interval,
                startTime=startTime,
                endTime=endTime,
            )
            self.logger.log_debug(
                f"Market history in DataFrame: \n{pd.DataFrame(market_history)}"
            )
            ohlcv_df = pd.DataFrame(data=market_history)
            if ohlcv_df is not None:
                return ohlcv_df
        except Exception as e:
            self.logger.logger.error(f"Error in make_df_ohlcv: {str(e)}")

    def _create_new_data(
        self, start_timestamp: int = None, end_timestamp: int = None
    ) -> pd.DataFrame:
        """
        Creates new OHLCV data.

        Returns:
        - pd.DataFrame: New OHLCV data.
        """
        self.logger.logger.info("_create_new_data (function)")

        interval = self.reg_input_values_instance._time_interval()
        self.logger.log_debug(f"interval: {interval}")

        if start_timestamp is None:
            start_timestamp = self.time_manager_instance._start_time_new()

        if end_timestamp is None:
            end_timestamp = self.time_manager_instance._end_time_now()

        new_ohlcv_df = self._fetch_market_history(
            symbol=self.symbol,
            interval=interval,
            startTime=start_timestamp,
            endTime=end_timestamp,
        )
        new_ohlcv_df = self.df_organizer_instance._regularize_dataframe(
            exchange=self.exchange, ohlcv_dataframe=new_ohlcv_df
        )
        new_ohlcv_df = self.df_organizer_instance._index_dataframe(
            ohlcv_dataframe=new_ohlcv_df
        )

        self.ohlcv_df = new_ohlcv_df
        return self.ohlcv_df

    def _update_existing_data(self, existing_ohlcv_df: pd.DataFrame) -> pd.DataFrame:
        """
        Updates existing OHLCV data.

        Returns:
        - pd.DataFrame: Updated OHLCV data.
        """
        self.logger.logger.info("_update_existing_data (function)")

        start_timestamp = self.time_manager_instance._start_time_exists(
            existing_ohlcv_df=existing_ohlcv_df
        )
        end_timestamp = self.time_manager_instance._end_time_now()
        seconds_time_unit = self.time_manager_instance._seconds_time_unit()

        new_candles_needed = (end_timestamp - start_timestamp) / seconds_time_unit

        if new_candles_needed > 0:
            new_ohlcv_data = self._create_new_data(
                start_timestamp=start_timestamp, end_timestamp=end_timestamp
            )

            actual_candles = self.reg_input_values_instance._actual_candles()
            concatenated_dataframe = self.df_organizer_instance._concatenate_dataframe(
                existing_ohlcv_df=existing_ohlcv_df,
                new_ohlcv_data=new_ohlcv_data,
                actual_candles=actual_candles,
            )
            self.ohlcv_df = concatenated_dataframe
            return self.ohlcv_df
        else:
            self.logger.log_debug(
                f"ohlcv_dataframe is up to date and does not need to be updated: {datetime.now().isoformat(sep=' ', timespec='seconds')}"
            )
            self.ohlcv_df = existing_ohlcv_df
            return self.ohlcv_df

    def dataframe_release(self, existing_ohlcv_df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Releases OHLCV DataFrame, either by updating or creating new data.

        Parameters:
            - existing_ohlcv_df (pd.DataFrame): Existing OHLCV DataFrame.

        Returns:
            - pd.DataFrame: Released OHLCV DataFrame.
        """
        self.logger.logger.info("dataframe_release (function)")

        if existing_ohlcv_df is None:
            existing_ohlcv_df = self.ohlcv_df

        if isinstance(existing_ohlcv_df, pd.DataFrame):
            # Existing data found, update it
            self._update_existing_data(existing_ohlcv_df=existing_ohlcv_df)
        else:
            # Existing data not found, create it
            self.logger.logger.info("The CSV DataFrame file does not exists.")
            self._create_new_data()

        return self.ohlcv_df

    def timeframe_release(
        self, ohlcv_dataframe: pd.DataFrame = None, new_timeframe: str = None
    ) -> pd.DataFrame:
        """
        Releases OHLCV DataFrame with a specified timeframe.

        Parameters:
            - ohlcv_dataframe (pd.DataFrame): OHLCV DataFrame.
            - new_timeframe (str): New timeframe for the released DataFrame.

        Returns:
            - pd.DataFrame: Released OHLCV DataFrame with the specified timeframe.
        """
        self.logger.logger.info("timeframe_release (function)")

        if ohlcv_dataframe is None:
            ohlcv_dataframe = self.dataframe_release()

        if new_timeframe is None:
            new_timeframe = self.timeframe

        self.ohlcv_tf = self.tf_organizer_instance.convert_timeframe(
            ohlcv_dataframe=ohlcv_dataframe, new_timeframe=new_timeframe
        )

        self.file_name_tf = f"{self.symbol}-{new_timeframe}_tf"

        return self.ohlcv_tf


if __name__ == "__main__":
    symbol_13 = "BTCUSDT"
    exchange1 = "Wallex"
    exchange2 = "Nobitex"
    exchange3 = "Binance"

    symbol_45 = "BTC-USDT"
    exchange4 = "Coinbase"
    exchange5 = "BingX"

    tf = "1min"
    num_candles = 10000
    symbol = symbol_45
    exchange = exchange4

    with GenerateOHLCV(
        symbol=symbol, timeframe=tf, exchange=exchange, num_candles=num_candles
    ) as ohlcv_object:
        x = 2
        for i in range(x):
            print("Exchange:", exchange, "\n")
            print("Number of Cycle: ", i + 1)
            print(ohlcv_object.timeframe_release())

            print("------------ end ------------\n")
            if i + 1 < x:
                time.sleep(5)

    # ohlcv_object = GenerateOHLCV(symbol=symbol, timeframe=tf, num_candles=num_candles)
    # x = 3
    # for i in range(x):
    #     print("Number of Cycle: ", i + 1)
    #     ohlcv_object.dataframe_release()
    #     print(ohlcv_object.timeframe_release())
    #     print(ohlcv_object.timeframe_release(new_timeframe="15min"))
    #     print("------------ end ------------\n")
    #     if i + 1 < x:
    #         time.sleep(5)
