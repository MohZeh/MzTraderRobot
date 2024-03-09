import os

file_path = os.path.abspath(__file__)
# folder_path = os.path.dirname(file_path)
app_directory = os.path.abspath(os.path.join(file_path, os.pardir))
# app_directory = os.path.abspath(os.path.join(file_path, "../.."))
# print(app_directory)

APP_DIRECTORY = app_directory
API_KEY = "X-API-Key"

symbol: str = "SHIBTMN"
tf = "1min"
quantity: str = "1000000"
tick_value: float = 0.0001
add_stop_loss: float = 10 * tick_value  # for SHIB/TMN
allow_pip_sl: float = 20 * tick_value  # for SHIB/TMN
min_reward_to_risk: float = 2
specific_order_id: str = f"MohZeh-{symbol}"
