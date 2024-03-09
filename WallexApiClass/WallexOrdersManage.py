import requests
import re

BASE_URL: str = "https://api.wallex.ir/"
CONTENT_TYPE: str = "application/json"


# ----- OrdersManage EndPoints -----
ORDERS_EP: dict = {
    "orders": "v1/account/orders",
    "openOrders": "v1/account/openOrders",
    "last_trades": "v1/account/trades",
}


class OrdersManage:
    """
    A Python client for interacting with the Wallex API to place orders and manage trading.

    Args:
        api_key (str): Your Wallex API key.
        base_url (str, optional): The base URL of the Wallex API. Defaults to "https://api.wallex.ir/".

    Methods:
        set_order(self, symbol: str, type_order: str, side: str, price: str, quantity: str, client_id: str = None) -> dict
            Place an order with the Wallex API.

        get_order(self, clientOrderId: str) -> dict
            Get information about a specific order by its clientOrderId.

        del_order(self, clientOrderId: str) -> dict
            Cancel an order by its clientOrderId.

        get_open_orders(self, symbol: str = None) -> dict
            Get a list of open orders.

        get_last_trades(self, symbol: str = None, side: str = None) -> dict
            Get a list of the last trades.

    Example:
        # Replace with your actual API key
        api_key: str = "Your-API-Key-Here"
        api: OrdersManage = OrdersManage(api_key)

        # Example usage of set_order function
        symbol: str = "USDTTMN"
        type_order: str = "LIMIT"
        side: str = "BUY"
        price: str = "50000"
        quantity: str = "10"
        client_id: str = "mohsen_zehtabchi_00001"

        set_order_result = api.set_order(symbol, type_order, side, price, quantity, client_id)
        print("Set Order Result:")
        print(set_order_result)

        # Example usage of get_order function
        client_order_id_to_get = "mohsen_zehtabchi_00001"
        get_order_result = api.get_order(client_order_id_to_get)
        print("Get Order Result:")
        print(get_order_result)

        # Example usage of del_order function
        client_order_id_to_cancel = "mohsen_zehtabchi_00001"
        cancel_order_result = api.del_order(client_order_id_to_cancel)
        print("Cancel Order Result:")
        print(cancel_order_result)

        # Example usage of get_open_orders function
        open_orders_result = api.get_open_orders(symbol="USDTTMN")
        print("Open Orders Result:")
        print(open_orders_result)

        # Example usage of get_last_trades function
        last_trades_result = api.get_last_trades(symbol="USDTTMN", side="buy")
        print("Last Trades Result:")
        print(last_trades_result)
    """

    def __init__(self, api_key: str, base_url=BASE_URL):
        """
        Initialize the API client with the provided API key.

        Args:
            api_key (str): Your Wallex API key.
            base_url (str, optional): The base URL of the Wallex API. Defaults to "https://api.wallex.ir/".
        """
        self.api_key: str = api_key
        self.BASE_URL = base_url
        self.CONTENT_TYPE = CONTENT_TYPE

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict = None,
        json_payload: dict = None,
    ) -> dict:
        """
        Make an HTTP request to the Wallex API.

        :param endpoint(str): The API endpoint.
        :param method(str): The HTTP method (GET or POST or DELETE).
        :param params(dict): Query parameters (for GET requests).
        :param json_payload(dict): JSON payload (for POST requests).
        :return: (dict) JSON response or an error message.
        """
        url: str = self.BASE_URL + endpoint
        headers: dict = {
            "Content-Type": self.CONTENT_TYPE,
            "x-api-key": self.api_key,
        }
        try:
            response = requests.request(
                method, url, headers=headers, params=params, json=json_payload
            )
            # response.raise_for_status()  ### Raise an error if the response status code is not in the 200s.
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"(Request) error: {e}"}
        except requests.exceptions.HTTPError as e:
            return {"error": f"(HTTP) error: {e}"}

    def _validate_client_id(self, client_id: str) -> bool:
        """
        Validate the client ID string.

        :param client_id(str): The client ID string to validate.
        :return: (bool) True if valid, False otherwise.
        """
        ### Allow letters, numbers, '.', ':', '-' and '_'
        pattern = re.compile(r"^[\w.:-]+$")
        return bool(pattern.match(client_id))

    def set_order(
        self,
        symbol: str,
        type_order: str,
        side: str,
        price: str,
        quantity: str,
        client_id: str = None,
        endpoint=ORDERS_EP["orders"],
    ) -> dict:
        """
        Place an order with the Wallex API.

        :param symbol(str): The trading symbol.
        :param type_order(str): Order type (LIMIT or MARKET).
        :param side(str): Order side (BUY or SELL).
        :param price(str): Order price (for LIMIT orders).
        :param quantity(str): Order quantity.
        :param client_id(str): Unique client identifier (optional).
        :return: (dict) JSON response or an error message.
        """

        payload: dict = {
            "symbol": symbol,
            "type": type_order,
            "side": side,
            "price": price,
            "quantity": quantity,
        }

        if client_id:
            if not self._validate_client_id(client_id):
                return {
                    "error": "Invalid client ID. Only letters, numbers, '.', ':', '-' and '_' are allowed."
                }
            payload["client_id"] = client_id

        return self._make_request(endpoint, method="POST", json_payload=payload)

    def get_order(self, clientOrderId: str, endpoint=ORDERS_EP["orders"]) -> dict:
        """
        Get information about a specific order by its clientOrderId.

        :param clientOrderId(str): The unique client identifier of the order.
        :return: (dict) JSON response or an error message.
        """
        endpoint = f"{endpoint}/{clientOrderId}"
        return self._make_request(endpoint)

    def del_order(self, clientOrderId: str, endpoint=ORDERS_EP["orders"]) -> dict:
        """
        Cancel an order by its clientOrderId.

        :param clientOrderId(str): The unique client identifier of the order to cancel.
        :return: (dict) JSON response or an error message.
        """
        endpoint = f"{endpoint}/{clientOrderId}"
        return self._make_request(endpoint, method="DELETE")

    def get_open_orders(
        self, symbol: str = None, endpoint=ORDERS_EP["openOrders"]
    ) -> dict:
        """
        Get a list of open orders.

        :param symbol(str): The trading symbol (optional).
        :return: (dict) JSON response or an error message.
        """
        params = {"symbol": symbol}
        return self._make_request(endpoint, params=params)

    def get_last_trades(
        self, symbol: str = None, side: str = None, endpoint=ORDERS_EP["last_trades"]
    ) -> dict:
        """
        Get a list of the last trades.

        :param symbol(str): The trading symbol (optional).
        :param side(str): Order side ("buy" or "sell") (optional).
        :return: (dict) JSON response or an error message.
        """
        params = {"symbol": symbol, "side": side}
        return self._make_request(endpoint, params=params)


if __name__ == "__main__":
    import time

    ### Replace with your actual API key
    api_key: str = "Your-API-Key-Here"  # Your-API-Key-Here

    api = OrdersManage(api_key)

    symbol: str = "SHIBTMN"
    type_order: str = "LIMIT"
    side: str = "BUY"
    price: str = "0.3500"
    quantity: str = "350000"
    time_id = str(time.time())
    client_id = f"MohZeh-{type_order}-{side}-Time-{time.time()}"

    ### Example usage of set_order function
    # set_order_result = api.set_order(
    #     symbol, type_order, side, price, quantity, client_id
    # )
    # print("Set Order Result:")
    # print(set_order_result)

    # time.sleep(0.5)
    # print("\n")
    # order = api.get_order(clientOrderId=client_id)
    # print("Set Order Result:")
    # print(order)
    # if order["result"]["side"] != "SELL":
    #     print(order["result"]["side"])
    #     api.del_order(clientOrderId=client_id)

    # print("\n")
    # order = api.get_order(clientOrderId=client_id)
    # print("Set Order Result:")
    # print(order["result"]["status"])

    ### Example usage of get_order function
    # client_order_id_to_get = (
    #     "MohZeh_LIMIT-SHIBTMN-Price:0.3500-Quantity:350000-Time:1708532669.81077"
    # )
    # get_order_result = api.get_order(client_order_id_to_get)
    # print("Get Order Result:")
    # print(get_order_result)

    ### Example usage of del_order function
    # client_order_id_to_cancel = "MohZeh-SHIBTMN-LIMIT-BUY-Time-1710006242.9108443"
    # cancel_order_result = api.del_order(client_order_id_to_cancel)
    # print("Cancel Order Result:")
    # print(cancel_order_result)

    ### Example usage of get_open_orders function
    # open_orders_result = api.get_open_orders(symbol=symbol)
    # print("Open Orders Result:", open_orders_result)
    # len_dic = len(open_orders_result["result"]["orders"])
    # for i in range(len_dic):
    #     client_id_for = open_orders_result["result"]["orders"][i]["clientOrderId"]
    #     side_for = open_orders_result["result"]["orders"][i]["side"]
    #     print("i:", i)
    #     print("client_id_for:", client_id_for)
    #     print("seide_for:", side_for)
    #     if client_id_for.startswith("MohZeh") and side_for != "SELL":
    #         api.del_order(clientOrderId=client_id_for)

    # client_id = open_orders_result["result"]["orders"][0]["clientOrderId"]
    # print("client_id:", client_id)

    ### Example usage of get_last_trades function
    # last_trades_result = api.get_last_trades(symbol=symbol, side="sell")
    # print("Last Trades Result:")
    # print(last_trades_result)
