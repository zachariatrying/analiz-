import pandas as pd
import numpy as np
from src.analyzer import Analyzer
from src.data_manager import DataManager

# Setup
manager = DataManager()
analyzer = Analyzer()

# Fetch a major stock usually having moves
ticker = "THYAO.IS" 
print(f"Fetching data for {ticker}...")
df = manager.fetch_stock_data(ticker, interval="1d")

if df is None:
    print("FATAL: No data fetched.")
    exit()

print(f"Data fetched: {len(df)} rows.")

# Manual Config for Testing (Relaxed)
analyzer.config['flag_pole_min'] = 0.05 # 5% check
print("Running Flag Detection...")

# WE need to inspect what's happening INSIDE, so we might need to modify analyzer temporarily 
# or just run it and see the output.
patterns = analyzer.detect_flag_pattern(df)

print(f"Patterns Found: {len(patterns)}")
for p in patterns:
    print(p)

# If empty, let's try to simulate checking constraints manually on the last peak
print("\n--- DIAGNOSTIC ---")
close = df['Close'].values
high = df['High'].values
low = df['Low'].values
curr_idx = len(df) - 1

# Check logic manually
from scipy import signal
peaks = signal.argrelextrema(high, np.greater, order=3)[0]
print(f"Peaks found: {len(peaks)}")

recent_peaks = [p for p in peaks if p > len(df) - 60]
print(f"Recent Peaks (last 60 bars): {recent_peaks}")

for p in recent_peaks:
    # Pole Check
    pole_end_idx = p
    base_val = high[pole_end_idx]
    pole_start_idx = p
    for k in range(p, max(0, p-25), -1):
        if low[k] < base_val:
            base_val = low[k]
            pole_start_idx = k
    
    pole_height = high[pole_end_idx] - base_val
    pole_pct = pole_height / base_val
    pole_width = pole_end_idx - pole_start_idx
    
    avg_return = pole_pct / pole_width if pole_width > 0 else 0
    
    print(f"Peak at {p}: Width={pole_width}, Height%={pole_pct*100:.1f}%, AvgReturn={avg_return*100:.2f}%")
    
    if pole_pct < 0.10: print("  -> REJECT: Pole too small (<10%)")
    elif avg_return < 0.01: print("  -> REJECT: Momentum too low (<1%/bar)")
    else: print("  -> CANDIDATE PASSED POLE CHECK")
