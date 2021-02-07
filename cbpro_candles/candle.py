from decimal import Decimal

class Candle(object):
    def __init__(self, 
                 product_id, 
                 granularity, 
                 timestamp, 
                 open=None,
                 high=None,
                 low=None,
                 close=None,
                 volume=Decimal(0),
                 trade_count=0,
                 complete=True):
        self.product_id = product_id
        self.granularity = granularity
        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.trade_count = trade_count
        self.complete = complete

    def update_candle(self, price, volume):
        dec_price = Decimal(price)
        dec_volume = Decimal(volume)
        if self.open is None:
            self.open = dec_price
        if self.high is None or self.high < dec_price:
            self.high = dec_price
        if self.low is None or self.low > dec_price:
            self.low = dec_price
        self.close = dec_price
        self.volume += dec_volume
        self.trade_count += 1

    def print(self):
        print(f"Candle for {self.product_id} at granularity {self.granularity} and time {self.timestamp}:\n"
                f"\tOpen: {self.open}\n"
                f"\tHigh: {self.high}\n"
                f"\tLow: {self.low}\n"
                f"\tClose: {self.close}\n"
                f"\tVolume: {self.volume}\n"
                f"\tTrade count: {self.trade_count}\n"
        )