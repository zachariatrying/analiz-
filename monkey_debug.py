import sys
import os
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

def debug_detect_flag(self, df, timeframe="Günlük"):
    patterns = []
    if df is None or len(df) < 20: 
        print("FAIL: df too short")
        return patterns
    
    close = df['Close'].values
    high = df['High'].values
    low = df['Low'].values
    vol = df['Volume'].values if 'Volume' in df.columns else None
    
    curr_idx = len(df) - 1
    lookback = 40
    start_scan = max(0, curr_idx - lookback)
    
    candidates = []
    for i in range(start_scan, curr_idx):
        if i < 2 or i > curr_idx - 2: continue
        if high[i] > high[i-1] and high[i] > high[i+1]: 
            candidates.append(i)
            
    print(f"CANDIDATES: {candidates}")
    
    for pole_top_idx in candidates:
        pole_top_val = high[pole_top_idx]
        print(f"Checking cand {pole_top_idx} val {pole_top_val}")
        
        pole_start_idx = -1
        min_val = pole_top_val
        pole_limit = max(0, pole_top_idx - 20)
        
        for k in range(pole_top_idx, pole_limit, -1):
            if low[k] < min_val:
                min_val = low[k]
                pole_start_idx = k
        
        if pole_start_idx == -1: 
            print(f"  REJECT: No pole start found for {pole_top_idx}")
            continue
            
        pole_start_val = min_val
        pole_height = pole_top_val - pole_start_val
        pole_pct = pole_height / pole_start_val
        pole_duration = pole_top_idx - pole_start_idx
        
        print(f"  POLE: pct {pole_pct:.2f}, dur {pole_duration}")
        if pole_pct < 0.10: 
            print("  REJECT: Pole pct too low")
            continue
        if pole_duration < 2: 
            print("  REJECT: Pole too short")
            continue
            
        flag_slice_lows = low[pole_top_idx+1:curr_idx+1]
        if len(flag_slice_lows) < 2: 
            print(f"  REJECT: Flag too short ({len(flag_slice_lows)})")
            continue
        
        min_flag_low = flag_slice_lows.min()
        retracement = pole_top_val - min_flag_low
        print(f"  FLAG: retracement {retracement:.2f} (max {0.5*pole_height:.2f})")
        if retracement > 0.5 * pole_height: 
            print("  REJECT: Retracement too deep")
            continue
        
        curr_close = close[-1]
        resistance = pole_top_val
        status = "unconfirmed"
        if curr_close > resistance: status = "confirmed"
        
        if status == "unconfirmed":
            dist_pct = (resistance - curr_close) / curr_close
            if dist_pct > 0.05: 
                print(f"  REJECT: Unconfirmed and too far ({dist_pct:.2f})")
                continue
        
        print(f"  STATUS: {status}")
        return [{"name": "Success"}] # Found it
    return []

Analyzer.detect_flag_pattern = debug_detect_flag

def create_flag_data(pole_pct=0.20, retracement=0.30, volume="good"):
    N = 100
    y = np.full(N, 100.0)
    vol = np.full(N, 1000.0)
    dates = pd.date_range(start='2023-01-01', periods=N)
    y[0:50] = 100.0
    pole_top = 100.0 * (1 + pole_pct)
    y[50:60] = np.linspace(100, pole_top, 10)
    pole_height = pole_top - 100
    flag_low = pole_top - (pole_height * retracement)
    y[60:80] = np.linspace(pole_top, flag_low, 20)
    y[80:] = pole_top + 2.0
    df = pd.DataFrame({'Date': dates, 'Close': y, 'Open': y, 'High': y, 'Low': y, 'Volume': vol})
    return df

a = Analyzer()
df = create_flag_data().iloc[:85].copy()
res = a.detect_flag_pattern(df)
print(f"FINAL RESULT: {res}")
