<p align="center">
  <h1 align="center">🦅 ZACHAİRA</h1>
  <p align="center">
    <strong>BIST Borsa Teknik Analiz Platformu</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
    <img src="https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?logo=plotly&logoColor=white" alt="Plotly">
    <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  </p>
</p>

---

## 📖 Proje Hakkında

**ZACHAİRA**, BIST (Borsa İstanbul) hisselerini otomatik olarak tarayan ve klasik teknik analiz formasyonlarını tespit eden bir yapay zeka destekli analiz platformudur.

Uygulama, **ZigZag algoritması**, **geometrik doğrulama** ve **hacim profili analizi** kullanarak yatırımcılara potansiyel alım/satım fırsatlarını görselleştirir.

## ✨ Özellikler

### 🔍 Formasyon Tarama Motoru

- **TOBO** (Ters Omuz Baş Omuz) — Dip dönüş formasyonu
- **OBO** (Omuz Baş Omuz) — Tepe dönüş formasyonu
- **Fincan & Kulp** (Cup and Handle) — Devam formasyonu
- **Boğa Bayrak** (Bull Flag) — Trend devamı
- **Flama** (Pennant) — Daralan üçgen
- **High Tight Flag** 🚀 — Yüksek momentumlu bayrak
- **RSI Uyumsuzluk** (Divergence) — Fiyat-RSI çelişkisi
- **Mum Formasyonları** — Doji, Hammer, Engulfing

### 📊 Teknik İndikatörler

- **RSI** (Relative Strength Index)
- **SMA** 20/50 (Simple Moving Average)
- **ZigZag** — Trend noktaları belirleme
- **Destek / Direnç** seviyeleri
- **Lineer Regresyon Kanalı** (Fair Value)
- **Hacim Profili** analizi

### 🗺️ Piyasa Dashboard

- BIST30 / BIST100 endeks bilgisi
- Sektörel ısı haritası (Treemap)
- En çok yükselen / düşen hisseler
- Piyasa risk göstergesi

### 🎓 Eğitim Modülü

- Her formasyonun detaylı açıklaması
- Teknik indikatör rehberi
- Görsel örneklerle desteklenmiş açıklamalar

## 🛠️ Teknoloji Stack

| Teknoloji | Kullanım Alanı |
|-----------|---------------|
| **Python 3.10+** | Ana programlama dili |
| **Streamlit** | Web arayüzü |
| **Plotly** | İnteraktif grafikler |
| **Pandas / NumPy** | Veri işleme |
| **SciPy** | Sinyal analizi (ZigZag, Peak Detection) |
| **yfinance** | Piyasa verisi (ücretsiz) |

## 🚀 Kurulum

### 1. Repoyu Klonlayın

```bash
git clone https://github.com/KULLANICI_ADINIZ/zachaira.git
cd zachaira
```

### 2. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın

```bash
streamlit run src/app.py
```

Tarayıcınız otomatik olarak `http://localhost:8501` adresinde açılacaktır.

## 📁 Proje Yapısı

```
zachaira/
├── src/
│   ├── app.py              # Ana uygulama (Multi-page router)
│   ├── analyzer.py          # Teknik analiz motoru (~2000 satır)
│   ├── data_manager.py      # Veri yönetimi & cache
│   ├── macro_data.py        # Makroekonomik veri (FED/TCMB)
│   ├── earnings_data.py     # Bilanço tarihleri
│   ├── grok_client.py       # AI entegrasyonu
│   ├── bist_tickers.json    # BIST hisse listesi
│   └── pages/
│       ├── 1_Dashboard.py   # Piyasa genel bakış
│       ├── 2_Tarayici.py    # Formasyon tarayıcı
│       └── 3_Hakkinda.py    # Eğitim & bilgi
├── tests/                   # Birim testleri
├── requirements.txt
└── README.md
```

## 🧮 Algoritma

### ZigZag + Geometrik Doğrulama

1. **Veri Çekme** — yfinance üzerinden OHLCV verisi
2. **İndikatör Hesaplama** — RSI, SMA, Hacim ortalamaları
3. **ZigZag Hesaplama** — Yüzde bazlı sapma ile kritik noktalar
4. **Formasyon Eşleşme** — Geometrik kurallarla (oran, simetri, Fibonacci) formasyon tespiti
5. **Hacim Onayı** — Hacim profilinin formasyonu destekleyip desteklemediği
6. **Skor & Hedef** — Güvenilirlik skoru, hedef fiyat ve stop-loss hesaplama

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

<p align="center">
  <strong>🦅 ZACHAİRA</strong> — Borsa İstanbul Teknik Analiz Platformu
</p>
