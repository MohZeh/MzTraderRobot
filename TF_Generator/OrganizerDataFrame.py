import pandas as pd


class DataFrameOrg:
    """
    Class for organizing and processing OHLCV (Open, High, Low, Close, Volume) DataFrame.

    Methods:
        - __init__(logger=None): Initializes the DataFrameOrg instance.
        - _regularize_dataframe(ohlcv_dataframe: pd.DataFrame) -> pd.DataFrame: Regularizes the OHLCV DataFrame by dropping NaN values, changing column order, and renaming columns.
        - _index_dataframe(ohlcv_dataframe: pd.DataFrame) -> pd.DataFrame: Indexes the OHLCV DataFrame based on the 'TimeStamp' column, converts 'TimeStamp' to Datetime, and sets it as the index.
        - _concatenate_dataframe(existing_ohlcv_df: pd.DataFrame, new_ohlcv_data: pd.DataFrame, actual_candles: int) -> pd.DataFrame: Concatenates existing and new OHLCV DataFrames, drops duplicates, and trims the DataFrame to the specified number of actual candles.
        - __del__(): Destructor, logs a message when the instance is deleted.
    """

    EXCHANGE_FUNCTIONS = {
        "Wallex": "_reg_df_wallex_nobitex",
        "Nobitex": "_reg_df_wallex_nobitex",
        "Binance": "_reg_df_binance",
        "Coinbase": "_reg_df_coinbase",
        "BingX": "_reg_df_bingx",
    }

    def __init__(self, logger=None):
        """
        Initialize DataFrameOrg class.

        Parameters:
            logger: LoggerManager instance.
        """

        self.logger = logger

        self.logger.logger.warning(f"--- Start : Class {self.__class__.__name__} ---")

    def _regularize_dataframe(
        self, exchange: str, ohlcv_dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Regularizes the OHLCV DataFrame based on the specified exchange.

        Parameters:
            exchange (str): The name of the exchange from which the data originates (e.g., "Wallex", "Binance", "Coinbase").
            ohlcv_dataframe (pd.DataFrame): The input OHLCV DataFrame containing columns 't' (timestamp), 'o' (open), 'h' (high), 'l' (low), 'c' (close), and 'v' (volume).

        Returns:
            pd.DataFrame: The regularized OHLCV DataFrame with standardized column names.

        Raises:
            ValueError: If the specified exchange is not supported.
        """
        self.logger.logger.info("_regularize_dataframe (function)")

        if exchange in self.EXCHANGE_FUNCTIONS:
            reg_func = getattr(self, self.EXCHANGE_FUNCTIONS[exchange])
            ohlcv_dataframe = reg_func(ohlcv_dataframe)
        else:
            raise ValueError(f"Exchange '{exchange}' not supported")

        ohlcv_dataframe = ohlcv_dataframe.astype(
            {
                "Open": float,
                "High": float,
                "Low": float,
                "Close": float,
                "Volume": float,
            }
        )
        self.logger.log_debug(f"Regularized ohlcv_dataframe: \n{ohlcv_dataframe}")
        self.logger.log_debug(
            f"Regularized ohlcv_dataframe length: {len(ohlcv_dataframe)}\n"
        )
        return ohlcv_dataframe

    def _reg_df_wallex_nobitex(self, ohlcv_dataframe: pd.DataFrame) -> pd.DataFrame:
        ### Wallex and Nobitex specific logic
        """
        Regularizes the OHLCV DataFrame from Wallex and Nobitex exchanges.

        Parameters:
            ohlcv_dataframe (pd.DataFrame): The input OHLCV DataFrame.

        Returns:
            pd.DataFrame: The regularized OHLCV DataFrame with standardized column names.

        Raises:
            KeyError: If required columns are not found in the input DataFrame.
        """
        try:
            # Drop rows with NaN values & additional column
            ohlcv_dataframe = ohlcv_dataframe.dropna().drop("s", axis=1)

            # change the order of columns
            # ohlcv_dataframe = ohlcv_dataframe[list("tohlcv")]
            ohlcv_dataframe = ohlcv_dataframe[["t", "o", "h", "l", "c", "v"]]
            ohlcv_dataframe = ohlcv_dataframe.rename(
                columns={
                    "t": "TimeStamp",
                    "o": "Open",
                    "h": "High",
                    "l": "Low",
                    "c": "Close",
                    "v": "Volume",
                }
            )
            return ohlcv_dataframe
        except Exception as e:
            self.logger.logger.error(f"regularize_dataframe: {str(e)}")

    def _reg_df_binance(self, ohlcv_dataframe: pd.DataFrame) -> pd.DataFrame:
        ### Binance specific logic
        """
        Regularizes the OHLCV DataFrame from Binance exchange.

        Parameters:
            ohlcv_dataframe (pd.DataFrame): The input OHLCV DataFrame.

        Returns:
            pd.DataFrame: The regularized OHLCV DataFrame with standardized column names and timestamp conversion.

        Raises:
            KeyError: If required columns are not found in the input DataFrame.
        """
        try:
            # change the order of columns
            ohlcv_dataframe = ohlcv_dataframe[ohlcv_dataframe.columns[:6]]
            # ohlcv_dataframe.columns = [
            #     "TimeStamp",
            #     "Open",
            #     "High",
            #     "Low",
            #     "Close",
            #     "Volume",
            # ]

            ohlcv_dataframe = ohlcv_dataframe.rename(
                columns={
                    0: "TimeStamp",
                    1: "Open",
                    2: "High",
                    3: "Low",
                    4: "Close",
                    5: "Volume",
                }
            )
            ohlcv_dataframe["TimeStamp"] = ohlcv_dataframe["TimeStamp"] / 1000
            return ohlcv_dataframe
        except Exception as e:
            self.logger.logger.error(f"regularize_dataframe: {str(e)}")

    def _reg_df_coinbase(self, ohlcv_dataframe: pd.DataFrame) -> pd.DataFrame:
        ### Coinbase specific logic
        """
        Regularizes the OHLCV DataFrame from Coinbase exchange.

        Parameters:
            ohlcv_dataframe (pd.DataFrame): The input OHLCV DataFrame.

        Returns:
            pd.DataFrame: The regularized OHLCV DataFrame with standardized column names.

        Raises:
            KeyError: If required columns are not found in the input DataFrame.
        """
        try:
            # change the order of columns
            ohlcv_dataframe = ohlcv_dataframe[ohlcv_dataframe.columns[:6]]
            ohlcv_dataframe = ohlcv_dataframe.rename(
                columns={
                    0: "TimeStamp",
                    1: "Open",
                    2: "High",
                    3: "Low",
                    4: "Close",
                    5: "Volume",
                }
            )
            return ohlcv_dataframe
        except Exception as e:
            self.logger.logger.error(f"regularize_dataframe: {str(e)}")

    def _reg_df_bingx(self, ohlcv_dataframe: pd.DataFrame) -> pd.DataFrame:
        ### BingX specific logic
        """
        Regularizes the OHLCV DataFrame from BingX exchange.

        Parameters:
            ohlcv_dataframe (pd.DataFrame): The input OHLCV DataFrame.

        Returns:
            pd.DataFrame: The regularized OHLCV DataFrame with standardized column names and timestamp conversion.

        Raises:
            KeyError: If required columns are not found in the input DataFrame.
        """
        try:
            ohlcv_dataframe = pd.DataFrame.from_records(ohlcv_dataframe["data"])

            # change the order of columns
            ohlcv_dataframe = ohlcv_dataframe[
                ["time", "open", "high", "low", "close", "volume"]
            ]
            ohlcv_dataframe = ohlcv_dataframe.rename(
                columns={
                    "time": "TimeStamp",
                    "open": "Open",
                    "high": "High",
                    "low": "Low",
                    "close": "Close",
                    "volume": "Volume",
                }
            )
            ohlcv_dataframe["TimeStamp"] = ohlcv_dataframe["TimeStamp"] / 1000
            return ohlcv_dataframe
        except Exception as e:
            self.logger.logger.error(f"regularize_dataframe: {str(e)}")

    def _index_dataframe(self, ohlcv_dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Indexes the OHLCV DataFrame based on the timestamp column.

        Parameters:
            ohlcv_dataframe (pd.DataFrame): The input OHLCV DataFrame.

        Returns:
            pd.DataFrame: The indexed OHLCV DataFrame with the timestamp converted to datetime and set as the index.
        """
        self.logger.logger.info("_index_dataframe (function)")

        try:
            # Convert TimeStamp to Datetime and set as index
            ohlcv_dataframe["Datetime"] = pd.to_datetime(
                ohlcv_dataframe["TimeStamp"], unit="s", utc=True
            )

            # # Convert the Datetime to local time zone
            # ohlcv_dataframe["Datetime"] = ohlcv_dataframe["Datetime"].dt.tz_localize("UTC")
            # ohlcv_dataframe["Datetime"] = ohlcv_dataframe["Datetime"].dt.tz_convert("Asia/Tehran")

            ohlcv_dataframe = ohlcv_dataframe.set_index("Datetime").sort_index()

            # Convert the index to local time zone
            # ohlcv_dataframe.index = ohlcv_dataframe.index.tz_localize("UTC")
            ohlcv_dataframe.index = ohlcv_dataframe.index.tz_convert("Asia/Tehran")

            self.logger.log_debug(f"ohlcv_dataframe indexed: \n{ohlcv_dataframe}")
            self.logger.log_debug(
                f"Len ohlcv_dataframe indexed: {len(ohlcv_dataframe)}\n"
            )

            return ohlcv_dataframe
        except Exception as e:
            self.logger.logger.error(f"index_dataframe: {str(e)}")

    def _concatenate_dataframe(
        self,
        existing_ohlcv_df: pd.DataFrame,
        new_ohlcv_data: pd.DataFrame,
        actual_candles: int,
    ) -> pd.DataFrame:
        """
        Concatenates existing and new OHLCV DataFrames, drops duplicates, and trims the DataFrame to the specified number of actual candles.

        Parameters:
            existing_ohlcv_df (pd.DataFrame): The existing OHLCV DataFrame.
            new_ohlcv_data (pd.DataFrame): The new OHLCV DataFrame to be concatenated.
            actual_candles (int): The number of actual candles to trim the concatenated DataFrame.

        Returns:
            pd.DataFrame: The concatenated and trimmed OHLCV DataFrame.
        """
        self.logger.logger.info("_concatenate_detaframe_ohlcv (function)")

        # Concatenate dataframes and drop duplicates based on TimeStamp
        concatenated_df = pd.concat([existing_ohlcv_df, new_ohlcv_data])
        concatenated_df.drop_duplicates(subset=["TimeStamp"], keep="last", inplace=True)

        if len(concatenated_df) > actual_candles:
            concatenated_df = concatenated_df.iloc[-actual_candles:].sort_index()

        self.logger.log_debug(
            f"concatenated_dataframe length (fix): {len(concatenated_df)}\n"
        )
        ### Return the concatenated DataFrame regardless of trimming
        return concatenated_df

    def __del__(self):
        """
        Destructor, logs a message when the instance is deleted.
        """
        self.logger.logger.info(f"Call __del__ (Class : {self.__class__.__name__})")
