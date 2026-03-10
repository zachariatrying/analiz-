import sys
import os
import pandas as pd

# Add local tvDatafeed to path
lib_path = os.path.join(os.getcwd(), "tvdatafeed_lib", "tvdatafeed-main")
sys.path.append(lib_path)

from tvDatafeed import TvDatafeed, Interval

def test_tv():
    print("Initializing TvDatafeed...")
    tv = TvDatafeed()
    
    symbol = "TCELL"
    exchange = "BIST"
    print(f"Fetching {symbol} from {exchange}...")
    
    # get_hist(symbol, exchange, interval, n_bars)
    # Intervals: in_1_minute, in_5_minutes, in_15_minutes, in_1_hour, in_daily, in_weekly, in_monthly
    try:
        df = tv.get_hist(symbol=symbol, exchange=exchange, interval=Interval.in_daily, n_bars=100)
        if df is not None and not df.empty:
            print(f"Success! Fetched {len(df)} rows.")
            print(f"Last Price: {df['close'].iloc[-1]}")
            print(df.tail())
        else:
            print("Failed to fetch data or empty dataframe.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_tv()
