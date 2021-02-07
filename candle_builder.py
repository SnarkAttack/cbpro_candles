from cbpro_candles.candle_websocket import CandleWebsocketManager
from cbpro_candles.candle import Candle
from cbpro_candles.candle_db import CoinbaseProCandleDatabase
from cbpro_candles.macd_strategy import MACDStrategy
from talib import MACD
from datetime import datetime
import dateutil.parser

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
    df = cbpdb.get_dataframe("ETH-USD", 60, max_count=None)

    strategy = MACDStrategy()

    for i in range(1, len(df)+1):
        df_step = df.head(i)
        strategy.execute(df_step)

    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    hours = mdates.HourLocator()


    macd, macd_signal, macd_hist = MACD(df.close, 
                                    fastperiod=12,
                                    slowperiod=26,
                                    signalperiod=9)

    df.timestamp = [dateutil.parser.parse(ts_str) for ts_str in df.timestamp]

    time_line = list(df.timestamp)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=15))

    fig, axs = plt.subplots(nrows=2, sharex=True)

    axs[0].plot(time_line, df.close, color='black')
    axs[1].plot(time_line, macd, color='blue')
    axs[1].plot(time_line, macd_signal, color='orange')
    plt.gcf().autofmt_xdate()

    plt.savefig('tmp.png')

