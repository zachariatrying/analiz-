import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

class TestFlagElite(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.analyzer.config['enabled_patterns'] = {'flag': True}
        
    def create_flag_data(self, pole_pct=0.20, retracement=0.30, volume="good"):
        # N=100 bars
        N = 100
        y = np.full(N, 100.0)
        vol = np.full(N, 1000.0)
        dates = pd.date_range(start='2023-01-01', periods=N)
        
        # 1. Base (0-50)
        y[0:50] = 100.0
        
        # 2. Pole (50-60) - Sharp Rise
        # Start at 100. End at 100*(1+pole_pct).
        pole_top = 100.0 * (1 + pole_pct)
        y[50:60] = np.linspace(100, pole_top, 10)
        
        # Pole Volume High
        if volume == "good":
            vol[50:60] = 5000
        
        # 3. Flag (60-80) - Consolidation
        # Retraces down to (pole_top - pole_height * retracement)
        pole_height = pole_top - 100
        flag_low = pole_top - (pole_height * retracement)
        
        # Triangle/Channel shape
        y[60:80] = np.linspace(pole_top, flag_low, 20)
        
        # Flag Volume Low
        if volume == "good":
            vol[60:80] = 500
            
        # 4. Breakout (80+) -> Up
        y[80:] = pole_top + 2.0
        
        # Breakout Vol
        if volume == "good":
            vol[80] = 6000
            
        df = pd.DataFrame({
            'Date': dates,
            'Close': y, 'Open': y, 'High': y, 'Low': y, 'Volume': vol
        })
        return df

    def test_ideal_flag(self):
        print("\nTesting IDEAL Flag (Strong Pole, Tight Flag)...")
        # 20% Pole, 30% Retracement (Valid)
        # We slice the dataframe to be "just after" breakout (e.g. idx 82)
        # Pattern occurs at 50-80. Breakout at 80.
        # If we send full 100 bars, it's 20 bars stale.
        full_df = self.create_flag_data(pole_pct=0.20, retracement=0.30)
        df = full_df.iloc[:85].copy() # Cut off the "future"
        
        patterns = self.analyzer.detect_classic_patterns(df)
        flag = [p for p in patterns if 'Flama' in p['name']]
        
        if flag:
            p = flag[0]
            print(f"Flag Found: {p['name']} | Score: {p['score']}")
            self.assertTrue(p['score'] > 60)
            self.assertIn("Direk", p['desc'])
        else:
            print(f"DEBUG: All Patterns Found: {[p['name'] for p in patterns]}")
            self.fail("Ideal Flag not detected")

    def test_deep_correction(self):
        print("\nTesting Deep Correction (Invalid Flag)...")
        # 20% Pole, 60% Retracement (Invalid > 50%)
        df = self.create_flag_data(pole_pct=0.20, retracement=0.60)
        patterns = self.analyzer.detect_classic_patterns(df)
        flag = [p for p in patterns if 'Flama' in p['name']]
        
        if flag:
            print("FAIL: Deep flag detected!")
            self.fail("Should reject deep retracement (>50%)")
        else:
            print("SUCCESS: Deep correction rejected.")
            
    def test_weak_pole(self):
        print("\nTesting Weak Pole (<10%)...")
        # 5% Pole (Invalid)
        df = self.create_flag_data(pole_pct=0.05, retracement=0.30)
        patterns = self.analyzer.detect_classic_patterns(df)
        flag = [p for p in patterns if 'Flama' in p['name']]
        
        if flag:
            print("FAIL: Weak pole detected!")
            self.fail("Should reject weak pole")
        else:
            print("SUCCESS: Weak pole rejected.")

if __name__ == '__main__':
    unittest.main()
