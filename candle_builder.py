from cbpro_candles.candle_websocket import CandleWebsocketManager
from cbpro_candles.candle import Candle
from cbpro_candles.candle_db import CoinbaseProCandleDatabase

db_file = 'candles.db'

PRODUCTS = sorted([
    "BTC-USD",
    "ETH-USD",
    "LTC-USD",
    "BCH-USD",
    "EOS-USD",
    "DASH-USD",
    "OXT-USD",
    "MKR-USD",
    "XLM-USD",
    "ATOM-USD",
    "XTZ-USD",
    "ETC-USD",
    "OMG-USD",
    "ZEC-USD",
    "LINK-USD",
    "REP-USD",
    "ZRX-USD",
    "ALGO-USD",
    "DAI-USD",
    "KNC-USD",
    "COMP-USD",
    "BAND-USD",
    "NMR-USD",
    "CGLD-USD",
    "UMA-USD",
    "LRC-USD",
    "YFI-USD",
    "UNI-USD",
    "REN-USD",
    "BAL-USD",
    "WBTC-USD",
    "NU-USD",
    "FIL-USD",
    "AAVE-USD",
    "GRT-USD",
    "BNT-USD",
    "SNX-USD"
])

if __name__ == "__main__":
    cbpdb = CoinbaseProCandleDatabase(db_file)
    cbws = CandleWebsocketManager(cbpdb)
    cbws.initialize_client(products=PRODUCTS)