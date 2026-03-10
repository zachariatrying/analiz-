import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer
from data_manager import DataManager

manager = DataManager()
analyzer = Analyzer()

# Select a few major tickers + newest ones
tickers = ['ASTOR.IS', 'THYAO.IS', 'ASELS.IS', 'UCAYM.IS', 'FRMPL.IS']

print(f"{'Ticker':<12} | {'Pattern Count':<15} | {'Min Bars Check'}")
print("-" * 50)

for t in tickers:
    df = manager.fetch_stock_data(t)
    if df is not None:
        # Check lengths
        l = len(df)
        
        # Test original restrictive logic
        indicators = analyzer.add_indicators(df)
        patterns = analyzer.detect_classic_patterns(indicators)
        
        # Why is it failing?
        msg = "OK"
        if l < 50: msg = f"REJECTED (<50 bars: {l})"
        
        print(f"{t:<12} | {len(patterns):<15} | {msg}")

print("\nRunning full scan on IPO list (First 30)...")
ip_list = manager.get_ipo_list().head(30)
found_any = 0
for t in ip_list['ticker']:
    df = manager.fetch_stock_data(t)
    if df is not None:
        indicators = analyzer.add_indicators(df)
        patterns = analyzer.detect_classic_patterns(indicators)
        if patterns:
            found_any += len(patterns)
            print(f"Found {len(patterns)} patterns in {t}")

print(f"\nTotal patterns found in first 30: {found_any}")
if found_any == 0:
    print("WARNING: Logic is returning zero results. Checking ZigZag...")
    # Check if ZigZag is empty
    df = manager.fetch_stock_data('THYAO.IS') # High liquidity
    dev = 0.04
    zz = analyzer.calculate_zigzag(df, deviation=dev)
    print(f"THYAO ZigZag Points: {len(zz)}")

