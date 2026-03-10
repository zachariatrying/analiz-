import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

class TestTOBO(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.analyzer.config['enabled_patterns'] = {'tobo': True}
        self.analyzer.config['tobo_tolerance'] = 0.2
        
    def create_strict_tobo(self, status='confirmed'):
        """
        Creates a 'Strict' TOBO pattern that satisfies:
        - 5-point structure
        - Wide enough (>15 bars)
        - Horizontal Neckline
        - Deep Head
        """
        # Create 100 bars
        x = np.arange(100)
        y = np.full(100, 100.0)
        
        # Define Pivots (spread out for strict logic)
        # LS Low at 20, Head Low at 50, RS Low at 80
        # Neckline Highs at 35 and 65
        
        # Left Shoulder Dip (15-25) -> Low at 20
        y[15:26] = np.linspace(100, 95, 11) # Down
        y[20:26] = np.linspace(95, 100, 6) # Up
        
        # Head Dip (35-65) -> Low at 50 (Deeper)
        y[35:51] = np.linspace(100, 90, 16) # Down to 90
        y[50:66] = np.linspace(90, 100, 16) # Up to 100
        
        # Right Shoulder Dip (75-85) -> Low at 80
        y[75:81] = np.linspace(100, 95, 6) # Down to 95
        y[80:86] = np.linspace(95, 100, 6) # Up to 100
        
        # Current Price Action (86-99)
        if status == 'confirmed':
            # Breakout above 100
            y[86:] = 102.0
        elif status == 'unconfirmed':
            # Recovering but below 100
            y[86:] = 98.0
            
        df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=100),
            'Open': y, 'High': y, 'Low': y, 'Close': y, 'Volume': np.random.randint(1000, 5000, 100)
        })
        return df

    def test_strict_confirmed(self):
        print("\nTesting Strict Confirmed TOBO...")
        df = self.create_strict_tobo('confirmed')
        patterns = self.analyzer.detect_classic_patterns(df)
        
        tobo = [p for p in patterns if 'TOBO' in p['name']]
        if not tobo:
            print("FAIL: No TOBO detected")
            return

        p = tobo[0]
        print(f"Detected: {p['name']}")
        print(f"Desc: {p['desc']}")
        
        self.assertEqual(p['status'], 'confirmed')
        self.assertIn('Hedef', p['desc'])
        self.assertIn('Stop', p['desc'])
        self.assertEqual(len(p['points']), 5)
        print("SUCCESS: Confirmed Strict TOBO detected.")

    def test_strict_unconfirmed(self):
        print("\nTesting Strict Unconfirmed TOBO...")
        df = self.create_strict_tobo('unconfirmed')
        patterns = self.analyzer.detect_classic_patterns(df)
        
        tobo = [p for p in patterns if 'TOBO' in p['name']]
        if not tobo:
            print("FAIL: No TOBO detected")
            return

        p = tobo[0]
        print(f"Detected: {p['name']}")
        self.assertEqual(p['status'], 'unconfirmed')
        print("SUCCESS: Unconfirmed Strict TOBO detected.")

if __name__ == '__main__':
    unittest.main()
