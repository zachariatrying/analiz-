from src.analyzer import Analyzer
from src.data_manager import DataManager
import time
import os

def verify_sequential():
    print("--- HASSA TARAMA (SEQUENTIAL + TRADINGVIEW) ---")
    manager = DataManager()
    analyzer = Analyzer()
    
    # Target Tickers
    tickers = ["THYAO.IS", "TCELL.IS", "AKBNK.IS", "QUAGR.IS"]
    
    # Config Mock
    config = {
        'timeframe': 'Günlük',
        'use_bull_flag': True, 'use_bear_flag': True,
        'use_bull_pennant': True, 'use_bear_pennant': True,
        'use_div_pos': True, 'use_div_neg': True,
        'use_candle': True, 'use_tobo': True, 'use_obo': True, 'use_cup': True,
        'show_confirmed': True, 'show_unconfirmed': True
    }
    
    found_count = 0
    
    for ticker in tickers:
        print(f"\nProses Ediliyor: {ticker}")
        
        # 1. Reset variable
        df = None
        
        # 2. Fetch
        df = manager.fetch_stock_data(ticker)
        if df is None:
            print(f"❌ {ticker} Veri Alınamadı.")
            continue
            
        last_price = df['Close'].iloc[-1]
        print(f"✅ {ticker} Başarılı. Fiyat: {last_price:.2f}")
        
        # 3. Detect
        indicators = analyzer.add_indicators(df.tail(200))
        patterns = analyzer.detect_classic_patterns(indicators)
        
        if patterns:
            print(f"🎯 Pattern Bulundu: {patterns[0]['name']} ({patterns[0]['status']})")
            found_count += 1
        else:
            print(f"ℹ️ Pattern Bulunmadı.")
            
        # 4. Explicit Delete
        del df
        
    print(f"\n--- SONUÇ ---")
    print(f"Toplam: {len(tickers)} | Bulunan: {found_count}")

if __name__ == "__main__":
    verify_sequential()
