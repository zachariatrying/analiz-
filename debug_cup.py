import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

def create_cup_data(shape="u", handle_slope="down"):
    N = 300
    y = np.full(N, 100.0)
    vol = np.full(N, 1000.0)
    
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
        'Close': y, 'Open': y, 'High': y, 'Low': y, 'Volume': vol
    })
    return df

analyzer = Analyzer()
analyzer.config['enabled_patterns'] = {'cup': True}
df = create_cup_data(handle_slope="up")

zz = analyzer.calculate_zigzag(df)
print("ZigZag Points:")
for p in zz:
    print(p)

patterns = analyzer.detect_cup_zigzag(df, zz)
print("\nPatterns Found:")
for p in patterns:
    print(p)

