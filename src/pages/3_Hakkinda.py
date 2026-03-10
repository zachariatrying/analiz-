"""
🎓 ZACHAİRA — Eğitim & Hakkında
Teknik analiz formasyonları ve indikatör rehberi
"""
import streamlit as st
import pandas as pd

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SAYFA AYARLARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title="Hakkında — ZACHAİRA", page_icon="🎓", layout="wide")

# Premium CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 40%, #16213e 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 24px; margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    }
    .pattern-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 8px;
    }
    .pattern-type-bullish {
        display: inline-block; padding: 3px 10px; border-radius: 16px;
        font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px;
        background: rgba(74,222,128,0.15); color: #4ade80; border: 1px solid rgba(74,222,128,0.3);
    }
    .pattern-type-bearish {
        display: inline-block; padding: 3px 10px; border-radius: 16px;
        font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px;
        background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3);
    }
    .pattern-type-neutral {
        display: inline-block; padding: 3px 10px; border-radius: 16px;
        font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px;
        background: rgba(148,163,184,0.15); color: #94a3b8; border: 1px solid rgba(148,163,184,0.3);
    }
    .indicator-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(168,85,247,0.05) 100%);
        border-radius: 14px;
        border: 1px solid rgba(99,102,241,0.12);
        padding: 20px; margin-bottom: 12px;
    }
    hr { border-color: rgba(255,255,255,0.06) !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BAŞLIK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div style="text-align:center; padding:10px 0 24px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        🎓 Eğitim & Hakkında
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">Teknik analiz formasyonları ve indikatör rehberi</p>
</div>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TABS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab1, tab2, tab3 = st.tabs(["📐 Formasyonlar", "📊 İndikatörler", "ℹ️ Proje Hakkında"])

# ━━━━━━ TAB 1: FORMASYONLAR ━━━━━━
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    # TOBO
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <span style="font-size:2rem;">🔄</span>
            <div>
                <div class="pattern-title">TOBO — Ters Omuz Baş Omuz (Inverse Head & Shoulders)</div>
                <span class="pattern-type-bullish">YÜKSELIŞ (Bullish Reversal)</span>
            </div>
        </div>
        <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem;">
            Düşüş trendinin sonunda oluşan <strong style="color:#e2e8f0;">dip dönüş formasyonu</strong>dur. Üç ardışık dip noktasından oluşur:
            ortadaki dip (baş) en derin, iki yandaki dipler (omuzlar) daha sığdır.
        </p>
        <div style="background:rgba(0,0,0,0.3); border-radius:12px; padding:16px; margin:12px 0;">
            <p style="color:#818cf8; font-weight:600; margin-bottom:8px; font-size:0.85rem;">📐 Geometrik Yapı:</p>
            <p style="color:#94a3b8; font-size:0.85rem; line-height:1.8; margin:0;">
                <strong style="color:#e2e8f0;">Sol Omuz:</strong> İlk dip noktası — panik satışları ile yüksek hacim<br>
                <strong style="color:#e2e8f0;">Baş:</strong> En derin dip — düşük hacim (absorpsiyon)<br>
                <strong style="color:#e2e8f0;">Sağ Omuz:</strong> Sığ dip — satış baskısı azalır, düşük hacim<br>
                <strong style="color:#e2e8f0;">Boyun Çizgisi:</strong> Omuzların tepelerini birleştiren direnç — kırılma sinyali<br>
                <strong style="color:#4ade80;">Hedef:</strong> Baş → Boyun arası mesafe kadar yukarı
            </p>
        </div>
        <p style="color:#64748b; font-size:0.8rem;">
            ⚡ ZACHAİRA bu formasyonu ZigZag + Fibonacci oranlarıyla ve hacim profili doğrulamasıyla tespit eder.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # OBO
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <span style="font-size:2rem;">⚠️</span>
            <div>
                <div class="pattern-title">OBO — Omuz Baş Omuz (Head & Shoulders)</div>
                <span class="pattern-type-bearish">DÜŞÜŞ (Bearish Reversal)</span>
            </div>
        </div>
        <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem;">
            Yükseliş trendinin sonunda oluşan <strong style="color:#e2e8f0;">tepe dönüş formasyonu</strong>dur.
            TOBO'nun tam tersidir — üç ardışık tepe noktasından oluşur ve fiyatın düşeceğinin habercisidir.
        </p>
        <div style="background:rgba(0,0,0,0.3); border-radius:12px; padding:16px; margin:12px 0;">
            <p style="color:#818cf8; font-weight:600; margin-bottom:8px; font-size:0.85rem;">📐 Geometrik Yapı:</p>
            <p style="color:#94a3b8; font-size:0.85rem; line-height:1.8; margin:0;">
                <strong style="color:#e2e8f0;">Sol Omuz:</strong> İlk tepe noktası<br>
                <strong style="color:#e2e8f0;">Baş:</strong> En yüksek tepe<br>
                <strong style="color:#e2e8f0;">Sağ Omuz:</strong> Düşük tepe — alıcı gücü azaldı<br>
                <strong style="color:#f87171;">Hedef:</strong> Baş → Boyun arası mesafe kadar aşağı
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Cup & Handle
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <span style="font-size:2rem;">☕</span>
            <div>
                <div class="pattern-title">Fincan & Kulp (Cup and Handle)</div>
                <span class="pattern-type-bullish">YÜKSELIŞ (Bullish Continuation)</span>
            </div>
        </div>
        <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem;">
            William O'Neil tarafından keşfedilen bu formasyon, bir fincan şeklinde <strong style="color:#e2e8f0;">yuvarlak dip</strong> oluşturduktan
            sonra sağ tarafta küçük bir geri çekilme (kulp) ile tamamlanır. Güçlü yükseliş potansiyeliyle bilinir.
        </p>
        <div style="background:rgba(0,0,0,0.3); border-radius:12px; padding:16px; margin:12px 0;">
            <p style="color:#818cf8; font-weight:600; margin-bottom:8px; font-size:0.85rem;">📐 Anahtar Kriterler:</p>
            <p style="color:#94a3b8; font-size:0.85rem; line-height:1.8; margin:0;">
                ✅ Fincan derinliği: %12-33 arası ideal<br>
                ✅ Yuvarlak dip — V şeklinde olmamalı<br>
                ✅ Kulp geri çekilmesi: Fincan derinliğinin %50'sinden az<br>
                ✅ Kırılma noktasında artan hacim<br>
                <strong style="color:#4ade80;">Hedef:</strong> Fincan derinliği kadar yukarı
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bull Flag
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <span style="font-size:2rem;">🏁</span>
            <div>
                <div class="pattern-title">Boğa Bayrak (Bull Flag)</div>
                <span class="pattern-type-bullish">YÜKSELIŞ (Bullish Continuation)</span>
            </div>
        </div>
        <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem;">
            Güçlü bir yükselişin ardından <strong style="color:#e2e8f0;">kısa süreli konsolidasyon</strong> dönemi.
            Bayrak direği (sert yükseliş) + bayrak (hafif düşüş kanalı) yapısından oluşur.
        </p>
        <div style="background:rgba(0,0,0,0.3); border-radius:12px; padding:16px; margin:12px 0;">
            <p style="color:#94a3b8; font-size:0.85rem; line-height:1.8; margin:0;">
                <strong style="color:#e2e8f0;">Direk:</strong> Hızlı, yüksek hacimli yükseliş (%20+ ideal)<br>
                <strong style="color:#e2e8f0;">Bayrak:</strong> Aşağı yönlü paralel kanal, düşük hacim<br>
                <strong style="color:#4ade80;">Hedef:</strong> Direk uzunluğu kadar yukarı (Flagpole Rule)
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Flama
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <span style="font-size:2rem;">🔺</span>
            <div>
                <div class="pattern-title">Flama (Pennant)</div>
                <span class="pattern-type-bullish">YÜKSELIŞ (Bullish Continuation)</span>
            </div>
        </div>
        <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem;">
            Boğa bayrak formasyonunun bir varyasyonudur. Fark olarak bayraktan farklı olarak
            <strong style="color:#e2e8f0;">daralan üçgen</strong> şeklinde konsolidasyon gösterir. Kırılma yönü genellikle trend yönündedir.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # RSI Divergence
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <span style="font-size:2rem;">📉</span>
            <div>
                <div class="pattern-title">RSI Uyumsuzluk (RSI Divergence)</div>
                <span class="pattern-type-neutral">DÖNÜŞ SİNYALİ</span>
            </div>
        </div>
        <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem;">
            Fiyat ile RSI indikatörünün <strong style="color:#e2e8f0;">zıt yönde hareket etmesi</strong>.
            Trendin zayıfladığını ve potansiyel dönüşü gösterir.
        </p>
        <div style="background:rgba(0,0,0,0.3); border-radius:12px; padding:16px; margin:12px 0;">
            <p style="color:#94a3b8; font-size:0.85rem; line-height:1.8; margin:0;">
                <strong style="color:#4ade80;">Boğa Uyumsuzluğu:</strong> Fiyat düşerken RSI yükseliyor → Alım sinyali<br>
                <strong style="color:#f87171;">Ayı Uyumsuzluğu:</strong> Fiyat yükselirken RSI düşüyor → Satım sinyali<br>
                ⚡ En güçlü sinyaller RSI'ın aşırı bölgelerde (30 altı / 70 üstü) olduğunda oluşur.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mum Formasyonları
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <span style="font-size:2rem;">🕯️</span>
            <div>
                <div class="pattern-title">Mum Formasyonları (Candlestick Patterns)</div>
                <span class="pattern-type-neutral">DÖNÜŞ SİNYALLERİ</span>
            </div>
        </div>
        <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem;">
            Japon mum grafiklerindeki tek veya çift mum formasyonları. Son 2-3 barı analiz ederek
            <strong style="color:#e2e8f0;">kısa vadeli dönüş sinyalleri</strong> üretir.
        </p>
        <div style="background:rgba(0,0,0,0.3); border-radius:12px; padding:16px; margin:12px 0;">
            <p style="color:#94a3b8; font-size:0.85rem; line-height:1.8; margin:0;">
                <strong style="color:#e2e8f0;">Doji:</strong> Açılış ≈ Kapanış — Kararsızlık, potansiyel dönüş<br>
                <strong style="color:#e2e8f0;">Hammer:</strong> Uzun alt gölge — Dip bölgede alım tepesi<br>
                <strong style="color:#e2e8f0;">Engulfing:</strong> Yutan mum — Güçlü dönüş sinyali<br>
                <strong style="color:#e2e8f0;">Shooting Star:</strong> Uzun üst gölge — Tepe bölgede satım baskısı
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # High Tight Flag
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <span style="font-size:2rem;">🚀</span>
            <div>
                <div class="pattern-title">High Tight Flag (Roket Formasyonu)</div>
                <span class="pattern-type-bullish">YÜKSEK MOMENTUM</span>
            </div>
        </div>
        <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem;">
            Nadir görülen ama son derece güçlü bir formasyon. <strong style="color:#e2e8f0;">%90+ kazanç</strong> ardından
            %20'den az gevşeme. Tekrar kırılma yapması halinde yüksek potansiyel sunar.
        </p>
        <div style="background:rgba(0,0,0,0.3); border-radius:12px; padding:16px; margin:12px 0;">
            <p style="color:#94a3b8; font-size:0.85rem; line-height:1.8; margin:0;">
                <strong style="color:#e2e8f0;">Kriter 1:</strong> 40 bar içinde %90+ yükseliş (Direk)<br>
                <strong style="color:#e2e8f0;">Kriter 2:</strong> Konsolidasyonda %20'den az geri çekilme<br>
                <strong style="color:#e2e8f0;">Kriter 3:</strong> Sıkı konsolidasyon süresi<br>
                ⚡ Thomas Bulkowski araştırmasına göre en yüksek başarı oranına sahip formasyon
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━ TAB 2: İNDİKATÖRLER ━━━━━━
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    indicators = [
        {
            "icon": "📊",
            "name": "RSI (Relative Strength Index)",
            "desc": "Fiyatın aşırı alım veya aşırı satım bölgesinde olup olmadığını gösteren momentum osilatörüdür.",
            "details": [
                ("Periyot", "14 bar (standart)"),
                ("Aşırı Alım", "> 70 → Satış baskısı beklenir"),
                ("Aşırı Satım", "< 30 → Alım tepkisi beklenir"),
                ("Nötr Bölge", "30-70 arası — trend devam edebilir"),
            ],
            "formula": "RSI = 100 - (100 / (1 + RS)), RS = Ortalama Kazanç / Ortalama Kayıp",
        },
        {
            "icon": "📈",
            "name": "SMA (Simple Moving Average)",
            "desc": "Belirli bir dönemdeki kapanış fiyatlarının aritmetik ortalamasıdır. Trendin yönünü ve gücünü belirler.",
            "details": [
                ("SMA 20", "Kısa vadeli trend — 20 günlük ortalama"),
                ("SMA 50", "Orta vadeli trend — 50 günlük ortalama"),
                ("Altın Çapraz", "SMA 20 > SMA 50 → Yükseliş sinyali"),
                ("Ölüm Çaprazı", "SMA 20 < SMA 50 → Düşüş sinyali"),
            ],
            "formula": "SMA = (P₁ + P₂ + ... + Pₙ) / n",
        },
        {
            "icon": "⚡",
            "name": "ZigZag Algoritması",
            "desc": "Fiyat hareketlerindeki gürültüyü filtreleyerek önemli pivot noktalarını (tepeler ve dipler) tespit eder.",
            "details": [
                ("Yöntem", "Yüzde bazlı sapma ile kritik noktalar"),
                ("Sapma", "Varsayılan %3 — küçük dalgalanmalar filtrelenir"),
                ("Kullanım", "Formasyon tespitinin temel bileşeni"),
                ("Çıktı", "Tepe (High) ve Dip (Low) noktaları listesi"),
            ],
            "formula": "Sapma > %X olan noktalar pivot olarak işaretlenir",
        },
        {
            "icon": "🔒",
            "name": "Destek & Direnç Seviyeleri",
            "desc": "Fiyatın geçmişte tepki verdiği önemli seviyeler. Destek alım tepkisini, direnç satış baskısını temsil eder.",
            "details": [
                ("Tespit", "Lokal ekstremum noktaları (argrelextrema)"),
                ("Pencere", "10 bar (varsayılan)"),
                ("Destek (yeşil)", "Fiyatın sıçradığı alt seviyeler"),
                ("Direnç (kırmızı)", "Fiyatın geri döndüğü üst seviyeler"),
            ],
            "formula": "Scipy argrelextrema ile lokal min/max tespiti",
        },
        {
            "icon": "📐",
            "name": "Lineer Regresyon Kanalı (Fair Value)",
            "desc": "Fiyatın istatistiksel olarak 'adil değer' çevresindeki hareketini ölçer. Standart sapma bantları ile birlikte kullanılır.",
            "details": [
                ("Orta Çizgi", "Lineer regresyon doğrusu (best fit)"),
                ("Üst Bant", "Orta + 2σ → Aşırı değerli bölge"),
                ("Alt Bant", "Orta - 2σ → Ucuz bölge"),
                ("R²", "Regresyon uyum kalitesi (trend gücü)"),
            ],
            "formula": "y = mx + b ± kσ (k = standart sapma çarpanı)",
        },
        {
            "icon": "📊",
            "name": "Hacim Profili Analizi",
            "desc": "Formasyonun hacim ile doğrulanıp doğrulanmadığını kontrol eder. Gerçek kırılmalar yüksek hacimle desteklenir.",
            "details": [
                ("Yüksek Hacim", "Kırılma noktalarında beklenir"),
                ("Düşük Hacim", "Konsolidasyon dönemlerinde normal"),
                ("Hacim SMA", "20 periyotluk hacim ortalaması"),
                ("Doğrulama", "Kırılma hacmi > 1.5x ortalama → Güçlü sinyal"),
            ],
            "formula": "Hacim Oranı = Mevcut Hacim / SMA(20) hacim",
        },
    ]

    for ind in indicators:
        st.markdown(f"""
        <div class="glass-card">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                <span style="font-size:1.5rem;">{ind['icon']}</span>
                <div class="pattern-title" style="margin:0;">{ind['name']}</div>
            </div>
            <p style="color:#94a3b8; font-size:0.9rem; line-height:1.6; margin-bottom:12px;">{ind['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Details table
        details_df = pd.DataFrame(ind['details'], columns=["Parametre", "Açıklama"])
        st.dataframe(details_df, use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div style="background:rgba(99,102,241,0.08); border-radius:10px; padding:10px 16px; margin-bottom:20px;
            border-left: 3px solid #818cf8;">
            <span style="color:#818cf8; font-weight:600; font-size:0.8rem;">📐 Formül: </span>
            <code style="color:#c084fc; font-size:0.85rem;">{ind['formula']}</code>
        </div>
        """, unsafe_allow_html=True)


# ━━━━━━ TAB 3: PROJE HAKKINDA ━━━━━━
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
            <span style="font-size:2.5rem;">🦅</span>
            <div>
                <h2 style="color:#e2e8f0; margin:0; font-size:1.5rem;">ZACHAİRA</h2>
                <p style="color:#64748b; margin:0; font-size:0.85rem;">BIST Borsa Teknik Analiz Platformu</p>
            </div>
        </div>
        <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem;">
            ZACHAİRA, Borsa İstanbul (BIST) hisselerini otomatik olarak tarayan ve klasik teknik analiz
            formasyonlarını tespit eden bir platformdur. ZigZag algoritması, geometrik doğrulama ve hacim
            profili analizi kullanarak yatırımcılara potansiyel alım/satım fırsatlarını görselleştirir.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color:#e2e8f0; font-size:1.1rem; margin-bottom:12px;">🛠️ Teknoloji Stack</h3>
            <div style="color:#94a3b8; font-size:0.9rem; line-height:2;">
                • <strong style="color:#e2e8f0;">Python 3.10+</strong> — Ana programlama dili<br>
                • <strong style="color:#e2e8f0;">Streamlit</strong> — Web arayüzü framework<br>
                • <strong style="color:#e2e8f0;">Plotly</strong> — İnteraktif grafik kütüphanesi<br>
                • <strong style="color:#e2e8f0;">Pandas & NumPy</strong> — Veri işleme<br>
                • <strong style="color:#e2e8f0;">SciPy</strong> — Sinyal analizi<br>
                • <strong style="color:#e2e8f0;">yfinance</strong> — Piyasa verisi (ücretsiz)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color:#e2e8f0; font-size:1.1rem; margin-bottom:12px;">📊 Rakamlarla ZACHAİRA</h3>
            <div style="color:#94a3b8; font-size:0.9rem; line-height:2;">
                • <strong style="color:#818cf8;">8</strong> farklı formasyon tespiti<br>
                • <strong style="color:#818cf8;">6</strong> zaman dilimi desteği<br>
                • <strong style="color:#818cf8;">500+</strong> BIST hissesi tarama<br>
                • <strong style="color:#818cf8;">~2000</strong> satır analiz motoru<br>
                • <strong style="color:#818cf8;">10</strong> birim test dosyası<br>
                • <strong style="color:#818cf8;">100%</strong> ücretsiz veri kaynağı
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Algoritma Akışı
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:#e2e8f0; font-size:1.1rem; margin-bottom:16px;">⚙️ Algoritma Akışı</h3>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div style="text-align:center; flex:1; min-width:120px;">
                <div style="background:rgba(99,102,241,0.2); border-radius:12px; padding:16px; margin-bottom:8px;">
                    <div style="font-size:1.5rem;">📡</div>
                </div>
                <div style="color:#e2e8f0; font-size:0.8rem; font-weight:600;">1. Veri Çekme</div>
                <div style="color:#64748b; font-size:0.7rem;">yfinance OHLCV</div>
            </div>
            <div style="color:#475569; font-size:1.2rem;">→</div>
            <div style="text-align:center; flex:1; min-width:120px;">
                <div style="background:rgba(99,102,241,0.2); border-radius:12px; padding:16px; margin-bottom:8px;">
                    <div style="font-size:1.5rem;">📊</div>
                </div>
                <div style="color:#e2e8f0; font-size:0.8rem; font-weight:600;">2. İndikatörler</div>
                <div style="color:#64748b; font-size:0.7rem;">RSI, SMA, Volume</div>
            </div>
            <div style="color:#475569; font-size:1.2rem;">→</div>
            <div style="text-align:center; flex:1; min-width:120px;">
                <div style="background:rgba(99,102,241,0.2); border-radius:12px; padding:16px; margin-bottom:8px;">
                    <div style="font-size:1.5rem;">⚡</div>
                </div>
                <div style="color:#e2e8f0; font-size:0.8rem; font-weight:600;">3. ZigZag</div>
                <div style="color:#64748b; font-size:0.7rem;">Pivot noktaları</div>
            </div>
            <div style="color:#475569; font-size:1.2rem;">→</div>
            <div style="text-align:center; flex:1; min-width:120px;">
                <div style="background:rgba(99,102,241,0.2); border-radius:12px; padding:16px; margin-bottom:8px;">
                    <div style="font-size:1.5rem;">📐</div>
                </div>
                <div style="color:#e2e8f0; font-size:0.8rem; font-weight:600;">4. Formasyon</div>
                <div style="color:#64748b; font-size:0.7rem;">Geometrik eşleşme</div>
            </div>
            <div style="color:#475569; font-size:1.2rem;">→</div>
            <div style="text-align:center; flex:1; min-width:120px;">
                <div style="background:rgba(74,222,128,0.2); border-radius:12px; padding:16px; margin-bottom:8px;">
                    <div style="font-size:1.5rem;">🎯</div>
                </div>
                <div style="color:#e2e8f0; font-size:0.8rem; font-weight:600;">5. Skor & Hedef</div>
                <div style="color:#64748b; font-size:0.7rem;">Sonuç raporu</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding:24px 0; color:#475569; font-size:0.8rem;">
        ⚠️ Bu uygulama eğitim amaçlı geliştirilmiştir. Yatırım tavsiyesi değildir.
    </div>
    """, unsafe_allow_html=True)
