import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

class TestTOBOStrict(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.analyzer.config['enabled_patterns'] = {'tobo': True}

    def create_tobo_data(self, ls=185, head=183, rs=185):
        N = 200
        dates = pd.date_range('2023-01-01', periods=N)
        y = np.full(N, 200.0)
        
        # LS at 40
        y[40] = ls
        # Neck 1 at 60
        y[60] = 195
        # Head at 80
        y[80] = head
        # Neck 2 at 100
        y[100] = 195
        # RS at 120
        y[120] = rs
        # Breakout
        y[130:] = 205
        
        # Linear interp
        y[0:40] = np.linspace(220, ls, 40)
        y[40:60] = np.linspace(ls, 195, 20)
        y[60:80] = np.linspace(195, head, 20)
        y[80:100] = np.linspace(head, 195, 20)
        y[100:120] = np.linspace(195, rs, 20)
        
        df = pd.DataFrame({'Date': dates, 'Close': y, 'High': y, 'Low': y, 'Volume': 1000})
        return df

    def test_flat_tobo_rejection(self):
        print("\nTesting Flat TOBO (Triple Bottom style)...")
        # LS=183, Head=182.9, RS=183.1 -> Head is only 0.05% lower
        df = self.create_tobo_data(ls=183, head=182.9, rs=183.1)
        zz = self.analyzer.calculate_zigzag(df)
        patterns = self.analyzer.detect_tobo_zigzag(df, zz)
        self.assertEqual(len(patterns), 0, "Flat TOBO should be rejected")
        print("SUCCESS: Flat TOBO rejected.")

    def test_proper_tobo_acceptance(self):
        print("\nTesting Distinct TOBO...")
        # LS=186, Head=180, RS=186 -> Head is ~3.2% lower
        df = self.create_tobo_data(ls=186, head=180, rs=186)
        zz = self.analyzer.calculate_zigzag(df)
        patterns = self.analyzer.detect_tobo_zigzag(df, zz)
        self.assertTrue(len(patterns) > 0, "Distinct TOBO should be accepted")
        print("SUCCESS: Distinct TOBO accepted.")

if __name__ == '__main__':
    unittest.main()

