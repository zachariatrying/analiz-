import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

class TestCupElite(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.analyzer.config['enabled_patterns'] = {'cup': True}
        
    def create_cup_data(self, shape="u", handle_slope="down", volume="good"):
        N = 300
        y = np.full(N, 100.0)
        vol = np.full(N, 1000.0)
        
        # P1 (Left Lip) at 100
        y[90:100] = 110.0 # High
        
        # Cup Bottom
        if shape == "u":
            # Round bottom
            y[100:130] = np.linspace(110, 80, 30)
            y[130:170] = 80 + np.random.normal(0, 0.5, 40) # Flat bottom
            y[170:200] = np.linspace(80, 110, 30)
        elif shape == "v":
            # Sharp V
            y[100:150] = np.linspace(110, 60, 50)
            y[150:200] = np.linspace(60, 110, 50)
            
        # P2 (Right Lip) at 200 -> 110
        
        # Handle (200-240)
        if handle_slope == "down":
            y[200:245] = np.linspace(110, 105, 45) # Gentle down
        elif handle_slope == "up":
            y[200:245] = np.linspace(110, 115, 45) # Up (Invalid)
            
        # Breakout
        y[245:] = 115
        
        if volume == "good":
            vol[245] = 10000 # Breakout
            
        df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=N),
            'Close': y, 'Open': y, 'High': y, 'Low': y, 'Volume': vol
        })
        df['Vol_SMA_20'] = 1000
        return df

    def test_ideal_cup(self):
        print("\nTesting IDEAL Cup (U-Shape + Down Handle)...")
        df = self.create_cup_data(shape="u", handle_slope="down")
        patterns = self.analyzer.detect_classic_patterns(df)
        cup = [p for p in patterns if 'Fincan' in p['name']]
        
        if cup:
            print(f"Cup Found: {cup[0]['name']} | Quality: {cup[0]['quality']}")
            self.assertTrue(cup[0]['score'] > 60)
        else:
            self.fail("Ideal Cup not detected")

    def test_bad_handle(self):
        print("\nTesting Bad Handle (Upward Slope)...")
        df = self.create_cup_data(shape="u", handle_slope="up")
        patterns = self.analyzer.detect_classic_patterns(df)
        cup = [p for p in patterns if 'Fincan' in p['name']]
        
        if cup:
            with open('cup_fail.txt', 'w') as f:
                f.write(f"FAIL: Upward handle detected as Cup!\n")
                f.write(f"Pattern Points: {cup[0]['points']}\n")
                f.write(f"Desc: {cup[0]['desc']}\n")
                f.write(f"Score: {cup[0]['score']}\n")
            print("FAIL: Check cup_fail.txt")
            self.fail("Should reject upward handle")
        else:
            print("SUCCESS: Upward handle rejected.")

if __name__ == '__main__':
    unittest.main()
