import yfinance as yf
import concurrent.futures
import pandas as pd

def download_one(ticker):
    print(f"Thread starting: {ticker}")
    df = yf.download(ticker, period='1mo', progress=False)
    
    print(f"\n[{ticker} DEBUG]")
    print(f"Columns: {df.columns.tolist()}")
    
    # Flatten if MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        print(f"Flattened Columns: {df.columns.tolist()}")
    
    # Check if 'Close' is a Series or DataFrame
    close_data = df['Close']
    if hasattr(close_data, 'iloc'):
        # If it's a DataFrame (multiple columns), take the first one or see what it is
        if isinstance(close_data, pd.DataFrame):
            print(f"WARNING: {ticker} 'Close' is a DataFrame! Shape: {close_data.shape}")
            last_price = close_data.iloc[-1, 0] # Take first column
        else:
            last_price = close_data.iloc[-1]
    else:
        last_price = 0.0
        
    rows = len(df)
    print(f"Thread finished: {ticker} -> Price: {last_price}, Rows: {rows}")
    return (ticker, last_price, rows)

tickers = ["THYAO.IS", "AKBNK.IS", "BIMAS.IS"]

print("Starting concurrent yfinance downloads...")
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(download_one, tickers))

print("\n[RESULTS]")
for t, p, r in results:
    try:
        print(f"{t}: {p:.2f} ({r} rows)")
    except:
        print(f"{t}: {p} ({r} rows)")
