import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

class TestTOBODowntrend(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        # Enable TOBO
        self.analyzer.config['enabled_patterns'] = {'tobo': True}
        
    def create_tobo(self, trend_type='downtrend'):
        """
        Creates a TOBO pattern with a specific pre-pattern trend.
        """
        N = 200
        y = np.full(N, 100.0)
        
        # TOBO Formation (Indices 100-160)
        # LS (110) = 90
        # H (130) = 80
        # RS (150) = 90
        # Neckline ~ 100
        
        # Left Shoulder
        y[105:111] = np.linspace(100, 90, 6)
        y[110:116] = np.linspace(90, 100, 6)
        
        # Head
        y[125:131] = np.linspace(100, 80, 6)
        y[130:136] = np.linspace(80, 100, 6)
        
        # Right Shoulder
        y[145:151] = np.linspace(100, 90, 6)
        y[150:156] = np.linspace(90, 100, 6)
        
        # Pre-Pattern Trend (0-100)
        if trend_type == 'downtrend':
            # Drop from 120 down to 100 (Valid)
            y[50:100] = np.linspace(120, 100, 50)
        elif trend_type == 'uptrend':
            # Rise from 80 up to 100 (Invalid for Reversal)
            y[50:100] = np.linspace(80, 100, 50)
            
        # Add Breakout
        y[160:] = 105
            
        df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=N),
            'Close': y, 'Open': y, 'High': y, 'Low': y, 'Volume': 1000
        })
        return df

    def test_valid_downtrend(self):
        print("\nTesting Valid Downtrend TOBO...")
        df = self.create_tobo('downtrend')
        patterns = self.analyzer.detect_classic_patterns(df)
        tobo = [p for p in patterns if 'TOBO' in p['name']]
        
        if tobo:
            print(f"SUCCESS: Detected TOBO with Downtrend. Points: {len(tobo[0]['points'])}")
            self.assertEqual(len(tobo[0]['points']), 5, "Should have 5 points")
        else:
            print("FAIL: Valid TOBO ignored.")
            self.fail("Valid TOBO ignored")

    def test_invalid_uptrend(self):
        print("\nTesting Invalid Uptrend TOBO...")
        df = self.create_tobo('uptrend')
        patterns = self.analyzer.detect_classic_patterns(df)
        tobo = [p for p in patterns if 'TOBO' in p['name']]
        
        if not tobo:
            print("SUCCESS: Invalid TOBO (after uptrend) ignored.")
        else:
            print("FAIL: Invalid TOBO detected despite uptrend.")
            self.fail("Invalid TOBO detected")

if __name__ == '__main__':
    unittest.main()
