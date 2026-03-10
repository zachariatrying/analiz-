from src.analyzer import Analyzer
from src.data_manager import DataManager
from src.data_manager import DataManager
import time
import pandas as pd
import os

# --- AYARLAR ---
# --- AYARLAR ---

def sonuclari_kaydet(result):
    """Bulunan formasyonları CSV'ye kaydeder."""
    filename = "tarama_sonuclari.csv"
    df_res = pd.DataFrame([result])
    if not os.path.exists(filename):
        df_res.to_csv(filename, index=False)
    else:
        df_res.to_csv(filename, mode='a', header=False, index=False)

# Init
manager = DataManager()
analyzer = Analyzer()
analyzer.config['flag_pole_min'] = 0.05
analyzer.config['enabled_patterns'] = {'flag': True, 'flama': True, 'tobo': True, 'cup': True}

# Tickers
tickers = ["THYAO.IS", "ASELS.IS", "TCELL.IS", "AKBNK.IS", "GARAN.IS", "KCHOL.IS", "TUPRS.IS", "SISE.IS"]
timeframe = "Günlük"

print(f"--- HASSAS TARAMA BAŞLADI (Hızlı Mod) ---")

start_total = time.time()
found_count = 0

for hisse in tickers:
    # 0. Değişkeni Sıfırla
    df = None
    sonuc = None
    
    try:
        # 1. Veri İndir
        df = manager.fetch_stock_data(hisse, interval='1d')
        if df is None: continue
        
        # 2. Analiz Et
        df_res = analyzer.resample_data(df, timeframe)
        detection_df = df_res.tail(500)
        indicators = analyzer.add_indicators(detection_df)
        patterns = analyzer.detect_classic_patterns(indicators, timeframe=timeframe)
        
        if patterns:
            best_p = patterns[0]
            # Sonuç Sözlüğünü Hazırla (Görselleştirme için gerekli tüm verilerle)
            sonuc = {
                'Hisse': hisse,
                'ticker': hisse,
                'pattern': best_p['name'],
                'Score': best_p['score'],
                'Points': best_p.get('Points'),
                'target': best_p.get('target', 0)
            }
            
            # Hesaplama
            cur_price = float(detection_df['Close'].iloc[-1])
            tgt = sonuc['target']
            pot = 0.0
            if cur_price > 0 and tgt > 0:
                pot = ((tgt - cur_price) / cur_price) * 100
                
            sonuc['Getiri Potansiyeli (%)'] = round(pot, 2)
            sonuc['Fiyat'] = cur_price

            
            print(f"✅ {hisse} BULUNDU! Puan: {sonuc['Score']}")
            
            # --- SIRALI İŞLEMLER ---
            # 1. Önce Sonucu Kaydet (CSV)
            sonuclari_kaydet(sonuc)
            
            # 2. Sonra (Eğer Açıksa) Grafiği Çiz (HENÜZ VERİ SİLİNMEDEN!)
            
            found_count += 1
            
    except Exception as e:
        # print(f"Hata ({hisse}): {e}")
        pass
    
    # 3. En Sonra Temizlik Yap
    df = None
    del df

print(f"\n--- TARAMA BİTTİ ({found_count} hisse bulundu) ---")
print(f"Süre: {time.time()-start_total:.2f}s")

