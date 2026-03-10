import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

def create_cup_data(shape="u", handle_slope="down"):
    N = 300
    y = np.full(N, 100.0)
    
    # P1 (Left Lip)
    y[90:100] = 110.0
    
    # Cup Bottom
    y[100:130] = np.linspace(110, 80, 30)
    y[130:170] = 80 # Flat
    y[170:200] = np.linspace(80, 110, 30)
    
    # Handle
    if handle_slope == "up":
        y[200:240] = np.linspace(110, 115, 40)
        
    y[245:] = 115
    
    df = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=N),
        'Close': y, 'Open': y, 'High': y, 'Low': y, 'Volume': np.full(N, 1000)
    })
    return df

analyzer = Analyzer()
df = create_cup_data(handle_slope="up")
zz = analyzer.calculate_zigzag(df)

class Log:
    def write(self, s): open('debug_zz.txt', 'a').write(s)

with open('debug_zz.txt', 'w') as f:
    f.write("ZZ Points:\n")
    for p in zz:
        f.write(f"Idx: {p['idx']}, Price: {p['price']}, Type: {p['type']}\n")

    patterns = analyzer.detect_cup_zigzag(df, zz)
    f.write(f"\nPatterns Found: {len(patterns)}\n")
    for p in patterns:
        f.write(f"Name: {p['name']}, Score: {p['score']}\n")

