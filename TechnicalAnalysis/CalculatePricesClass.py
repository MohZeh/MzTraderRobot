class CalculatePrices:
    def __init__(self, allow_pip_sl, add_to_stop_loss, min_reward_to_risk):
        self.allow_pip_sl = allow_pip_sl
        self.add_to_stop_loss = add_to_stop_loss
        self.min_reward_to_risk = min_reward_to_risk

        self.reset_prices()

    def reset_prices(self):
        self.order_price = None
        self.stop_loss_price = None
        self.take_profit_price = None

    def setupCalculatePrices(self, idx, data_signal, signal_side):
        self.idx = idx
        self.data_signal = data_signal
        self.signal_side = signal_side

        self.define_variables(idx=self.idx)
        self.set_prices()

    def define_variables(self, idx):
        self.last_price_close = self.data_signal.iloc[idx].Close
        print("last Price Close:", self.last_price_close)

    def set_prices(self):
        self.order_price = self.set_order_price()
        self.stop_loss_price = self.set_stop_loss_price()
        self.take_profit_price = self.set_take_profit_price()

    # ------- Functions: Stop/Loss & Take/Profit -------
    def set_stop_loss_price(self):
        if self.signal_side == "BUY":  # (Buy Position)
            return self.data_signal["Low"].min() - self.add_stop_loss
        elif self.signal_side == "SELL":  # (Sell Position)
            # print("data_signal[High].max():", data_signal["High"].max())
            return self.data_signal["High"].max() + self.add_stop_loss
        return None

    def set_take_profit_price(self):
        if self.signal_side == "BUY":  # (Buy Position)
            return self.data_signal["bb_high"].max()
        elif self.signal_side == "SELL":  # (Sell Position)
            return self.data_signal["bb_low"].min()
        return None

    def set_order_price(self):
        if self.signal_side == "BUY":
            self.order_price = self.stop_loss_price + self.allow_pip_sl
            self.order_price = min(self.order_price, last_price_close)

        elif self.signal_side == "SELL":
            self.order_price = self.stop_loss_price - self.allow_pip_sl
            self.order_price = max(self.order_price, last_price_close)

        print("order_price(0):", self.order_price)

        return self.order_price

    def get_prices_dict(self, idx, signals_dict) -> dict:
        if signals_dict is not None:
            data_signal = signals_dict["data_signal"]
            signal_side = signals_dict["signal_side"]

            self.setupCalculatePrices(
                idx=idx, data_signal=data_signal, signal_side=signal_side
            )

            prices_dict = {
                "order_price": self.order_price,
                "stop_loss_price": self.stop_loss_price,
                "take_profit_price": self.take_profit_price,
            }

            return prices_dict

        # return self.order_price, self.stop_loss_price, self.take_profit_price
