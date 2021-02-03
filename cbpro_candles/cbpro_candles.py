from cbpro import WebsocketClient
import sqlite3
from decimal import Decimal
from .candle import Candle

def adapt_decimal(d):
    return str(d)

def convert_decimal(s):
    return Decimal(s)


class CoinbaseProCandleDatabase(object):

    def __init__(self, db_file):
        self.db_file = db_file
        sqlite3.register_adapter(Decimal, adapt_decimal)
        sqlite3.register_converted("decimal", convert_decimal)
        if not self.candle_table_exists():
            self.create_candle_table()

    def conn(self):
        conn = sqlite3.connect(self.db_file, 
                                detect_types=sqlite3.PARSE_DECLTYPES |
                                sqlite3.PARSE_COLNAMES)
        return conn

    def candle_table_exists(self, table_name):

        table_exists = False

        conn = self.conn()
        c = conn.cursor()

        c.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='candles';''')

        if c.fetchone()[0] == 1:
            table_exists = True

        conn.commit()
        conn.close()

    def create_candle_table(self):

        conn = self.conn()
        c = conn.cursor()

        c.execute('''CREATE TABLE candles
                    (product_id text, granularity integer, timestamp datetime, open decimal, 
                    high decimal, low decimal, close decimal, volume decimal)'''))

        conn.commit()

        conn.close()

    def add_candle(self, candle):

        conn = self.conn()
        c = conn.cursor()

        c.execute('''INSERT INTO candles VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', (candle.product_id,
                                                                             candle.granularity,
                                                                             candle.timestamp,
                                                                             candle.open,
                                                                             candle.high,
                                                                             candle.low,
                                                                             candle.close,
                                                                             candle.volume))

        conn.commit()
        conn.close()
            


    
