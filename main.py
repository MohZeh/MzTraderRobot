import time

from TF_Generator.GenerateTimeFrame import GenerateOHLCV
from ManageTimeIdx.TimeIdxClass import TimeAndIdxManage
from TechnicalAnalysis.TechnicalClass import TradingStrategy
from TechnicalAnalysis.CalculatePricesClass import CalculatePrices
from ManageOrder.SpotOrderManagerClass import SpotOrderManager

# -------   Initialize Variables   -------
import var

num_candles: int = 400
type_order: str = "LIMIT"

idx: int = 0
side: str = None
last_date: str = None

order_price = None
stop_loss_price = None
take_profit_price = None

status_order = False

# -------   Create Instance   -------
time_and_idx_instance = TimeAndIdxManage()
trading_strategy_instance = TradingStrategy()
calculate_prices_instance = CalculatePrices(
    allow_pip_sl=var.allow_pip_sl,
    add_to_stop_loss=var.add_stop_loss,
    min_reward_to_risk=var.min_reward_to_risk,
)
order_manage_instance = SpotOrderManager(api_key=var.API_KEY)

with GenerateOHLCV(
    symbol=var.symbol, timeframe=var.tf, exchange="Wallex", num_candles=num_candles
) as ohlcv_object:
    while True:
        data = ohlcv_object.timeframe_release()

        print("\n***-------***")

        idx = time_and_idx_instance.get_idx(idx=idx, last_date=last_date)
        last_date = data.index[idx]

        signals_dict = trading_strategy_instance.get_signals_dict(idx=idx, data=data)
        print("signals_dict:", signals_dict)
        if signals_dict is not None:
            side = signals_dict["signal_side"]

        prices_dict = calculate_prices_instance.get_prices_dict(
            idx=idx, signals_dict=signals_dict
        )
        print("prices_dict:", prices_dict)
        if prices_dict is not None:
            order_price = prices_dict["order_price"]
            stop_loss_price = stop_loss_price["stop_loss_price"]
            take_profit_price = take_profit_price["take_profit_price"]

        if idx == -1:
            print("Final Signal(Live):", side, "-> Date:", last_date)
            order_params = {
                "symbol": var.symbol,
                "type_order": type_order,
                "side": side,
                "price": order_price,
                "quantity": var.quantity,
                "specific_order_id": var.specific_order_id,
            }
            if order_price != None:
                status_order = order_manage_instance.order_manage(
                    order_params=order_params
                )
            print("status_order :", status_order)

            if status_order == True:
                trading_strategy_instance.reset_signal()
                status_order = False

            sleep_time = time_and_idx_instance.get_sleep_time()
            print("sleep_time_sec:", sleep_time)
            time.sleep(sleep_time)

        if idx != -1:
            print("Final Signal(History):", side, "-> Date:", last_date)
            print("last_time_now:", int(time.time()))
            print("Index and time : Maybe the data is lost!")
            time.sleep(0.2)

        print("***-------***\n")
