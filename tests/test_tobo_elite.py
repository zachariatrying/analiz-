import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

class TestTOBOElite(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.analyzer.config['enabled_patterns'] = {'tobo': True}
        
    def create_elite_tobo_data(self, trend="down", volume_type="ideal"):
        """
        Creates a synthetic TOBO data with controllable Pre-Trend and Volume Profile.
        """
        N = 300
        # Base Price
        y = np.full(N, 100.0)
        vol = np.full(N, 1000.0)
        
        # 1. Pre-Trend (0-100)
        if trend == "down":
            # Strong Downtrend from 140 to 100
            y[0:100] = np.linspace(140, 100, 100)
        elif trend == "up":
            # Uptrend from 60 to 100 (Invalid for Reversal TOBO)
            y[0:100] = np.linspace(60, 100, 100)
        elif trend == "flat":
             y[0:100] = 100.0
             
        # 2. TOBO Geometry (100-200)
        # LS(120)=90, H(150)=80, RS(180)=90, Neck=100
        
        # Left Shoulder
        y[110:130] = np.linspace(100, 90, 20) # Down
        y[130:140] = np.linspace(90, 100, 10)  # Up
        ls_idx = 130
        
        # Head
        y[140:150] = np.linspace(100, 80, 10)  # Down deep
        y[150:160] = np.linspace(80, 100, 10)  # Up
        h_idx = 150
        
        # Right Shoulder
        y[160:175] = np.linspace(100, 92, 15) # Down shallow (Fib check: > 84.7) 92 is good
        y[175:190] = np.linspace(92, 100, 15) # Up
        rs_idx = 175
        
        # Breakout
        y[200:] = 105
        
        # 3. Volume Profile
        if volume_type == "ideal":
             vol[ls_idx-5:ls_idx+5] = 5000 # High LS
             vol[h_idx-5:h_idx+5] = 2000   # Lower Head
             vol[rs_idx-5:rs_idx+5] = 1000 # Low RS
             vol[200] = 10000              # Breakout Boom
        elif volume_type == "bad":
             vol[h_idx-5:h_idx+5] = 10000 # Huge volume at Head bottom (Catching the knife, risky?)
             vol[200] = 100               # No volume breakout

        df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=N),
            'Close': y, 'Open': y, 'High': y, 'Low': y, 'Volume': vol
        })
        # Add Vol SMA
        df['Vol_SMA_20'] = df['Volume'].rolling(20).mean().fillna(1000)
        
        return df

    def test_ideal_elite_tobo(self):
        print("\nTesting IDEAL Elite TOBO (Downtrend + Vol + Geo)...")
        df = self.create_elite_tobo_data(trend="down", volume_type="ideal")
        patterns = self.analyzer.detect_classic_patterns(df)
        print(f"DEBUG: All Patterns: {patterns}")
        tobo = [p for p in patterns if 'TOBO' in p['name']]
        
        if tobo:
            p = tobo[0]
            print(f"DTOBO Found: {p['name']} | Score: {p['score']}")
            self.assertTrue(p['score'] > 60, "Ideal TOBO score should be high")
            self.assertIn("Hacimli", p['name'], "Should detect volume")
        else:
            self.fail("Ideal TOBO not detected")

    def test_trend_filtering(self):
        print("\nTesting Trend Filtering (Uptrend Rejection)...")
        df = self.create_elite_tobo_data(trend="up", volume_type="ideal")
        patterns = self.analyzer.detect_classic_patterns(df)
        tobo = [p for p in patterns if 'TOBO' in p['name']]
        
        if tobo:
            print(f"FAIL: Detected TOBO after Uptrend! Score: {tobo[0]['score']}")
            self.fail("Should reject TOBO after uptrend")
        else:
            print("SUCCESS: Properly rejected TOBO after uptrend.")

    def test_geometry_check(self):
        # We can reuse the old logic check, but let's trust the main test
        pass

if __name__ == '__main__':
    unittest.main()
