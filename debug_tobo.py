import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

def create_data():
    N = 300
    y = np.full(N, 100.0)
    vol = np.full(N, 1000.0)
    
    # Downtrend
    y[0:100] = np.linspace(140, 100, 100)
    
    # LS
    y[110:130] = np.linspace(100, 90, 20)
    y[130:140] = np.linspace(90, 100, 10)
    
    # Head
    y[140:150] = np.linspace(100, 80, 10)
    y[150:160] = np.linspace(80, 100, 10)
    
    # RS
    y[160:175] = np.linspace(100, 92, 15)
    y[175:190] = np.linspace(92, 100, 15) # Ends at 100
    
    # Breakout
    y[200:] = 105

    df = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=N),
        'Close': y, 'Open': y, 'High': y, 'Low': y, 'Volume': vol
    })
    df['Vol_SMA_20'] = 1000
    return df

analyzer = Analyzer()
df = create_data()
analyzer.config['tobo'] = True # Ensure enabled

# 1. Check ZigZag
zz = analyzer.calculate_zigzag(df, deviation=0.04)
print(f"ZigZag Points Found: {len(zz)}")
for p in zz:
    print(f"Idx: {p['idx']}, Price: {p['price']:.2f}, Type: {p['type']}")

# 2. Check Detection
print("\n--- Detection Trace ---")
patterns = analyzer.detect_tobo_zigzag(df, zz)
print(f"\nPatterns Found: {len(patterns)}")
for p in patterns:
    print(p)

