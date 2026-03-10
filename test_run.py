from src.data_manager import DataManager
from src.analyzer import Analyzer
import pandas as pd

def test_system():
    print("Initializing DataManager...")
    dm = DataManager()
    ipo_list = dm.get_ipo_list('US Market')
    print(f"Loaded {len(ipo_list)} US IPOs.")
    
    ticker = 'PLTR'
    print(f"Fetching data for {ticker}...")
    try:
        # Check if we can fetch data (might fail if no internet, but code structure is tested)
        # We'll mock the fetch if it fails to just test logic
        df = dm.fetch_stock_data(ticker)
        
        if df is None:
            print("Could not fetch data (network issue?), creating dummy data.")
            # Create dummy data for testing logic
            dates = pd.date_range(start='2020-01-01', periods=100)
            df = pd.DataFrame({
                'Date': dates,
                'Open': [100] * 100,
                'High': [110] * 100,
                'Low': [90] * 100,
                'Close': [105] * 100,
                'Volume': [1000] * 100
            })
        
        print(f"Data shape: {df.shape}")
        
        print("Initializing Analyzer...")
        analyzer = Analyzer()
        
        print("Adding indicators...")
        df_analyzed = analyzer.add_indicators(df)
        print("Indicators added:", list(df_analyzed.columns))
        
        print("Detecting patterns...")
        patterns = analyzer.detect_patterns(df_analyzed)
        print("Patterns detected:", patterns)
        
        print("Testing similarity search...")
        # Self comparison should yield 0 distance
        matches = analyzer.find_similar_patterns(df_analyzed, {ticker: df_analyzed})
        print("Matches:", matches)
        
        print("\nSUCCESS: System structure appears valid.")
        
    except Exception as e:
        print(f"\nFAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_system()

