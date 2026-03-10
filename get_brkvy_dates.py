from src.analyzer import Analyzer
from src.data_manager import DataManager
import pandas as pd

manager = DataManager()
analyzer = Analyzer()

ticker = "BRKVY.IS"
try:
    df = manager.fetch_stock_data(ticker, interval='1d')
    if df is not None:
        # Replicate the exact processing steps
        df_res = analyzer.resample_data(df, "Günlük")
        detection_df = df_res.tail(500) # Indices are relative to this tail
        
        # Indices from previous result
        # Points: {'p_start_idx': 442, 'p_end_idx': 473, 'f_end_idx': 499}
        idx_start = 442
        idx_peak = 473
        idx_break = 499
        
        # Get Dates
        # Check if Date is in columns or index
        if 'Date' in detection_df.columns:
             date_start = pd.to_datetime(detection_df['Date'].iloc[idx_start])
             date_peak = pd.to_datetime(detection_df['Date'].iloc[idx_peak])
             date_break = pd.to_datetime(detection_df['Date'].iloc[idx_break])
        else:
             detection_df.index = pd.to_datetime(detection_df.index)
             date_start = detection_df.index[idx_start]
             date_peak = detection_df.index[idx_peak]
             date_break = detection_df.index[idx_break]
        
        with open("dates.txt", "w", encoding="utf-8") as f:
            f.write(f"Start: {date_start.strftime('%d %B %Y')}\n")
            f.write(f"Peak: {date_peak.strftime('%d %B %Y')}\n")
            f.write(f"Break: {date_break.strftime('%d %B %Y')}\n")
        print("Dates written to dates.txt")
        
    else:
        print("Could not fetch data.")
except Exception as e:
    print(f"Error: {e}")

