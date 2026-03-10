from src.analyzer import Analyzer
import pandas as pd
import numpy as np

# Simulation of what app.py does
def test_app_simulation():
    print("Initializing Analyzer...")
    analyzer = Analyzer()
    
    # Create dummy data with indicators
    dates = pd.date_range(start='2020-01-01', periods=100)
    df = pd.DataFrame({
        'Date': dates,
        'Close': np.random.rand(100) * 100,
        'Open': np.random.rand(100) * 100,
        'High': np.random.rand(100) * 100,
        'Low': np.random.rand(100) * 100,
        'Volume': np.random.rand(100) * 1000
    })
    
    # Calling add_indicators
    print("Adding indicators...")
    indicators = analyzer.add_indicators(df)
    
    # Simulating Sidebar Slider Values
    tobo_tol = 0.25
    flag_pole_min = 0.20
    cup_depth = 0.12
    breakout_lookback = 45
    
    print("Applying Config updates (Fix verification)...")
    try:
        # This matches the new code pattern in app.py
        analyzer.config['tobo_tolerance'] = tobo_tol
        analyzer.config['flag_pole_min'] = flag_pole_min
        analyzer.config['cup_min_depth'] = cup_depth
        analyzer.config['trend_lookback'] = breakout_lookback
        
        print(f"Config set: {analyzer.config}")
        
        # Calling detection WITHOUT kwargs (The Fix)
        patterns = analyzer.detect_classic_patterns(indicators)
        print(f"Detection successful. Found {len(patterns)} patterns (on random data).")
        print("SUCCESS: No TypeError raised.")
        
    except TypeError as te:
        print(f"FAILURE: TypeError caught: {te}")
    except Exception as e:
        print(f"FAILURE: Unexpected error: {e}")

if __name__ == "__main__":
    test_app_simulation()

