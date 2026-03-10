import pandas as pd
import time
from src.data_manager import DataManager
from src.analyzer import Analyzer

def dedektif_tarama(hisse_listesi):
    print(f"\n🕵️ DETEKTİF MODU BAŞLATILDI: {len(hisse_listesi)} hisse taranacak...")
    
    dm = DataManager()
    analyzer = Analyzer()
    
    # Configure Analyzer with relaxed settings for debugging
    analyzer.config['flag_pole_min'] = 0.03 # 3%
    
    for sembol in hisse_listesi:
        try:
            print(f"\n🔍 Analiz Ediliyor: {sembol}")
            # 1. VERİ KONTROLÜ
            # Force download true to test API
            df = dm.fetch_stock_data(sembol, interval="1d") 
            
            if df is None or df.empty:
                print(f"❌ {sembol}: Veri çekilemedi (BOŞ). API engeli olabilir!")
                time.sleep(1) # Engeli aşmak için bekle
                continue
                
            print(f"   📊 Veri Tamam: {len(df)} bar geldi. Son Tarih: {df.index[-1] if not df.empty else 'Yok'}")

            if len(df) < 60:
                print(f"⚠️ {sembol}: Yetersiz veri ({len(df)} bar). En az 60 lazım.")
                continue

            # 2. ANALİZ KONTROLÜ
            # Calculate indicators first as app does
            df = analyzer.add_indicators(df)
            
            # Detect Flags
            start_t = time.time()
            sonuc = analyzer.detect_flag_pattern(df)
            dur = time.time() - start_t

            if sonuc:
                for p in sonuc:
                    print(f"✅ BULUNDU: {sembol} - {p['name']} (Skor: {p['score']})")
            else:
                print(f"Running... {sembol}: Temiz (Formasyon yok) - {dur:.4f}s")
                # Debug internal values if possible? 
                # Since we can't easily see inside the function without modifying it, 
                # we rely on the fact that we have data.

        except Exception as e:
            print(f"🔥 {sembol} HATASI: {e}")
        
        # Rate limiting sleep
        time.sleep(0.5) 

if __name__ == "__main__":
    test_tickers = ["THYAO.IS", "GARAN.IS", "ASELS.IS", "KCHOL.IS", "AKBNK.IS"]
    dedektif_tarama(test_tickers)

