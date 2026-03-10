from src.analyzer import Analyzer
from src.data_manager import DataManager
import pandas as pd

manager = DataManager()
analyzer = Analyzer()

# Configure like app.py
analyzer.config['enabled_patterns'] = {'tobo': True, 'flag': True, 'cup': True, 'breakout': True}

ticker = "BRKVY.IS"
print(f"Analyzing {ticker}...")

try:
    df = manager.fetch_stock_data(ticker, interval='1d')
    if df is not None:
        df_res = analyzer.resample_data(df, "Günlük")
        detection_df = df_res.tail(500)
        indicators = analyzer.add_indicators(detection_df)
        patterns = analyzer.detect_classic_patterns(indicators, timeframe="Günlük")
        
        if patterns:
            with open("brkvy_result.txt", "w", encoding="utf-8") as f:
                f.write(f"Found {len(patterns)} patterns.\n")
                for p in patterns:
                    f.write("\n--- PATTERN FOUND ---\n")
                    f.write(f"Name: {p['name']}\n")
                    f.write(f"Score: {p['score']}\n")
                    f.write(f"Desc: {p['desc']}\n")
                    f.write(f"Points: {p.get('Points')}\n")
                    f.write(f"Target: {p.get('target')}\n")
            print("Results written to brkvy_result.txt")
        else:
            with open("brkvy_result.txt", "w", encoding="utf-8") as f:
               f.write("No patterns found.")
    else:
        print("Could not fetch data.")
except Exception as e:
    print(f"Error: {e}")
