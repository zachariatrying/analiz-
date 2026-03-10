import matplotlib.pyplot as plt
import numpy as np

# Create synthetic data for TOBO (Inverse Head & Shoulders)
# Pattern: Downtrend -> Left Shoulder -> Head -> Right Shoulder -> Uptrend

x = np.linspace(0, 100, 500)
y = np.zeros_like(x)

# Base curve (downtrend then uptrend)
y = 100 - x + (x**2)/150

# Add the shoulders and head inverted gaussian-like dips
def add_dip(x, center, depth, width):
    return -depth * np.exp(-((x - center)**2) / (2 * width**2))

# Trend line base
base_trend = 120 - 0.5*x 
# Adjust trend to be flatter for clearer visual
base_trend = np.full_like(x, 100)

# Left Shoulder (LS)
y += add_dip(x, 30, 20, 5)
# Head (H) - Deeper
y += add_dip(x, 50, 40, 5)
# Right Shoulder (RS) - Similar to LS
y += add_dip(x, 70, 20, 5)

# Add some noise for realism
np.random.seed(42)
noise = np.random.normal(0, 1, size=len(x))
y = base_trend + y + noise

plt.figure(figsize=(12, 8))
plt.plot(x, y, label='Price', color='green', linewidth=2)

# Mark key points
ls_idx = 30 * 5 # approx index for 30
h_idx = 50 * 5
rs_idx = 70 * 5

# Identify actual minima in those regions
def find_min_idx(center_idx, span=20):
    start = max(0, center_idx - span)
    end = min(len(y), center_idx + span)
    return start + np.argmin(y[start:end])

real_ls_idx = find_min_idx(150) # 30 * 5
real_h_idx = find_min_idx(250)  # 50 * 5
real_rs_idx = find_min_idx(350) # 70 * 5

# Plot markers
plt.scatter([x[real_ls_idx], x[real_h_idx], x[real_rs_idx]], 
            [y[real_ls_idx], y[real_h_idx], y[real_rs_idx]], 
            color='red', s=100, zorder=5)

# Annotate
plt.annotate('Sol Omuz (Left Shoulder)', xy=(x[real_ls_idx], y[real_ls_idx]), xytext=(x[real_ls_idx]-10, y[real_ls_idx]-10),
             arrowprops=dict(facecolor='white', shrink=0.05), color='white', fontsize=12, fontweight='bold')

plt.annotate('Bas (Head)', xy=(x[real_h_idx], y[real_h_idx]), xytext=(x[real_h_idx], y[real_h_idx]-15),
             arrowprops=dict(facecolor='white', shrink=0.05), color='white', fontsize=12, fontweight='bold', ha='center')

plt.annotate('Sag Omuz (Right Shoulder)', xy=(x[real_rs_idx], y[real_rs_idx]), xytext=(x[real_rs_idx]+10, y[real_rs_idx]-10),
             arrowprops=dict(facecolor='white', shrink=0.05), color='white', fontsize=12, fontweight='bold', ha='right')

# Neckline
# Find peaks between shoulders to draw neckline
def find_max_idx(start_idx, end_idx):
    return start_idx + np.argmax(y[start_idx:end_idx])

peak1 = find_max_idx(real_ls_idx, real_h_idx)
peak2 = find_max_idx(real_h_idx, real_rs_idx)

plt.plot([x[peak1], x[peak2]], [y[peak1], y[peak2]], 'w--', linewidth=2, label='Boyun Cizgisi (Neckline)')
plt.text((x[peak1]+x[peak2])/2, (y[peak1]+y[peak2])/2 + 2, 'Boyun Cizgisi (Neckline)', color='white', fontsize=11, ha='center')

# Styles
plt.title('Ters Omuz Bas Omuz (TOBO) Formasyonu', color='white', fontsize=16)
plt.gca().set_facecolor('#1e1e1e')
plt.gcf().patch.set_facecolor('#121212')
plt.tick_params(colors='white')
plt.grid(True, alpha=0.2)
plt.legend()

# Save
output_path = r'c:\Users\ibrah\.gemini\antigravity\brain\2efd8093-4e9f-49f5-8f9c-614217df062e\tobo_viz.png'
plt.savefig(output_path)
print(f"Graph saved to {output_path}")
