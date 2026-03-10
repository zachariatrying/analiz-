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

<div align="center">
  <h1 align="center">BIST Teknik Analiz Platformu</h1>
  <p align="center"><strong>Ibrahim Tatar Analiz</strong></p>
  <p align="center">
    Borsa İstanbul (BIST) hisseleri için gelişmiş teknik analiz ve backtesting aracı.
  </p>
</div>

<hr>

## 📌 Proje Özeti

**BIST Teknik Analiz Platformu**, BIST (Borsa İstanbul) hisselerini otomatik olarak tarayan ve klasik teknik analiz formasyonlarını tespit eden bir yapay zeka destekli analiz platformudur. Uygulama lokalinizde veya bulutta anlık olarak çalışır; yüzlerce hisseyi dakikalar içinde analiz eder.

Premium arayüzü, akıllı bildirim sistemi ve backtest altyapısı ile profesyonel bir borsa asistanı görevi görür.

## ✨ Temel Özellikler

- **Gelişmiş Tarayıcı (Scanner)**: BIST hisselerinde TOBO, OBO, Fincan-Kulp, Boğa Bayrak, Flama, RSI Uyumsuzlukları ve Mum Formasyonlarını tespit eder.
- **Premium Dashboard**: Cam efekti (glassmorphism) ve modern koyu tema ile şık bir kullanıcı deneyimi.
- **Modüler Yapı**: Kod tabanı Dashboard, Tarayıcı, Haberler, Portföy Takip, Backtesting gibi çok sayfalık (Multi-page) Streamlit yapısına taşınmıştır.
- **Akıllı Backtesting**: Geçmiş formasyonların başarı oranlarını hesaplar. Seçilen formasyonlar için "Hedefe Ulaştı" veya "Stop Oldu" istatistiklerini raporlar.
- **Portföy Yönetimi**: Kendi portföyünüzü ekleyip, hisselerinizin maliyet ve kâr/zarar durumunu canlı olarak grafiklerle takip edebilirsiniz.
- **Canlı Piyasa Haberleri**: Seçili hisselere veya genel BIST piyasasına ait finansal haberleri otomatik çeker ve pozitif/negatif duygu analizi (Sentiment Analysis) yapar.
- **Telegram Entegrasyonu**: Özel alarmlarınızı veya tarama sonuçlarınızı anlık olarak Telegram botunuz üzerinden telefonunuza gönderir. (Ayarlar kalıcı olarak kaydedilir).

## 🚀 Kurulum

### 1. Python Sürümü

Bu proje **Python 3.10+** sürümleriyle uyumludur.

### 2. Gerekli Kütüphaneler

Repoyu klonladıktan sonra bağımlılıkları yükleyin:

```bash
git clone https://github.com/KULLANICI_ADINIZ/analiz.git
cd analiz
```

```bash
pip install -r requirements.txt
```

### 3. Ortam Değişkenleri (Opsiyonel)

Projedeki bazı özellikler API anahtarları gerektirebilir. Proje kök dizinine `.env` veya Streamlit Secrets (`.streamlit/secrets.toml`) dosyası açarak gerekli anahtarları tanımlayabilirsiniz. Telegram bilgileri arayüz üzerinden de girilip cihazda kalıcı olarak saklanabilmektedir.

## 💻 Kullanım

Uygulamayı başlatmak için ana klasördeyken şu komutu çalıştırın:

```bash
python -m streamlit run src/app.py
```

Tarayıcınızda otomatik olarak **<http://localhost:8501>** adresinde BIST Teknik Analiz Platformu açılacaktır.

### Klasör Yapısı

```
analiz/
├── src/
│   ├── app.py                       # Ana Streamlit uygulaması ve karşılama ekranı
│   ├── analyzer.py                  # Formasyon tespiti ve teknik analiz algoritmaları
│   ├── yf_utils.py                  # Yahoo Finance veri çekme işlemleri
│   └── pages/                       # Çoklu sayfa (Multi-page) modülleri
│       ├── 1_Dashboard.py           # Genel piyasa özeti ve BIST endeksleri
│       ├── 2_Tarayici.py            # Otomatik formasyon tarama motoru
│       ├── 3_Hakkinda.py            # Kullanım kılavuzu ve proje hakkında
│       ├── 4_Sektorler.py           # Sektörel performans izleme
│       ├── 5_Bist30_Kiyaslama.py    # Göreceli Güç (RS) analizi
│       ├── 6_Backtesting.py         # Geçmiş formasyonların performans testi
│       ├── 7_Portfoy.py             # Portföy ve kâr/zarar takibi
│       ├── 8_Telegram.py            # Telegram bot bildirim ayarları
│       └── 9_Haberler.py            # Haber akışı ve yapay zeka duygu analizi
├── requirements.txt
└── README.md
```

---

<p align="center">
  <strong>🦅 ZACHAİRA</strong> — Borsa İstanbul Teknik Analiz Platformu
</p>

