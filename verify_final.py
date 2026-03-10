from src.analyzer import Analyzer
import pandas as pd
import numpy as np

def verify_final_features():
    print("Initializing Analyzer...")
    analyzer = Analyzer()
    
    # 1. Create Dummy Data (Daily)
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    df = pd.DataFrame({
        'Date': dates,
        'Open': np.random.rand(100) * 100,
        'High': np.random.rand(100) * 110,
        'Low': np.random.rand(100) * 90,
        'Close': np.linspace(100, 200, 100) + np.random.normal(0, 5, 100), # Uptrend
        'Volume': np.random.rand(100) * 1000
    })
    
    # 2. Test Resampling
    print("Testing Resampling (Weekly)...")
    df_weekly = analyzer.resample_data(df, 'Haftalık')
    if len(df_weekly) < len(df):
        print(f"Resampling SUCCESS: {len(df)} days -> {len(df_weekly)} weeks")
    else:
        print("Resampling FAILED or data too short.")

    # 3. Test Trendlines
    print("Testing Trendline Calculation...")
    trends = analyzer.calculate_trendlines(df)
    if 'uptrend' in trends:
        print(f"Trendlines Calculated: {trends.keys()}")
        if trends['uptrend']:
            print(f"Uptrend Points: {len(trends['uptrend'])}")
    else:
        print("Trendline Calculation FAILED keys missing.")

    # 4. Test Toggles logic (via Config)
    print("Testing Toggles Configuration...")
    analyzer.config['enabled_patterns'] = {'tobo': False, 'flag': False, 'cup': False, 'breakout': False}
    # Should find nothing
    indicators = analyzer.add_indicators(df)
    patterns = analyzer.detect_classic_patterns(indicators)
    if len(patterns) == 0:
        print("Toggles SUCCESS: No patterns found when disabled.")
    else:
        print(f"Toggles FAILED: Found {len(patterns)} patterns.")

if __name__ == "__main__":
    verify_final_features()
