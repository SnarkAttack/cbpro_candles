from cbpro import WebsocketClient
from threading import Thread
from .candle import Candle
from .candle_logger import logger
import dateutil.parser

granularities = [60, 300, 900, 3600, 21600, 86400]

class CandleBuilderWebsocketClient(WebsocketClient):
    def __init__(self, database, products=None):
        super().__init__(products=products, channels=["ticker"])
        self.database = database
        self.products = products
        self.candles = {granularity: {} for granularity in granularities}
        self.shutdown = False

    def on_open(self):
        logger.info("CandleBuilderWebsocketClient subscribed")

    # Returns the values needed to replace in the timestamp for hours and minutes
    # As of right now, seconds and milliseconds will always be set to 0
    def get_replace_values(self, ts, granularity):
        if granularity == 60:
            return (ts.hour, ts.minute)
        elif granularity == 300:
            five_min_int = int(ts.minute//5)*5
            return (ts.hour, five_min_int)
        elif granularity == 900:
            fifteen_min_int = int(ts.minute//15)*15
            return (ts.hour, fifteen_min_int)
        elif granularity == 3600:
            return (ts.hour, 0)
        elif granularity == 21600:
            six_hour_int = int(ts.hour//6)*6
            return (six_hour_int, 0)
        elif granularity == 86400:
            return (0, 0)
        else:
            raise ValueError(f"{granularity} is an invalid granularity") 

    def process_ticker_message(self, msg):
        product_id = msg['product_id']
        ts = dateutil.parser.isoparse(msg['time'])
        for granularity in granularities:
            hour_val, min_val = self.get_replace_values(ts, granularity)
            rounded_ts = ts.replace(hour=hour_val, minute=min_val, second=0, microsecond=0)
            if not self.candles[granularity].get(product_id):
                self.candles[granularity][product_id] = Candle(product_id, granularity, rounded_ts, complete=False)
            else:
                candle = self.candles[granularity][product_id]
                if rounded_ts > candle.timestamp:
                    if candle.complete:
                        self.database.add_candle(candle)
                    self.candles[granularity][product_id] = Candle(product_id, granularity, rounded_ts)
            self.candles[granularity][product_id].update_candle(msg['price'], msg['last_size'])

    def on_message(self, msg):
        granularity = 60
        if msg['type'] == 'ticker':
            self.process_ticker_message(msg)

    def on_close(self):
        if self.shutdown:
            logger.info("CandleBuilderWebsocketClient closed")
        else:
            logger.info("CandleBuilderWebsocketClient disconnected, restarting")
            self.client.close()
            self.client.start()

    def get_last_complete_candle(self, product):
        if self.candles.get(product) is None:
            return None
        if len(self.candles[product]) > 1:
            return self.candles[product][-2]
        return None

    def get_current_candle(self, product):
        if self.candles.get(product) is None:
            return None
        if len(self.candles[product]) > 0:
            return self.candles[product][-1]
        return None


class CandleWebsocketManager(Thread):

    def __init__(self, database):
        super().__init__()
        self.database = database

    def initialize_client(self, products=None):
        self.client = CandleBuilderWebsocketClient(
            self.database,
            products=products
        )
        self.client.start()

    def shutdown_client(self):
        self.client.close()
        self.client = None
