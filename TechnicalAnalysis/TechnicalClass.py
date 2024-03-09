import pandas as pd
import ta


class TradingStrategy:
    MOD_PRICE = "Typical Price"

    def __init__(self):
        self.reset_signal()

    def reset_signal(self):
        self.signal_1st = None
        self.signal_2st = None
        self.signal_side = None
        self.idx_signal_1st = None
        self.idx_signal_side = None
        self.data_signal = None

    def setupTradingStrategy(self, idx, data):
        self.data = data
        self.idx = idx
        self.add_prices_data()
        self.add_indicators_data()
        self.define_variables(idx=self.idx)
        self.get_signal()

    def add_prices_data(self):
        data_high = self.data["High"]
        data_low = self.data["Low"]
        data_close = self.data["Close"]
        self.data["Median Price"] = (data_high + data_low) / 2
        self.data["Typical Price"] = (data_high + data_low + data_close) / 3
        self.data["Weighted Price"] = (data_high + data_low + 2 * data_close) / 4

    def add_indicators_data(self):
        self.data["rsi"] = self.rsi_indicator_data(mod_price=self.MOD_PRICE)
        self.data["bb_high"] = self.bollinger_indicator_data().bollinger_hband()
        self.data["bb_low"] = self.bollinger_indicator_data().bollinger_lband()
        self.data["bb_mavg"] = self.bollinger_indicator_data().bollinger_mavg()

    def define_variables(self, idx):
        self.high_price = self.data.iloc[idx].High
        self.low_price = self.data.iloc[idx].Low
        self.close_price = self.data.iloc[idx].Close
        self.open_price = self.data.iloc[idx].Open

        self.rsi_value = self.get_rsi_value(idx)
        self.bb_high_price = self.get_bb_high_price(idx)
        self.bb_low_price = self.get_bb_low_price(idx)
        self.bb_mavg_price = self.get_bb_mavg_price(idx)

    def get_signal(self):
        self.signal_rsi = self.get_signal_rsi(rsi_value=self.rsi_value)
        self.signal_bollinger = self.get_signal_bollinger(
            open_price=self.open_price,
            close_price=self.close_price,
            bb_low_price=self.bb_low_price,
            bb_mavg_price=self.bb_mavg_price,
            bb_high_price=self.bb_high_price,
        )
        self.signal_candle = self.get_signal_candle(
            open_price=self.open_price,
            close_price=self.close_price,
            bb_low_price=self.bb_low_price,
            bb_high_price=self.bb_high_price,
        )

        self.signal_1st = self.get_signal_1st()
        self.signal_2st = self.get_signal_2st()
        self.signal_side = self.get_signal_side()

    # ------- Functions: Tuning Indicators -------
    def rsi_indicator_data(self, mod_price="Close", period=13):
        return ta.momentum.rsi(close=self.data[mod_price], window=period)

    def bollinger_indicator_data(self, mod_price="Close", period=20, deviations=2):
        return ta.volatility.BollingerBands(
            close=self.data[mod_price], window=period, window_dev=deviations
        )

    def get_rsi_value(self, idx):
        return self.data["rsi"].iloc[idx]

    def get_bb_low_price(self, idx):
        return self.data["bb_low"].iloc[idx]

    def get_bb_high_price(self, idx):
        return self.data["bb_high"].iloc[idx]

    def get_bb_mavg_price(self, idx):
        return self.data["bb_mavg"].iloc[idx]

    # ------- Functions: Get Signal (indicator & candle) -------
    def get_signal_rsi(self, rsi_value, low=30, high=70):
        if rsi_value < low:
            return "buy"
        elif rsi_value > high:
            return "sell"
        else:
            return None

    def get_signal_bollinger(
        self, open_price, close_price, bb_low_price, bb_mavg_price, bb_high_price
    ):
        if open_price > bb_low_price and close_price < bb_low_price:
            return "buy"
        elif open_price < bb_high_price and close_price > bb_high_price:
            return "sell"
        else:
            return None

    def get_signal_candle(self, open_price, close_price, bb_low_price, bb_high_price):
        if close_price > open_price and close_price > bb_low_price:
            return "buy"
        elif close_price < open_price and close_price < bb_high_price:
            return "sell"
        else:
            return None

    # ------- Functions: Get Mixed Signals -------
    def get_signal_1st(self):
        return (
            "BUY"
            if self.signal_rsi == "buy" and self.signal_bollinger == "buy"
            else "SELL"
            if self.signal_rsi == "sell" and self.signal_bollinger == "sell"
            else None
        )

    def get_signal_2st(self):
        return (
            "BUY"
            if self.signal_candle == "Buy"
            else "SELL"
            if self.signal_candle == "Sell"
            else None
        )

    def get_signal_side(self):
        return (
            "BUY"
            if self.signal_1st == "BUY" and self.signal_2st == "BUY"
            else "SELL"
            if self.signal_1st == "SELL" and self.signal_2st == "SELL"
            else None
        )

    def confirm_signal_side(self):
        if self.signal_side == "BUY" and self.high_price >= self.bb_high_price:
            self.reset_signal()

        if self.signal_side == "SELL" and self.low_price <= self.bb_low_price:
            self.reset_signal()

    def get_idx_signal_1st(self, idx):
        if self.idx_signal_1st is None and self.signal_1st is not None:
            self.idx_signal_1st = self.data.index[idx]
            print("signal_1st:", self.signal_1st, "-> Date:", self.idx_signal_1st)

    def get_idx_signal_side(self, idx):
        if idx == -1 and self.idx_signal_side is None and self.signal_side is not None:
            self.idx_signal_side = self.data.index[idx]
            print("signal_side:", signal_side, "-> Date:", self.signal_type)

    def get_data_signal(self, idx):
        self.get_idx_signal_1st(idx=idx)
        self.get_idx_signal_side(idx=idx)
        if self.idx_signal_side is not None:
            self.data_signal = self.data[self.idx_signal_1st : self.idx_signal_side]

    # -------------------------------
    def get_signals_dict(self, idx, data) -> dict:
        self.setupTradingStrategy(idx=idx, data=data)
        print("signal_side :", self.signal_side)
        self.get_data_signal(idx=idx)
        self.confirm_signal_side()
        if self.data_signal is not None:
            signals_dict = {
                "data_signal": self.data_signal,
                "signal_side": self.signal_side,
            }
            return signals_dict


if __name__ == "__main__":
    # Example usage of the TradingStrategy class

    pass
