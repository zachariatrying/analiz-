import pandas as pd
import numpy as np
from src.analyzer import Analyzer
import os

# Create synthetic data for verification
def generate_cup_handle():
    x = np.linspace(0, 100, 100)
    # Cup: Parabola
    y_cup = 0.05 * (x[:80] - 40)**2 + 100
    # Handle: Small downtrend
    y_handle = 130 - 0.5 * (x[80:] - 80)
    
    y = np.concatenate([y_cup, y_handle])
    # Last point break out slightly
    y[-1] = 135 
    
    df = pd.DataFrame({'Close': y, 'High': y+1, 'Low': y-1, 'Date': pd.date_range('2023-01-01', periods=100)})
    return df

def generate_downtrend_breakout():
    x = np.linspace(0, 100, 100)
    # Lower highs: 100 -> 90 -> 80
    y = 100 - 0.2 * x + 5 * np.sin(x/5)
    # Breakout at end
    y[-1] = y[-1] + 10 
    
    df = pd.DataFrame({'Close': y, 'High': y+1, 'Low': y-1, 'Date': pd.date_range('2023-01-01', periods=100)})
    return df

print("Initializing...")
analyzer = Analyzer()
analyzer = Analyzer()
# visualizer removed

print("--- Testing Cup & Handle ---")
df_cup = generate_cup_handle()
# Add indicators (Required by detect_patterns)
df_cup = analyzer.add_indicators(df_cup) 
patterns_cup = analyzer.detect_patterns(df_cup) # Unified call

for p in patterns_cup:
    if isinstance(p, dict):
        print(f"Found: {p['name']} - {p['desc']}")
        # Visualize - REMOVED
        # path = visualizer.plot_pattern(df_cup, p, ticker="TEST_CUP")
        # print(f"Chart saved to: {path}")

print("\n--- Testing Downtrend Breakout ---")
df_down = generate_downtrend_breakout()
df_down = analyzer.add_indicators(df_down)
patterns_down = analyzer.detect_patterns(df_down)

for p in patterns_down:
    if isinstance(p, dict):
        print(f"Found: {p['name']} - {p['desc']}")
        # Visualize - REMOVED
        # path = visualizer.plot_pattern(df_down, p, ticker="TEST_BREAKOUT")
        # print(f"Chart saved to: {path}")

print("\nDONE.")

