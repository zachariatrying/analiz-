import sys
import os
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

a = Analyzer()
a.config['enabled_patterns'] = {'flag': True}

def create_flag_data(pole_pct=0.20, retracement=0.30, volume="good"):
    N = 100
    y = np.full(N, 100.0)
    vol = np.full(N, 1000.0)
    dates = pd.date_range(start='2023-01-01', periods=N)
    y[0:50] = 100.0
    pole_top = 100.0 * (1 + pole_pct)
    y[50:60] = np.linspace(100, pole_top, 10)
    if volume == "good": vol[50:60] = 5000
    pole_height = pole_top - 100
    flag_low = pole_top - (pole_height * retracement)
    y[60:80] = np.linspace(pole_top, flag_low, 20)
    if volume == "good": vol[60:80] = 500
    y[80:] = pole_top + 2.0
    if volume == "good": vol[80] = 6000
    df = pd.DataFrame({'Date': dates, 'Close': y, 'Open': y, 'High': y, 'Low': y, 'Volume': vol})
    return df

df = create_flag_data().iloc[:85].copy()
res = a.detect_classic_patterns(df)
print(f"PATTERNS: {[p['name'] for p in res]}")
for p in res:
    if 'Flama' in p['name']:
        print(f"SUCCESS: {p}")
