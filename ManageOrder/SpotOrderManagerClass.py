import os
import sys
import time
from datetime import datetime

file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
app_directory = os.path.abspath(os.path.join(folder_path, os.pardir))
# app_directory = os.path.abspath(os.path.join(file_path, "../.."))
# print(app_directory)

sys.path.append(app_directory)
from WallexApiClass.WallexOrdersManage import OrdersManage


class SpotOrderManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.setupOrderManager()

    def setupOrderManager(self):
        self.orders_api_instance = OrdersManage(api_key=self.api_key)
        self.init_variables()

    def init_variables(self):
        self.symbol = None
        self.open_orders_result = None
        self.len_open_orders = None
        self.order_result = None
        self.open_orders_id = []
        self.client_id = None
        self.order_allowed = False

        self.status_order = False

    def set_order_params(self, order_params):
        self.symbol = order_params["symbol"]
        self.type_order = order_params["type_order"]
        self.side = order_params["side"]
        self.price = order_params["price"]
        self.quantity = order_params["quantity"]
        self.specific_order_id = order_params["specific_order_id"]

    def get_open_orders_result(self):
        self.open_orders_result = self.orders_api_instance.get_open_orders(
            symbol=self.symbol
        )
        # print("open_orders_result:", self.open_orders_result)
        return self.open_orders_result

    def get_open_orders_id(self):
        open_orders_result = self.get_open_orders_result()
        self.len_open_orders = len(open_orders_result["result"]["orders"])

        for i in range(self.len_open_orders):
            self.open_orders_id.append(
                open_orders_result["result"]["orders"][i]["clientOrderId"]
            )

        print("\n")
        # print(f"open_orders_id:", self.open_orders_id)

        return self.open_orders_id

    def get_order_result(self, order_id):
        self.order_result = self.orders_api_instance.get_order(clientOrderId=order_id)
        # print("order_result:", self.order_result)
        return self.order_result

    def set_order(self):
        order = self.orders_api_instance.set_order(
            symbol=self.symbol,
            type_order=self.type_order,
            side=self.side,
            price=self.price,
            quantity=self.quantity,
            client_id=self.client_id,
        )
        # print("\n")
        # print("Order :", order)
        return order

    def delete_order(self, order_id):
        self.orders_api_instance.del_order(clientOrderId=order_id)

    def order_manage(self, order_params):
        self.set_order_params(order_params=order_params)

        for order_id in self.open_orders_id:
            if order_id.startswith(self.specific_order_id):
                print("Delete Order :", self.delete_order(order_id=order_id))
                time.sleep(1)

        self.open_orders_id.clear()
        self.get_open_orders_id()
        self.order_allowed = True
        for order_id in self.open_orders_id:
            if order_id.startswith(self.specific_order_id):
                self.order_allowed = False

        print("\n")
        print("order_allowed:", self.order_allowed)
        # ------------------

        if self.price != None and self.order_allowed == True:
            print("order price 0 :", self.price)
            self.client_id = f"{self.specific_order_id}-{self.type_order}-{self.side}-Time-{time.time()}"

            if self.side == "BUY":
                self.price = float("{:.4f}".format(self.price - self.price * 0.45))
                print("order price 1 :", self.price)
                order = self.set_order()
                if order["result"]["status"] == "NEW":
                    self.status_order = True
                # if order["result"]["status"] == "CANCELED":
                #     self.status_order = False

        return self.status_order


if __name__ == "__main__":
    API_KEY = "X-API-Key"

    symbol: str = "SHIBTMN"
    type_order: str = "LIMIT"
    quantity: str = "400000"
    specific_order_id: str = f"MohZeh-{symbol}"
    order_params = {
        "symbol": symbol,
        "type_order": type_order,
        "side": "BUY",
        "price": 0.5000,
        "quantity": quantity,
        "specific_order_id": specific_order_id,
    }

    ### Example usage of SpotOrderManager Class
    order_manage_instance = SpotOrderManager(api_key=API_KEY)

    ### Example usage of open_orders_id
    orders_id = order_manage_instance.get_open_orders_id()
    for i in orders_id:
        print("\n")
        print("orders_id is :", i)
        order_manage_instance.get_order_result(order_id=i)

    ### Example usage of set_order
    # status_order = order_manage_instance.order_manage(order_params=order_params)
    # print("status_order :", status_order)

    ### Example usage of delete_order
    # from urllib.parse import quote

    # original_clientOrderId = "MohZeh-SHIBTMN-LIMIT-BUY-Time-1710006242.9108443"
    # encoded_string = quote(original_clientOrderId)
    # print("encoded_string:", encoded_string)

    # order_manage_instance.delete_order(order_id=encoded_string),
    # print("Delet OrderID :", encoded_string, "\n")

    ### Example usage of order_result
    # get_order_result = order_manage_instance.get_order_result(order_id=encoded_string)
    # print("get_order_result : ", get_order_result)
