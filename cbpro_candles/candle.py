from Decimal import Decimal

class Candle(object):
    def __init__(self, product_id, granularity, timestamp, complete=True):
        self.product_id = product_id
        self.granularity = granularity
        self.timestamp = timestamp
        self.complete = complete
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.volume = Decimal(0)

    def update_candle(self, price, volume)
        dec_price = Decimal(price)
        dec_volume = Decimal(volume)
        if self.open is None:
            self.open = dec_price
        if self.high < dec_price:
            self.high = dec_price
        if self.low > dec_price:
            self.low = dec_price
        self.close = dec_price
        self.volume += dec_volume
