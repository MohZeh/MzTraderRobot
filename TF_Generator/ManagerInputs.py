import re

### MAX_CANDLE_TIME_UNIT (dict): Maximum number of candles for each time unit.
MAX_CANDLE_TIME_UNIT = {"min": 50000, "H": 15000, "D": 5000}
### ALLOWED_VALUE_RANGES (dict): Allowed numeric value ranges for each time unit.
ALLOWED_VALUE_RANGES = {
    "min": range(1, 60),
    "H": range(1, 24),
    "D": range(1, 7),
    "W": range(1, 4),
    "M": range(1, 12),
}

### INVALID_NUMERIC_VALUE (str): Error message for invalid timeframe format or invalid numeric value.
INVALID_TIMEFRAME_VALUE = (
    "Invalid timeframe format! or numeric value for time unit!\n"
    "It should start with a number and end with one of (min, H, D, W, M).\n"
    "\nMore details:\n"
    "for minute (ex:'1min'), numeric value: range(1, 59), time unit: 'min',\n"
    "for hour (ex:'2H'), numeric value: range(1, 23), time unit: 'H'\n"
    "for Day (ex:'1D'), numeric value: range(1, 6), time unit: 'D'\n"
    "for Week (ex:'3W'), numeric value: range(1, 3), time unit: 'W'\n"
    "for Month (ex:'1M'), numeric value: range(1, 11), time unit: 'M'\n"
)

### ------- WALLEX EXCHANGE -------
### MAPPING_TIME_UNIT_WALLEX (dict): Mapping of raw time units to standardized time units.
MAPPING_TIME_UNIT_WALLEX = {"min": "min", "H": "H", "D": "D", "W": "D", "M": "D"}
### CANDLE_TIME_UNIT_WALLEX (dict): Mapping of time units to number of candles in these time units.
CANDLE_TIME_UNIT_WALLEX = {"min": 1, "H": 1, "D": 1, "W": 7, "M": 31}
### INTERVAL_TIME_UNIT_WALLEX (dict): Mapping of time units to interval strings.
INTERVAL_TIME_UNIT_WALLEX = {"min": "1", "H": "60", "D": "1D", "W": "1D", "M": "1D"}

### ------- BINGX EXCHANGE -------
### MAPPING_TIME_UNIT_BINGX (dict): Mapping of raw time units to standardized time units.
MAPPING_TIME_UNIT_BINGX = {"min": "min", "H": "H", "D": "D", "W": "W", "M": "M"}
### CANDLE_TIME_UNIT_BINGX (dict): Mapping of time units to number of candles in these time units.
CANDLE_TIME_UNIT_BINGX = {"min": 1, "H": 1, "D": 1, "W": 1, "M": 1}
### INTERVAL_TIME_UNIT_BINGX (dict): Mapping of time units to interval strings.
INTERVAL_TIME_UNIT_BINGX = {"min": "1m", "H": "1h", "D": "1d", "W": "1w", "M": "1M"}

### INTERVAL_TIME_UNIT_COINBASE (dict): Mapping of time units to interval strings.
INTERVAL_TIME_UNIT_COINBASE = {
    "min": "60",
    "H": "3600",
    "D": "86400",
    "W": "86400",
    "M": "86400",
}


class InputsManager:
    """
    Class for regularizing input values such as timeframes for different exchanges.

    Methods:
        - __init__(timeframe: str, exchange: str, num_candles: int = None, logger=None): Initializes the InputsManager instance.
        - setup_regularize_inputs_values(): Sets up the InputsManager instance by calling necessary setup methods.
        - _parse_timeframe(timeframe: str) -> None: Parses the input timeframe string to extract numeric value and time unit.
        - _time_unit() -> str: Returns the standardized time unit for the given exchange.
        - _numeric_value() -> int: Returns the numeric value extracted from the timeframe string.
        - _time_interval() -> str: Returns the interval string corresponding to the timeframe.
        - _actual_candles(num_candles: int = None) -> int: Calculates the actual number of candles based on the input timeframe.
    """

    def __init__(
        self,
        timeframe: str,
        exchange: str,
        num_candles: int = None,
        logger=None,
    ):
        """
        Initialize InputsManager class.

        Parameters:
            timeframe (str): Input timeframe string (e.g., '1min', '2H', '1D').
            exchange (str): Name of the exchange for which the input is being regularized.
            num_candles (int): Number of candles (optional).
            logger: LoggerManager instance (optional).
        """
        self.timeframe = timeframe
        self.exchange = exchange
        self.num_candles = num_candles
        self.logger = logger

        if self.logger is None:
            pass
        self.logger.logger.warning(f"--- Start : Class {self.__class__.__name__} ---")

        self.setup_regularize_inputs_values()

    def setup_regularize_inputs_values(self):
        """
        Set up the InputsManager instance by calling necessary setup methods.
        """
        self._init_values()
        self._match_exchange()
        self._parse_timeframe(self.timeframe)

    def _init_values(self):
        self.mapping_time_unit = None
        self.candel_time_unit = None
        self.interval_time_unit = None

    def _match_exchange(self):
        match self.exchange:
            case "Wallex" | "Nobitex":
                self.mapping_time_unit = MAPPING_TIME_UNIT_WALLEX
                self.candel_time_unit = CANDLE_TIME_UNIT_WALLEX
                self.interval_time_unit = INTERVAL_TIME_UNIT_WALLEX
            case "BingX" | "Binance":
                self.mapping_time_unit = MAPPING_TIME_UNIT_BINGX
                self.candel_time_unit = CANDLE_TIME_UNIT_BINGX
                self.interval_time_unit = INTERVAL_TIME_UNIT_BINGX
            case "Coinbase":
                self.interval_time_unit = INTERVAL_TIME_UNIT_COINBASE
                self.mapping_time_unit = MAPPING_TIME_UNIT_WALLEX
                self.candel_time_unit = CANDLE_TIME_UNIT_WALLEX

    def _parse_timeframe(self, timeframe: str) -> None:
        """
        Parse the input timeframe string to extract numeric value and time unit.

        Parameters:
            timeframe (str): Input timeframe string.

        Returns:
            None
        """
        self.logger.logger.info("_parse_timeframe (function)")

        # Define a regular expression pattern to match numeric value and time unit
        pattern = re.compile(r"(\d+)(min|H|D|W|M)")

        # Use regex to extract numeric value and time unit
        match = pattern.match(timeframe)

        if not match:
            self.logger.log_error(INVALID_TIMEFRAME_VALUE)
            exit()

        self.numeric_value, self.raw_unit = int(match.group(1)), match.group(2)

        # Check if the extracted values are within the allowed ranges
        if self.numeric_value not in ALLOWED_VALUE_RANGES.get(self.raw_unit, []):
            self.logger.log_error(INVALID_TIMEFRAME_VALUE)
            exit()

    def _time_unit(self) -> str:
        """
        Get the standardized time unit for the given exchange.

        Returns:
            str: Time unit.
        """
        self.time_unit = self.mapping_time_unit[self.raw_unit]
        return self.time_unit

    def _numeric_value(self) -> int:
        """
        Get the numeric value extracted from the timeframe.

        Returns:
            int: Numeric value.
        """
        return self.numeric_value

    def _time_interval(self) -> str:
        """
        Get the interval string corresponding to the timeframe.

        Returns:
            str: Time interval.
        """

        interval = self.interval_time_unit.get(self.raw_unit, [])
        return interval

    def _actual_candles(self, num_candles: int = None) -> int:
        """
        Calculate the actual number of candles based on the input timeframe.

        Parameters:
            num_candles (int): Number of candles (optional).

        Returns:
            int: Actual number of candles.
        """
        if num_candles is None:
            num_candles = self.num_candles

        if num_candles is None:
            self.logger.log_error(
                "Argument missing, function (_actual_candles) requires argument (num_candles)"
            )
            exit()

        # Calculate the candle coefficient based on the numeric value and coefficient
        candle_coeff = self.numeric_value * self.candel_time_unit.get(self.raw_unit, [])
        return min(num_candles * candle_coeff, MAX_CANDLE_TIME_UNIT[self.time_unit])
