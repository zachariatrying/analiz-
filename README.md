# Analiz - Finansal Veri Takip ve Teknik Analiz Platformu

Bu proje, hisse senedi piyasalarında teknik analiz süreçlerini otomatize etmek, algoritmik formasyon tespiti yapmak ve çoklu zaman dilimlerinde gelişmiş veri görselleştirmesi sunmak amacıyla geliştirilmiştir.

Python (FastAPI) tabanlı ölçeklenebilir bir arka uç mimarisi ile Flutter tabanlı, platform bağımsız (Cross-platform) bir kullanıcı arayüzünü bir araya getirir.

## Temel Özellikler

Proje aşağıdaki teknik yetenekleri sunmaktadır:

* **Çoklu Zaman Dilimi Analizi:** 1 Saatlik (1h), 4 Saatlik (4h), Günlük (Daily), Haftalık (Weekly) ve Aylık (Monthly) periyotlarda veri işleme.
* **Otomatik Destek ve Direnç Hesaplama:** Fiyat hareketlerine duyarlı dinamik seviye tespiti.
* **İstatistiksel Trend Takibi:** Lineer Regresyon Kanalı (Linear Regression Channel) entegrasyonu.
* **Gelişmiş Formasyon Tarama:**
    * Boğa Bayrak (Bull Flag)
    * High Tight Flag
    * Fincan Kulp (Cup and Handle)
* **Dinamik Skorlama Motoru:** Teknik indikatörlere dayalı puanlama ve hedef fiyat belirleme algoritması.
* **İnteraktif Görselleştirme:** Kullanıcı etkileşimine açık detaylı grafik arayüzleri.

## Teknoloji Yığını

Uygulama modern yazılım mimarileri kullanılarak geliştirilmiştir.

### Backend (Sunucu Tarafı)
* **Dil:** Python
* **API Framework:** FastAPI
* **Veri Sağlayıcılar:** TradingView (tvDatafeed), yfinance
* **Analitik Kütüphaneler:** Pandas, NumPy, TA-Lib

### Frontend (İstemci Tarafı)
* **Framework:** Flutter
* **Desteklenen Platformlar:** iOS, Android, Web, Windows/macOS/Linux
* **Grafik Motoru:** Plotly / Chart.js

## Kurulum ve Çalıştırma

Projeyi yerel ortamınıza kurmak için aşağıdaki adımları izleyin.

### Gereksinimler
* Python 3.9+
* Flutter SDK
* Git

### 1. Projeyi Klonlama

Terminali açın ve projeyi yerel diskinize indirin.

git clone https://github.com/zachariatrying/analiz-.git
cd analiz-

### 2. Backend Yapılandırması

Backend dizinine geçiş yapın ve sanal ortamı kurun.

cd backend
python -m venv venv

Sanal ortamı aktif hale getirin (Windows).

venv\Scripts\activate

Gerekli bağımlılıkları yükleyin.

pip install -r requirements.txt

API sunucusunu başlatın.

uvicorn main:app --reload

### 3. Frontend Yapılandırması

Yeni bir terminal penceresinde proje ana dizinine dönün ve frontend klasörüne girin.

cd frontend

Gerekli paketleri indirin.

flutter pub get

Uygulamayı çalıştırın.

flutter run

## Kullanım Talimatları

1.  Backend servisinin aktif olduğundan emin olun (Varsayılan: `http://127.0.0.1:8000`).
2.  Mobil veya masaüstü arayüzü üzerinden hisse senedi sembolü (Örn: THYAO) girerek analiz başlatın.
3.  **Tarama Modülü** aracılığıyla aktif formasyonları listeleyin.

## Katkı Sağlama

Projeye katkıda bulunmak için lütfen bir "Pull Request" oluşturun veya tespit ettiğiniz hataları "Issues" bölümünden bildirin.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına göz atabilirsiniz.
