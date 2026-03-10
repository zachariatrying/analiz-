import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

def test_new_features():
    print("Testing Analyzer New Features...")
    analyzer = Analyzer()
    
    # Create Dummy Data (Uptrend with consolidation)
    dates = pd.date_range(start='2023-01-01', periods=100)
    prices = np.linspace(10, 20, 100) + np.random.normal(0, 0.5, 100)
    # Add a rocket move at the end
    prices[-10:] = prices[-10:] * 1.5 
    
    df = pd.DataFrame({
        'Date': dates,
        'Open': prices,
        'High': prices + 0.5,
        'Low': prices - 0.5,
        'Close': prices,
        'Volume': np.random.randint(100, 1000, 100)
    })
    
    # 1. Test Regression Channel
    try:
        print("1. Testing Regression Channel...", end="")
        ch = analyzer.calculate_linear_regression_channel(df)
        if 'middle' in ch and len(ch['middle']) == 100:
            print("OK")
        else:
            print("FAILED (Format mismatch)")
    except Exception as e:
        print(f"FAILED ({e})")
        
    # 2. Test Support/Resistance
    try:
        print("2. Testing Support/Resistance...", end="")
        # Needs date index? No, argrelextrema uses values
        sr = analyzer.detect_support_resistance(df)
        if isinstance(sr, dict) and 'supports' in sr:
            print("OK")
        else:
            print("FAILED")
    except Exception as e:
        print(f"FAILED ({e})")
        
    # 3. Test High Tight Flag
    try:
        print("3. Testing High Tight Flag...", end="")
        # Create a DF suitable for HTF (Rocket)
        p_rocket = np.concatenate([np.linspace(10, 12, 50), np.linspace(12, 25, 20), np.linspace(25, 24, 10)])
        df_rocket = pd.DataFrame({'Close': p_rocket, 'High': p_rocket, 'Low': p_rocket}) # Minimal
        
        patterns = analyzer.detect_high_tight_flag(df_rocket)
        if isinstance(patterns, list):
            print(f"OK (Found {len(patterns)} patterns)")
        else:
            print("FAILED (Type error)")
    except Exception as e:
        print(f"FAILED ({e})")

if __name__ == "__main__":
    test_new_features()

