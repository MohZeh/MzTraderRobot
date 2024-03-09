import requests


class ExchangeAPI:
    """
    A class for interacting with Exchange APIs to retrieve market history data.
    """

    BASE_URL = {
        "Wallex": "https://api.wallex.ir/",
        "Nobitex": "https://api.nobitex.ir",
        "BingX": "https://open-api.bingx.com",
        "Binance": "https://api.binance.com",
        "Coinbase": "https://api.exchange.coinbase.com",
    }

    PATH_URL = {
        "Wallex": "v1/udf/history",
        "Nobitex": "/market/udf/history",
        "BingX": "/openApi/swap/v3/quote/klines",
        "Binance": "/api/v3/uiKlines",
        "Coinbase": "/products",
    }

    def __init__(self):
        pass

    def make_request(self, url: str, params: dict = None) -> dict:
        """
        Sends an HTTP GET request to the specified endpoint.

        Args:
            url (str): The URL of the API endpoint.
            params (dict, optional): Query parameters to include in the request. Defaults to None.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If a network-related error occurs.
            requests.exceptions.HTTPError: If an HTTP error (4xx or 5xx) occurs.
        """
        try:
            response = requests.get(url, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"(Request) error: {e}")
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(f"(HTTP) error: {e}")


class HistoryOHLCV(ExchangeAPI):
    """
    A class for retrieving market history data from Exchange APIs.
    """

    def __init__(self):
        super().__init__()

    def get_ohlcv_history(
        self, exchange: str, symbol: str, interval: str, startTime: int, endTime: int
    ):
        """
        Retrieves market history data for a specific symbol and time range from the specified exchange API.
        Exchange: "Wallex", "Nobitex", "Binance", "Coinbase", "BingX"

        Args:
            exchange (str): The name of the exchange from which to retrieve data.
            symbol (str): The symbol for which to retrieve market history data.
            interval (str): The time interval for data, specified in minutes for most exchanges.
            startTime (int): The start time for data retrieval (Unix timestamp in seconds).
            endTime (int): The end time for data retrieval (Unix timestamp in seconds).

        Returns:
            dict: A dictionary containing market history data.
        """
        api_url = self.BASE_URL.get(exchange)
        api_path = self.PATH_URL.get(exchange)
        url = f"{api_url}{api_path}"

        match exchange:
            case "Wallex":
                params = {
                    "symbol": symbol,
                    "resolution": interval,
                    "from": startTime,
                    "to": endTime,
                }
            case "Nobitex":
                params = {
                    "symbol": symbol,
                    "resolution": interval,
                    "from": startTime,
                    "to": endTime,
                }
            case "Binance":
                params = {
                    "symbol": symbol,
                    "interval": interval,
                    "limit": "1000",
                    # "startTime": startTime * 1000,
                    # "endTime": endTime * 1000,
                }
            case "Coinbase":
                url = url + f"/{symbol}/candles"
                params = {
                    "granularity": interval,
                    "startTime": startTime * 1,
                    "endTime": endTime * 1,
                }
            case "BingX":
                params = {
                    "symbol": symbol,
                    "interval": interval,
                    "limit": "1440",
                    "startTime": startTime * 1000,
                    "endTime": endTime * 1000,
                }

        ### Send request to the exchange API and return the market history data
        ohlcv_history = self.make_request(url, params=params)
        if bool(ohlcv_history):
            return ohlcv_history
        print("Error to fetch market history!, please check input values.")


if __name__ == "__main__":
    import pandas as pd
    import time

    # Example usage:
    api = HistoryOHLCV()
    time_now = int(time.time())
    time_now = time_now - (time_now % 60)

    ### Retrieve market history data for a specific symbol and time range
    start_time = time_now - 60 * 60 * 15
    end_time = time_now

    ### Exchanges: "Wallex", "Nobitex", "Binance", "Coinbase", "BingX"
    exchange = "BingX"
    symbol = "BTC-USDT"

    ### interval "Wallex": (1=1m), (60=1h, 180=3h, 360=6h, 720=12h), (1D=1d)
    ### interval "Nobitex": (1, 5, 15, 30):min, (60, 180, 240, 360, 720):h, (1D, 2D, 3D):D
    ### interval "Binance": (1m, 3m, 5m, 15m, 30m), (1h, 2h, 4h, 6h), (1d, 3d), (1w), (1M)
    ### interval "Coinbase": (60=1m, 300=5m, 900=15m), (3600=1h, 21600=6h), (86400=1d)
    ### interval "BingX": (1m, 3m, 5m, 15m, 30m), (1h, 2h, 4h, 6h), (1d, 3d), (1w), (1M)
    interval = "1m"

    market_history = api.get_ohlcv_history(
        exchange=exchange,
        symbol=symbol,
        interval=interval,
        startTime=start_time,
        endTime=end_time,
    )
    market_history = pd.DataFrame(market_history)
    print("Market History Result: (", exchange, ")")
    print(market_history)
    # print(pd.DataFrame.from_records(market_history["data"]))
