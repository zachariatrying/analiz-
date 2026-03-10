import sys
import os
import pandas as pd

lib_path = os.path.join(os.getcwd(), "tvdatafeed_lib", "tvdatafeed-main")
sys.path.append(lib_path)

from tvDatafeed import TvDatafeed, Interval

def test_leak():
    tv = TvDatafeed()
    tickers = ["THYAO", "AKBNK", "TCELL", "QUAGR"]
    
    for t in tickers:
        print(f"\n--- {t} ---")
        df = tv.get_hist(symbol=t, exchange='BIST', interval=Interval.in_daily, n_bars=1)
        if df is not None:
            print(df)
            print(f"Close: {df['close'].iloc[-1]}")
        else:
            print("FAILED")

if __name__ == "__main__":
    test_leak()
