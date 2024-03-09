import requests

BASE_URL: str = "https://api.wallex.ir/"


# ----- MarketInfo EndPoints -----
MARKET_EP: dict = {
    "markets": "v1/markets",
    "currencies_stats": "v1/currencies/stats",
    "order_book_symbol": "v1/depth",
    "order_book_all": "v2/depth/all",
    "latest_trades": "v1/trades",
    "market_history": "v1/udf/history",
}


class MarketInfo:
    """
    A class for interacting with the Wallex API to retrieve market-related information.

    Methods:
        get_markets(self): Retrieves a list of available markets.
        get_currencies(self): Retrieves currency statistics.
        get_order_book_symbol(self, symbol: str): Retrieves the order book for a specific symbol.
        get_order_book_all(self, symbol: str): Retrieves the order book for all symbols.
        get_latest_trades(self, symbol: str): Retrieves the latest trades for a specific symbol.
        get_market_history(self, symbol: str, resolution: str, time_from: int, time_to: int): Retrieves market history data for a specific symbol and time range.

    Example:
        api = MarketInfo()
        symbol = "USDTTMN"
        m00_time = int(time.time())
        h01_time = m00_time - (m00_time % (60 * 60))

        # Retrieve a list of available markets
        markets = api.get_markets()
        print("Markets Result:")
        print(markets)

        # Retrieve currency statistics
        currencies = api.get_currencies()
        print("Currencies Result:")
        print(currencies)

        # Retrieve the order book for a specific symbol
        order_book_symbol = api.get_order_book_symbol(symbol)
        print("Order Book for Symbol Result:")
        print(order_book_symbol)

        # Retrieve the order book for all symbols
        order_book_all = api.get_order_book_all(symbol)
        print("Order Book for All Symbols Result:")
        print(order_book_all)

        # Retrieve the latest trades for a specific symbol
        latest_trades = api.get_latest_trades(symbol)
        print("Latest Trades Result:")
        print(latest_trades)

        # Retrieve market history data for a specific symbol and time range
        time_from = h01_time - 60 * 60 * 5
        time_to = h01_time
        market_history = api.get_market_history(symbol, "60", time_from, time_to)
        print("Market History Result:")
        print(market_history)
    """

    def __init__(self, base_url=BASE_URL):
        """
        Initializes a new instance of the MarketInfo class.

        Args:
            base_url (str, optional): The base URL of the Wallex API. Defaults to "https://api.wallex.ir/".
        """
        self.BASE_URL = base_url

    def _make_request(self, endpoint, params=None):
        """
        Sends an HTTP GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to request.
            params (dict, optional): Query parameters to include in the request. Defaults to None.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If a network-related error occurs.
            requests.exceptions.HTTPError: If an HTTP error (4xx or 5xx) occurs.
        """
        try:
            response = requests.get(self.BASE_URL + endpoint, params=params)
            # response.raise_for_status()  # Raises an exception for 4xx and 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"(Request) error: {e}")
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(f"(HTTP) error: {e}")

    def get_markets(self, endpoint=MARKET_EP["markets"]):
        """
        Retrieves a list of available markets.

        Returns:
            dict: A dictionary containing market information.
        """
        return self._make_request(endpoint)

    def get_currencies(self, endpoint=MARKET_EP["currencies_stats"]):
        """
        Retrieves currency statistics.

        Returns:
            dict: A dictionary containing currency statistics.
        """
        return self._make_request(endpoint)

    def get_order_book_symbol(
        self, symbol: str, endpoint=MARKET_EP["order_book_symbol"]
    ):
        """
        Retrieves the order book for a specific symbol.

        Args:
            symbol (str): The symbol for which to retrieve the order book.

        Returns:
            dict: A dictionary containing the order book for the specified symbol.
        """
        params = {"symbol": symbol}
        return self._make_request(endpoint, params=params)

    def get_order_book_all(self, symbol: str, endpoint=MARKET_EP["order_book_all"]):
        """
        Retrieves the order book for all symbols.

        Args:
            symbol (str): The symbol for which to retrieve the order book.

        Returns:
            dict: A dictionary containing the order book for all symbols.
        """
        params = {"symbol": symbol}
        return self._make_request(endpoint, params=params)

    def get_latest_trades(self, symbol: str, endpoint=MARKET_EP["latest_trades"]):
        """
        Retrieves the latest trades for a specific symbol.

        Args:
            symbol (str): The symbol for which to retrieve the latest trades.

        Returns:
            dict: A dictionary containing the latest trades for the specified symbol.
        """
        params = {"symbol": symbol}
        return self._make_request(endpoint, params=params)

    def get_market_history(
        self,
        symbol: str,
        resolution: str,
        time_from: int,
        time_to: int,
        endpoint=MARKET_EP["market_history"],
    ):
        """
        Retrieves market history data for a specific symbol and time range.

        Args:
            symbol (str): The symbol for which to retrieve market history.
            resolution (str): The time interval for data (e.g., "60" for 1-hour intervals).
            time_from (int): The start time for data retrieval (Unix timestamp in seconds).
            time_to (int): The end time for data retrieval (Unix timestamp in seconds).

        Returns:
            dict: A dictionary containing market history data.
        """
        params = {
            "symbol": symbol,
            "resolution": resolution,
            "from": time_from,
            "to": time_to,
        }
        return self._make_request(endpoint, params=params)


if __name__ == "__main__":
    import time

    # Example usage:
    api = MarketInfo()
    symbol = "USDTTMN"
    m00_time = int(time.time())
    h01_time = m00_time - (m00_time % (60 * 60))

    # Retrieve a list of available markets
    markets = api.get_markets()
    print("Markets Result:")
    print(markets)

    # Retrieve currency statistics
    currencies = api.get_currencies()
    print("Currencies Result:")
    print(currencies)

    # Retrieve the order book for a specific symbol
    order_book_symbol = api.get_order_book_symbol(symbol)
    print("Order Book for Symbol Result:")
    print(order_book_symbol)

    # Retrieve the order book for all symbols
    order_book_all = api.get_order_book_all(symbol)
    print("Order Book for All Symbols Result:")
    print(order_book_all)

    # Retrieve the latest trades for a specific symbol
    latest_trades = api.get_latest_trades(symbol)
    print("Latest Trades Result:")
    print(latest_trades)

    # Retrieve market history data for a specific symbol and time range
    time_from = h01_time - 60 * 60 * 5
    time_to = h01_time
    market_history = api.get_market_history(symbol, "60", time_from, time_to)
    print("Market History Result:")
    print(market_history)
