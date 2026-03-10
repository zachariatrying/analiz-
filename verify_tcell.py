import yfinance as yf
import pandas as pd
from datetime import datetime

def verify_price(ticker):
    print(f"Fetching {ticker}...")
    try:
        df = yf.download(ticker, period='1mo', interval='1d')
        if df.empty:
            print(f"FAILED: {ticker} returned empty dataframe.")
            return
        
        # Flatten MultiIndex if necessary (yfinance v0.2.40+ style)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        last_date = df.index[-1]
        last_price = df['Close'].iloc[-1]
        
        print(f"\n[VERIFICATION RESULT]")
        print(f"Ticker: {ticker}")
        print(f"Last Date: {last_date}")
        print(f"Last Close Price: {last_price:.2f}")
        
        if 110 < last_price < 130:
            print("✅ PRICE IS CORRECT (Expected ~117 TL)")
        else:
            print("❌ PRICE IS WRONG! (Expected ~117 TL)")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    verify_price("TCELL.IS")

