import pandas as pd
import numpy as np
from analyzer import Analyzer

# Mock Analyzer Config
config = {
    'tobo_tolerance': 0.20,
    'tobo_min_depth': 0.03,
    'cup_min_depth': 0.10
}

def create_synthetic_tobo(fail_case=False):
    # Create a perfect TOBO
    # LS at 100, Neck at 110, Head at 90, Neck at 110, RS at 100
    # We need intermediate points to simulate "candles"
    
    dates = pd.date_range(start='2024-01-01', periods=50)
    
    # Base pattern points (approximate indices)
    # 0-10: Down to LS (100)
    # 10-20: Up to N1 (110)
    # 20-30: Down to H (90)
    # 30-40: Up to N2 (110)
    # 40-50: Down to RS (100)
    
    prices = np.linspace(120, 100, 10) # 0-10
    prices = np.concatenate([prices, np.linspace(100, 110, 10)]) # 10-20
    prices = np.concatenate([prices, np.linspace(110, 90, 10)])  # 20-30
    prices = np.concatenate([prices, np.linspace(90, 110, 10)])  # 30-40
    prices = np.concatenate([prices, np.linspace(110, 100, 10)]) # 40-50
    
    # Create DF
    df = pd.DataFrame({'Date': dates, 'Close': prices, 'High': prices+1, 'Low': prices-1, 'Open': prices})
    
    # Set Exact Key Points to ensure ZigZag catches them
    # LS (idx 9)
    df.at[9, 'Low'] = 100
    df.at[9, 'Close'] = 100
    # N1 (idx 19)
    df.at[19, 'High'] = 110
    df.at[19, 'Close'] = 110
    # Head (idx 29)
    df.at[29, 'Low'] = 90
    df.at[29, 'Close'] = 90
    # N2 (idx 39)
    df.at[39, 'High'] = 110
    df.at[39, 'Close'] = 110
    # RS (idx 49)
    df.at[49, 'Low'] = 100
    df.at[49, 'Close'] = 100
    
    # In FAIL CASE: Add a wick lower than Head (90) somewhere else
    if fail_case:
        # At index 15 (between LS and N1, or anywhere really, let's put it near Head)
        # Let's put it at index 25 (approaching Head)
        df.at[25, 'Low'] = 88 # 88 < 90. This should INVALIDATE pattern.
        df.at[25, 'Close'] = 92 # Close is still higher, only Wick is lower!
        print("created fail case: Low 88 vs Head 90")
    
    # Add Vol SMA for completeness
    df['Volume'] = 1000
    df['Vol_SMA_20'] = 1000
    df['RSI'] = 50
    
    return df

analyzer = Analyzer()
analyzer.config = config

print("--- TEST 1: INVALID PATTERN (Lower Wick) ---")
df_fail = create_synthetic_tobo(fail_case=True)
# We need to manually feed zigzag points because calculate_zigzag might be sensitive to noise
# But let's try to detect using the full pipeline first
zz_points_fail = analyzer.calculate_zigzag(df_fail, deviation=0.05)
# Override zigzag to ensure it sees the shape, we are testing the VALIDATION logic, not detection
# But wait, strict validation is inside detect_tobo_zigzag
# Let's manually construct the zigzag points passed to it to isolate the test
manual_zz = [
    {'idx': 9, 'price': 100, 'type': 'low'},   # LS
    {'idx': 19, 'price': 110, 'type': 'high'}, # N1
    {'idx': 29, 'price': 90, 'type': 'low'},   # Head
    {'idx': 39, 'price': 110, 'type': 'high'}, # N2
    {'idx': 49, 'price': 100, 'type': 'low'},  # RS
]
# We also need to reverse it because the function iterates backwards
manual_zz.reverse() # RS, N2, H, N1, LS

patterns_fail = analyzer.detect_tobo_zigzag(df_fail, manual_zz)
if len(patterns_fail) == 0:
    print("SUCCESS: Invalid pattern rejected!")
else:
    print("FAILURE: Invalid pattern ACCEPTED! logic is broken.")


print("\n--- TEST 2: VALID PATTERN (Clean) ---")
df_valid = create_synthetic_tobo(fail_case=False)
patterns_valid = analyzer.detect_tobo_zigzag(df_valid, manual_zz)
if len(patterns_valid) > 0:
    print(f"SUCCESS: Valid pattern detected! Name: {patterns_valid[0]['name']}")
else:
    print("FAILURE: Valid pattern REJECTED! Logic is too strict.")
