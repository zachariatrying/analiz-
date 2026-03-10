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
        self.analyzer.config['enabled_patterns'] = {
            'div_pos': True,
            'div_neg': True
        }

    def create_rsi_data(self, price_trend="down", rsi_trend="up", rsi_reset=False):
        """Creates synthetic data for RSI divergence."""
        N = 100
        dates = pd.date_range('2023-01-01', periods=N)
        
        # Base price
        price = np.linspace(100, 80, N) if price_trend == "down" else np.linspace(80, 100, N)
        
        if price_trend == "down":
            # Low 1 at index 40, Low 2 at index 80
            price[40] = 70
            price[80] = 65
        else:
            # High 1 at index 40, High 2 at index 80
            price[40] = 110
            price[80] = 115
            
        # Add some noise to pivots
        price[39:42] = price[40] + np.array([1, 0, 1])
        price[79:82] = price[80] + np.array([1, 0, 1])

        # RSI simulation (simplified)
        rsi = np.full(N, 50.0)
        if rsi_trend == "up": # Positive Div: Price LL, RSI HL
            rsi[40] = 25
            rsi[80] = 35
            if rsi_reset:
                rsi[60] = 60 # Crossed midline
        else: # Negative Div: Price HH, RSI LH
            rsi[40] = 75
            rsi[80] = 65
            if rsi_reset:
                rsi[60] = 40 # Crossed midline

        df = pd.DataFrame({
            'Date': dates,
            'Close': price,
            'High': price + 0.5,
            'Low': price - 0.5,
            'Volume': np.random.rand(N) * 1000,
            'RSI': rsi
        })
        return df

    def test_ideal_positive_divergence(self):
        print("\nTesting Ideal Positive Divergence...")
        df = self.create_rsi_data(price_trend="down", rsi_trend="up")
        patterns = self.analyzer.detect_rsi_divergence(df)
        self.assertTrue(any(p['type'] == 'divergence_pos' for p in patterns), "Should detect positive divergence")
        print("SUCCESS: Positive Divergence detected.")

    def test_rsi_reset_rejection(self):
        print("\nTesting RSI Reset Rejection (Line of Sight)...")
        # Elite rule: RSI shouldn't cross 50 significantly between points
        df = self.create_rsi_data(price_trend="down", rsi_trend="up", rsi_reset=True)
        patterns = self.analyzer.detect_rsi_divergence(df)
        self.assertFalse(any(p['type'] == 'divergence_pos' for p in patterns), "Should reject divergence if RSI resets (>55)")
        print("SUCCESS: RSI Reset divergence correctly rejected.")

if __name__ == '__main__':
    unittest.main()
