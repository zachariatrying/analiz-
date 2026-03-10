import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

class TestTOBOFilter(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.analyzer.config['enabled_patterns'] = {'tobo': True}
        
    def create_tobo(self, status='active'):
        """
        Creates a TOBO.
        active: Price is near breakout (Target not reached).
        completed: Price >= Target.
        """
        N = 200
        y = np.full(N, 100.0)
        
        # Pre-Trend Drop (for validity)
        y[50:100] = np.linspace(120, 100, 50)
        
        # TOBO Formation (Neck ~ 100, Head ~ 80)
        # Depth = 20. Target = 100 + 20 = 120.
        
        # LS
        y[105:111] = np.linspace(100, 90, 6)
        y[110:116] = np.linspace(90, 100, 6)
        
        # Head
        y[125:131] = np.linspace(100, 80, 6)
        y[130:136] = np.linspace(80, 100, 6)
        
        # RS
        y[145:151] = np.linspace(100, 90, 6)
        y[150:156] = np.linspace(90, 100, 6)
        
        # Breakout
        if status == 'active':
            y[160:] = 105 # Breakout but below target (120)
        elif status == 'completed':
            y[160:] = 125 # Above target (120)
            
        df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=N),
            'Close': y, 'Open': y, 'High': y, 'Low': y, 'Volume': 1000
        })
        return df

    def test_active_pattern(self):
        print("\nTesting Active TOBO...")
        df = self.create_tobo('active')
        patterns = self.analyzer.detect_classic_patterns(df)
        tobo = [p for p in patterns if 'TOBO' in p['name']]
        
        if tobo:
            print(f"SUCCESS: Active TOBO detected. Price: {df['Close'].iloc[-1]}")
        else:
            print("FAIL: Active TOBO ignored.")
            self.fail("Active TOBO ignored")

    def test_completed_pattern(self):
        print("\nTesting Completed TOBO (Price > Target)...")
        df = self.create_tobo('completed')
        patterns = self.analyzer.detect_classic_patterns(df)
        tobo = [p for p in patterns if 'TOBO' in p['name']]
        
        if not tobo:
            print("SUCCESS: Completed TOBO ignored.")
        else:
            print(f"FAIL: Completed TOBO detected! Target: {tobo[0]['target']}, Price: {df['Close'].iloc[-1]}")
            self.fail("Completed TOBO detected")

if __name__ == '__main__':
    unittest.main()
