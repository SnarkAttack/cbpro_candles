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

    def on_open(self):
        logger.info("CandleBuilderWebsocketClient subscribed")

    def on_message(self, msg):
        granularity = 60
        if msg['type'] == 'ticker':
            product_id = msg['product_id']
            ts = dateutil.parser.isoparse(msg['time']).replace(second=0, microsecond=0)
            if not self.candles[granularity].get(product_id):
                self.candles[granularity][product_id] = Candle(product_id, granularity, ts, complete=False)
            else:
                candle = self.candles[granularity][product_id]
                if ts > candle.timestamp:
                    if candle.complete:
                        self.database.add_candle(candle)
                    self.candles[granularity][product_id] = Candle(product_id, granularity, ts)
            self.candles[granularity][product_id].update_candle(msg['price'], msg['last_size'])

    def on_close(self):
        logger.info("CandleBuilderWebsocketClient closed")

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
