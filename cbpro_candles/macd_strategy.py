from talib import MACD
#from strategy import Strategy

MACD_HIGH = 0
MACD_LOW = 1

class Trade(object):

    def __init__(self, product_id, ts, price, quantity, value):
        self.product_id = product_id
        self.ts = ts
        self.price = price
        self.quantity = quantity
        self.value = value

class MACDStrategy(object):

    def __init__(self, 
                 fast_period=12,
                 slow_period=26,
                 signal_period=9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.signal = None
        self.trade = None
        self.cash = 10000

    def execute(self, df):

        last_row_idx = len(df)-1

        macd, macd_signal, macd_hist = MACD(df.close, 
                                            fastperiod=self.fast_period,
                                            slowperiod=self.slow_period,
                                            signalperiod=self.signal_period)

        macd_state = MACD_HIGH if macd_hist[last_row_idx] > 0 else MACD_LOW

        if self.signal is None:
            self.signal = macd_state
        elif self.signal != macd_state:
            if macd_state == MACD_HIGH:
                # buy
                if self.trade is None:
                    quantity = self.cash/df.close[last_row_idx]
                    product_id = df.product_id[last_row_idx]
                    ts = df.timestamp[last_row_idx]
                    price = df.close[last_row_idx]
                    trade = Trade(
                        product_id,
                        ts,
                        price,
                        quantity,
                        self.cash)
                    print(f"Bought {quantity} shares of {product_id} at "
                          f"{ts} for {price} a share (for a total of {self.cash})")
                    self.trade = trade
                    self.cash = 0
                else:
                    print("already holding trade")
            elif macd_state == MACD_LOW:
                # sell
                if self.trade is not None:
                    sell_price = df.close[last_row_idx]
                    sell_value = self.trade.quantity*sell_price
                    sell_ts = df.timestamp[last_row_idx]
                    print(f"Sold {self.trade.quantity} shares of {self.trade.product_id} "
                          f"at {sell_ts} for {sell_price} a share (for a total "
                          f"of {sell_value}, profit of "
                          f"{sell_value-self.trade.value}")
                    self.cash = sell_value
                    self.trade = None
                else:
                    print("did not have active trade")
            self.signal = macd_state
    