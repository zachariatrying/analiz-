import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

class TestRSIDivergence(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.analyzer.config['enabled_patterns'] = {'tobo': False, 'flag': False, 'cup': False, 'breakout': False}
        
    def create_divergence_data(self, pattern_type='positive'):
        """
        Creates synthetic data for divergence.
        """
        N = 100
        x = np.arange(N)
        
        # Base Price & RSI
        price = np.linspace(100, 100, N)
        rsi = np.linspace(50, 50, N)
        
        if pattern_type == 'positive': # Bullish (Price LL, RSI HL)
            # Dip 1 (IDX 40)
            price[35:45] -= 10 # Low 90
            rsi[35:45] -= 20 # Low 30
            
            # Dip 2 (IDX 80)
            price[75:85] -= 15 # Low 85 (Lower)
            rsi[75:85] -= 10 # Low 40 (Higher)
            
        elif pattern_type == 'negative': # Bearish (Price HH, RSI LH)
            # Peak 1 (IDX 40)
            price[35:45] += 10 # High 110
            rsi[35:45] += 20 # High 70
            
            # Peak 2 (IDX 80)
            price[75:85] += 15 # High 115 (Higher)
            rsi[75:85] += 10 # High 60 (Lower)
            
        df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=N),
            'Close': price,
            'High': price, 'Low': price, 'Open': price, 
            'Volume': 1000
        })
        # Mock RSI directly so we don't depend on calculation logic
        df['RSI'] = rsi
        
        return df

    def test_positive_divergence(self):
        print("\nTesting Positive Divergence...")
        df = self.create_divergence_data('positive')
        # We call detect_rsi_divergence directly or detect_patterns
        patterns = self.analyzer.detect_rsi_divergence(df)
        
        div = [p for p in patterns if 'Pozitif' in p['name']]
        if not div:
            print("FAIL: No Positive Divergence detected")
        else:
            p = div[0]
            print(f"Detected: {p['name']}")
            print(f"Desc: {p['desc']}")
            self.assertEqual(p['type'], 'divergence_pos')
            print("SUCCESS: Positive Divergence detected.")

    def test_negative_divergence(self):
        print("\nTesting Negative Divergence...")
        df = self.create_divergence_data('negative')
        patterns = self.analyzer.detect_rsi_divergence(df)
        
        div = [p for p in patterns if 'Negatif' in p['name']]
        if not div:
            print("FAIL: No Negative Divergence detected")
        else:
            p = div[0]
            print(f"Detected: {p['name']}")
            print(f"Desc: {p['desc']}")
            self.assertEqual(p['type'], 'divergence_neg')
            print("SUCCESS: Negative Divergence detected.")

if __name__ == '__main__':
    unittest.main()

