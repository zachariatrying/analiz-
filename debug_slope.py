import numpy as np
from scipy.stats import linregress

def calculate_trend_slope(values):
    if len(values) < 2: return 0.0
    x = np.arange(len(values))
    slope, _, _, _, _ = linregress(x, values)
    return slope / np.mean(values)

# Data from test case: 110 to 115 over 40 steps
y = np.linspace(110, 115, 40)
print(f"Data start: {y[0]}, end: {y[-1]}")
s = calculate_trend_slope(y)
print(f"Calculated Slope: {s}")
print(f"Is > 0.0? {s > 0.0}")
print(f"Is > 0.005? {s > 0.005}")

