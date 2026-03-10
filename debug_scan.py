import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), 'src'))
from data_manager import DataManager
from analyzer import Analyzer

def test_fetch_and_analyze():
    print("Initializing DataManager...")
    dm = DataManager()
    
    ticker = 'THYAO.IS'
    print(f"Fetching data for {ticker}...")
    df = dm.fetch_stock_data(ticker)
    
    if df is None or df.empty:
        print("ERROR: No data fetched!")
        return
    
    print(f"Data fetched: {len(df)} rows.")
    print(df.tail())
    
    print("\nInitializing Analyzer with Relaxed Constraints...")
    analyzer = Analyzer()
    # Ensure config has defaults if not set in init
    analyzer.config['tobo_tolerance'] = 0.25
    
    print("Detecting patterns...")
    patterns = analyzer.detect_classic_patterns(df)
    
    tobo_count = len([p for p in patterns if 'TOBO' in p['name']])
    print(f"\nFound {len(patterns)} total patterns.")
    print(f"Found {tobo_count} TOBO patterns.")
    
    for p in patterns:
        if 'TOBO' in p['name']:
            print(f" - {p['name']} | Date: {p['date_range']} | Status: {p['status']}")
        if 'RSI' in p['name']:
             print(f" - {p['name']} | Signal: {p['signal']}")
             if 'strategy' in p:
                 print(f"   Strategy: {p['strategy']}")

if __name__ == "__main__":
    test_fetch_and_analyze()
