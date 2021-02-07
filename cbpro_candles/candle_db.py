import sqlite3
from decimal import Decimal
from .candle import Candle
import pandas as pd
import dateutil.parser
import datetime

def adapt_decimal(d):
    return str(d)

def convert_decimal(s):
    return Decimal(s.decode("utf-8"))

def adapt_iso_datetime(dt):
    return str(dt)

def convert_iso_datetime(s):
    return dateutil.parser.isoparse(s)

class CoinbaseProCandleDatabase(object):

    def __init__(self, db_file):
        self.db_file = db_file
        sqlite3.register_adapter(Decimal, adapt_decimal)
        sqlite3.register_converter("decimal", convert_decimal)
        sqlite3.register_adapter(datetime.datetime, adapt_iso_datetime)
        sqlite3.register_converter("iso_datetime", convert_iso_datetime)
        if not self.candle_table_exists():
            self.create_candle_table()

    def conn(self):
        conn = sqlite3.connect(self.db_file,
                                detect_types=sqlite3.PARSE_DECLTYPES |
                                sqlite3.PARSE_COLNAMES)
        return conn

    def candle_table_exists(self):

        table_exists = False

        conn = self.conn()
        c = conn.cursor()

        c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='candles';''')

        if c.fetchone()[0] == 1:
            table_exists = True

        conn.commit()
        conn.close()

        return table_exists

    def create_candle_table(self):

        conn = self.conn()
        c = conn.cursor()

        c.execute('''CREATE TABLE "candles" (
                    "product_id"	text,
                    "granularity"	integer,
                    "timestamp"	iso_datetime,
                    "open"	decimal,
                    "high"	decimal,
                    "low"	decimal,
                    "close"	decimal,
                    "volume"	decimal,
                    "trade_count"	INTEGER
                )''')

        c.execute('''CREATE UNIQUE INDEX ix_prod_gran_ts ON candles(product_id, granularity, timestamp)''')

        conn.commit()

        conn.close()

    def add_candle(self, candle):

        conn = self.conn()
        c = conn.cursor()

        c.execute('''INSERT INTO candles VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''', (candle.product_id,
                                                                             candle.granularity,
                                                                             candle.timestamp,
                                                                             candle.open,
                                                                             candle.high,
                                                                             candle.low,
                                                                             candle.close,
                                                                             candle.volume,
                                                                             candle.trade_count))

        conn.commit()
        conn.close()

    def get_dataframe(self, product_id_list, granularity, max_count=300):

        conn = self.conn()
        c = conn.cursor()

        dataframes = []

        cols = ['granularity', 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'trade_count']

        for product_id in product_id_list:

            c.execute('''SELECT %s FROM candles where product_id = ? AND granularity = ? ORDER BY timestamp''' % (', '.join(cols),), (product_id, granularity))

            candle_data = c.fetchall()   

            if max_count is not None and len(candle_data) > max_count:
                candle_data = candle_data[-max_count:]

            dataframes.append(pd.DataFrame(candle_data, columns=cols))

        candle_dfs = pd.concat(
            dataframes, 
            axis=1,
            keys=[product_id for product_id in product_id_list]
        )
        
        conn.commit()
        conn.close()

        return candle_dfs



    def get_candles(self, product_id, granularity, max_count=300):

        conn = self.conn()
        c = conn.cursor()

        c.execute('''SELECT * FROM candles where product_id = ? AND granularity = ? ORDER BY timestamp''', (product_id, granularity))

        candle_data = c.fetchall()   

        if max_count is not None and len(candle_data) > max_count:
            candle_data = candle_data[-max_count:]

        candles = [Candle(*list(c)) for c in candle_data]
        
        conn.commit()
        conn.close()

        return candles




