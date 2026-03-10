import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from analyzer import Analyzer

class TestSignals(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        
    def create_mock_data(self, condition='buy'):
        N = 100
        df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=N),
            'Close': np.linspace(100, 100, N),
            'Volume': 1000
        })
        
        # Add necessary columns manually to mock indicator values
        # Analyzer recalculates indicators in get_detailed_signals, wait...
        # Analyzer.get_detailed_signals expects 'RSI', 'MACD', etc. to be present in df?
        # No, analyze_trend/get_detailed_signals takes a df that already has indicators added.
        # So I need to add them or mock them.
        
        df['RSI'] = 50
        df['MACD'] = 0
        df['MACD_Signal'] = 0
        df['BB_Low'] = 90
        df['BB_High'] = 110
        df['SMA_50'] = 100
        df['SMA_200'] = 100
        
        if condition == 'buy':
            # RSI Oversold
            df.loc[99, 'RSI'] = 25 
            # MACD Crossover (Prev: MACD < Sig, Curr: MACD > Sig)
            df.loc[98, 'MACD'] = -0.5
            df.loc[98, 'MACD_Signal'] = 0
            df.loc[99, 'MACD'] = 0.5
            df.loc[99, 'MACD_Signal'] = 0
            # Bollinger Low
            df.loc[99, 'Close'] = 89 # Below 90
            
        elif condition == 'sell':
            # RSI Overbought
            df.loc[99, 'RSI'] = 75
            # Bollinger High
            df.loc[99, 'Close'] = 115 # Above 110
            
        return df

    def test_buy_signals(self):
        print("\nTesting BUY Signals...")
        df = self.create_mock_data('buy')
        signals = self.analyzer.get_detailed_signals(df)
        
        found_rsi = False
        found_macd = False
        found_bb = False
        
        for s in signals:
            print(f"{s['indicator']}: {s['signal']} - {s['reason']}")
            if s['indicator'] == 'RSI' and s['signal'] == 'AL': found_rsi = True
            if s['indicator'] == 'MACD' and s['signal'] == 'AL': found_macd = True
            if s['indicator'] == 'Bollinger' and s['signal'] == 'AL': found_bb = True
            
        self.assertTrue(found_rsi, "RSI Buy not found")
        self.assertTrue(found_macd, "MACD Buy not found")
        self.assertTrue(found_bb, "Bollinger Buy not found")
        print("SUCCESS: All BUY signals detected.")

    def test_sell_signals(self):
        print("\nTesting SELL Signals...")
        df = self.create_mock_data('sell')
        signals = self.analyzer.get_detailed_signals(df)
        
        found_rsi = False
        found_bb = False
        
        for s in signals:
            print(f"{s['indicator']}: {s['signal']} - {s['reason']}")
            if s['indicator'] == 'RSI' and s['signal'] == 'SAT': found_rsi = True
            if s['indicator'] == 'Bollinger' and s['signal'] == 'SAT': found_bb = True
            
        self.assertTrue(found_rsi, "RSI Sell not found")
        self.assertTrue(found_bb, "Bollinger Sell not found")
        print("SUCCESS: All SELL signals detected.")

if __name__ == '__main__':
    unittest.main()
