"""
Egitim ve Hakkinda
Teknik analiz formasyonlari ve indikator rehberi
"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hakkinda", page_icon="", layout="wide")

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
    .pattern-title { font-size: 1.15rem; font-weight: 700; color: #e2e8f0; margin-bottom: 8px; }
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
    hr { border-color: rgba(255,255,255,0.06) !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:10px 0 24px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        Egitim ve Hakkinda
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">Teknik analiz formasyonlari ve indikator rehberi</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Formasyonlar", "Indikatorler", "Proje Hakkinda"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    patterns = [
        ("TOBO -- Ters Omuz Bas Omuz (Inverse Head and Shoulders)", "YUKSELIS (Bullish Reversal)", "bullish",
         "Dusus trendinin sonunda olusan dip donus formasyonudur. Uc ardisik dip noktasindan olusur: ortadaki dip (bas) en derin, iki yandaki dipler (omuzlar) daha sigdir.",
         [("Sol Omuz", "Ilk dip noktasi -- panik satislari ile yuksek hacim"),
          ("Bas", "En derin dip -- dusuk hacim (absorpsiyon)"),
          ("Sag Omuz", "Sig dip -- satis baskisi azalir, dusuk hacim"),
          ("Boyun Cizgisi", "Omuzlarin tepelerini birlestiren direnc -- kirilma sinyali"),
          ("Hedef", "Bas - Boyun arasi mesafe kadar yukari")]),

        ("OBO -- Omuz Bas Omuz (Head and Shoulders)", "DUSUS (Bearish Reversal)", "bearish",
         "Yukselis trendinin sonunda olusan tepe donus formasyonudur. TOBO nun tam tersidir -- uc ardisik tepe noktasindan olusur.",
         [("Sol Omuz", "Ilk tepe noktasi"),
          ("Bas", "En yuksek tepe"),
          ("Sag Omuz", "Dusuk tepe -- alici gucu azaldi"),
          ("Hedef", "Bas - Boyun arasi mesafe kadar asagi")]),

        ("Fincan ve Kulp (Cup and Handle)", "YUKSELIS (Bullish Continuation)", "bullish",
         "William O Neil tarafindan kesfedilen bu formasyon, bir fincan seklinde yuvarlak dip olusturduktan sonra sag tarafta kucuk bir geri cekilme (kulp) ile tamamlanir.",
         [("Fincan derinligi", "%12-33 arasi ideal"),
          ("Yuvarlak dip", "V seklinde olmamali"),
          ("Kulp geri cekilmesi", "Fincan derinliginin %50 sinden az"),
          ("Kirilma noktasi", "Artan hacim gerekli"),
          ("Hedef", "Fincan derinligi kadar yukari")]),

        ("Boga Bayrak (Bull Flag)", "YUKSELIS (Bullish Continuation)", "bullish",
         "Guclu bir yukselisin ardindan kisa sureli konsolidasyon donemi. Bayrak diregi (sert yukselis) + bayrak (hafif dusus kanali) yapisindan olusur.",
         [("Direk", "Hizli, yuksek hacimli yukselis (%20+ ideal)"),
          ("Bayrak", "Asagi yonlu paralel kanal, dusuk hacim"),
          ("Hedef", "Direk uzunlugu kadar yukari (Flagpole Rule)")]),

        ("Flama (Pennant)", "YUKSELIS (Bullish Continuation)", "bullish",
         "Boga bayrak formasyonunun bir varyasyonudur. Bayraktan farkli olarak daralan ucgen seklinde konsolidasyon gosterir.",
         []),

        ("RSI Uyumsuzluk (RSI Divergence)", "DONUS SINYALI", "neutral",
         "Fiyat ile RSI indikatorunun zit yonde hareket etmesi. Trendin zayifladigini ve potansiyel donusu gosterir.",
         [("Boga Uyumsuzlugu", "Fiyat duserken RSI yukseliyor -- Alim sinyali"),
          ("Ayi Uyumsuzlugu", "Fiyat yukselirken RSI dusuyor -- Satim sinyali"),
          ("En guclu sinyaller", "RSI nin asiri bolgelerde (30 alti / 70 ustu) oldugu durumlar")]),

        ("Mum Formasyonlari (Candlestick Patterns)", "DONUS SINYALLERI", "neutral",
         "Japon mum grafiklerindeki tek veya cift mum formasyonlari. Son 2-3 bari analiz ederek kisa vadeli donus sinyalleri uretir.",
         [("Doji", "Acilis = Kapanis -- Kararsizlik, potansiyel donus"),
          ("Hammer", "Uzun alt golge -- Dip bolgede alim tepesi"),
          ("Engulfing", "Yutan mum -- Guclu donus sinyali"),
          ("Shooting Star", "Uzun ust golge -- Tepe bolgede satim baskisi")]),

        ("High Tight Flag (Roket Formasyonu)", "YUKSEK MOMENTUM", "bullish",
         "Nadir gorulen ama son derece guclu bir formasyon. %90+ kazanc ardindan %20 den az gevseme.",
         [("Kriter 1", "40 bar icinde %90+ yukselis (Direk)"),
          ("Kriter 2", "Konsolidasyonda %20 den az geri cekilme"),
          ("Kriter 3", "Siki konsolidasyon suresi"),
          ("Kaynak", "Thomas Bulkowski arastirmasina gore en yuksek basari oranina sahip formasyon")]),
    ]

    for name, ptype, pclass, desc, details in patterns:
        st.markdown(f"""
        <div class="glass-card">
            <div class="pattern-title">{name}</div>
            <span class="pattern-type-{pclass}">{ptype}</span>
            <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem; margin-top:12px;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        if details:
            details_df = pd.DataFrame(details, columns=["Parametre", "Aciklama"])
            st.dataframe(details_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    indicators = [
        ("RSI (Relative Strength Index)",
         "Fiyatin asiri alim veya asiri satim bolgesinde olup olmadigini gosteren momentum osilatoru.",
         [("Periyot", "14 bar (standart)"), ("Asiri Alim", "> 70 - Satis baskisi beklenir"),
          ("Asiri Satim", "< 30 - Alim tepkisi beklenir"), ("Notr Bolge", "30-70 arasi")],
         "RSI = 100 - (100 / (1 + RS)), RS = Ortalama Kazanc / Ortalama Kayip"),

        ("SMA (Simple Moving Average)",
         "Belirli bir donemdeki kapanis fiyatlarinin aritmetik ortalamasidir.",
         [("SMA 20", "Kisa vadeli trend"), ("SMA 50", "Orta vadeli trend"),
          ("Altin Capraz", "SMA 20 > SMA 50 - Yukselis sinyali"),
          ("Olum Caprazi", "SMA 20 < SMA 50 - Dusus sinyali")],
         "SMA = (P1 + P2 + ... + Pn) / n"),

        ("ZigZag Algoritmasi",
         "Fiyat hareketlerindeki gurultuyu filtreleyerek onemli pivot noktalarini tespit eder.",
         [("Yontem", "Yuzde bazli sapma ile kritik noktalar"), ("Sapma", "Varsayilan %3"),
          ("Kullanim", "Formasyon tespitinin temel bileseni"), ("Cikti", "Tepe ve Dip noktalari listesi")],
         "Sapma > %X olan noktalar pivot olarak isaretlenir"),

        ("Destek ve Direnc Seviyeleri",
         "Fiyatin gecmiste tepki verdigi onemli seviyeler.",
         [("Tespit", "Lokal ekstremum noktalari (argrelextrema)"), ("Pencere", "10 bar (varsayilan)"),
          ("Destek", "Fiyatin sicradigi alt seviyeler"), ("Direnc", "Fiyatin geri dondugu ust seviyeler")],
         "Scipy argrelextrema ile lokal min/max tespiti"),

        ("Lineer Regresyon Kanali (Fair Value)",
         "Fiyatin istatistiksel olarak adil deger cevresindeki hareketini olcer.",
         [("Orta Cizgi", "Lineer regresyon dogrusu"), ("Ust Bant", "Orta + 2 sigma"),
          ("Alt Bant", "Orta - 2 sigma"), ("R2", "Regresyon uyum kalitesi")],
         "y = mx + b +/- k*sigma"),

        ("Hacim Profili Analizi",
         "Formasyonun hacim ile dogrulanip dogrulanmadigini kontrol eder.",
         [("Yuksek Hacim", "Kirilma noktalarinda beklenir"), ("Dusuk Hacim", "Konsolidasyon donemlerinde normal"),
          ("Hacim SMA", "20 periyotluk hacim ortalamasi"), ("Dogrulama", "Kirilma hacmi > 1.5x ortalama")],
         "Hacim Orani = Mevcut Hacim / SMA(20) hacim"),
    ]

    for name, desc, details, formula in indicators:
        st.markdown(f"""
        <div class="glass-card">
            <div class="pattern-title">{name}</div>
            <p style="color:#94a3b8; font-size:0.9rem; line-height:1.6;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        details_df = pd.DataFrame(details, columns=["Parametre", "Aciklama"])
        st.dataframe(details_df, use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div style="background:rgba(99,102,241,0.08); border-radius:10px; padding:10px 16px; margin-bottom:20px; border-left: 3px solid #818cf8;">
            <span style="color:#818cf8; font-weight:600; font-size:0.8rem;">Formul: </span>
            <code style="color:#c084fc; font-size:0.85rem;">{formula}</code>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h2 style="color:#e2e8f0; margin:0 0 8px 0; font-size:1.5rem;">BIST Teknik Analiz Platformu</h2>
        <p style="color:#94a3b8; line-height:1.7; font-size:0.9rem;">
            Borsa Istanbul (BIST) hisselerini otomatik olarak tarayan ve klasik teknik analiz
            formasyonlarini tespit eden bir platformdur. ZigZag algoritmasi, geometrik dogrulama ve hacim
            profili analizi kullanarak yatirimcilara potansiyel alim/satim firsatlarini gorsellestirir.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color:#e2e8f0; font-size:1.1rem; margin-bottom:12px;">Teknoloji Stack</h3>
            <div style="color:#94a3b8; font-size:0.9rem; line-height:2;">
                Python 3.10+ -- Ana programlama dili<br>
                Streamlit -- Web arayuzu framework<br>
                Plotly -- Interaktif grafik kutuphanesi<br>
                Pandas ve NumPy -- Veri isleme<br>
                SciPy -- Sinyal analizi<br>
                yfinance -- Piyasa verisi (ucretsiz)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color:#e2e8f0; font-size:1.1rem; margin-bottom:12px;">Rakamlarla</h3>
            <div style="color:#94a3b8; font-size:0.9rem; line-height:2;">
                <strong style="color:#818cf8;">8</strong> farkli formasyon tespiti<br>
                <strong style="color:#818cf8;">6</strong> zaman dilimi destegi<br>
                <strong style="color:#818cf8;">500+</strong> BIST hissesi tarama<br>
                <strong style="color:#818cf8;">~2000</strong> satir analiz motoru<br>
                <strong style="color:#818cf8;">10</strong> birim test dosyasi<br>
                <strong style="color:#818cf8;">100%</strong> ucretsiz veri kaynagi
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h3 style="color:#e2e8f0; font-size:1.1rem; margin-bottom:16px;">Algoritma Akisi</h3>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div style="text-align:center; flex:1; min-width:120px;">
                <div style="background:rgba(99,102,241,0.2); border-radius:12px; padding:16px; margin-bottom:8px;">
                    <div style="font-size:1.2rem; color:#818cf8; font-weight:700;">1</div>
                </div>
                <div style="color:#e2e8f0; font-size:0.8rem; font-weight:600;">Veri Cekme</div>
                <div style="color:#64748b; font-size:0.7rem;">yfinance OHLCV</div>
            </div>
            <div style="color:#475569; font-size:1.2rem;">-</div>
            <div style="text-align:center; flex:1; min-width:120px;">
                <div style="background:rgba(99,102,241,0.2); border-radius:12px; padding:16px; margin-bottom:8px;">
                    <div style="font-size:1.2rem; color:#818cf8; font-weight:700;">2</div>
                </div>
                <div style="color:#e2e8f0; font-size:0.8rem; font-weight:600;">Indikatorler</div>
                <div style="color:#64748b; font-size:0.7rem;">RSI, SMA, Volume</div>
            </div>
            <div style="color:#475569; font-size:1.2rem;">-</div>
            <div style="text-align:center; flex:1; min-width:120px;">
                <div style="background:rgba(99,102,241,0.2); border-radius:12px; padding:16px; margin-bottom:8px;">
                    <div style="font-size:1.2rem; color:#818cf8; font-weight:700;">3</div>
                </div>
                <div style="color:#e2e8f0; font-size:0.8rem; font-weight:600;">ZigZag</div>
                <div style="color:#64748b; font-size:0.7rem;">Pivot noktalari</div>
            </div>
            <div style="color:#475569; font-size:1.2rem;">-</div>
            <div style="text-align:center; flex:1; min-width:120px;">
                <div style="background:rgba(99,102,241,0.2); border-radius:12px; padding:16px; margin-bottom:8px;">
                    <div style="font-size:1.2rem; color:#818cf8; font-weight:700;">4</div>
                </div>
                <div style="color:#e2e8f0; font-size:0.8rem; font-weight:600;">Formasyon</div>
                <div style="color:#64748b; font-size:0.7rem;">Geometrik eslesme</div>
            </div>
            <div style="color:#475569; font-size:1.2rem;">-</div>
            <div style="text-align:center; flex:1; min-width:120px;">
                <div style="background:rgba(74,222,128,0.2); border-radius:12px; padding:16px; margin-bottom:8px;">
                    <div style="font-size:1.2rem; color:#4ade80; font-weight:700;">5</div>
                </div>
                <div style="color:#e2e8f0; font-size:0.8rem; font-weight:600;">Skor ve Hedef</div>
                <div style="color:#64748b; font-size:0.7rem;">Sonuc raporu</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding:24px 0; color:#475569; font-size:0.8rem;">
        Bu uygulama egitim amacli gelistirilmistir. Yatirim tavsiyesi degildir.
    </div>
    """, unsafe_allow_html=True)

