# ------- Functions: Stop/Loss & Take/Profit -------


def get_reward_to_risk(order_price, stop_loss_price, take_profit_price):
    pip_tp = abs(take_profit_price - order_price)
    pip_sl = abs(order_price - stop_loss_price)
    if pip_sl == 0:
        pip_sl = 1000000
    reward_to_risk = pip_tp / pip_sl
    print("reward_to_risk:", reward_to_risk)
    return reward_to_risk


def optimum_order_price(signal_side, order_price, stop_loss_price, take_profit_price):
    # if signal_side == "BUY":
    # if signal_side == "SELL":
    pass
