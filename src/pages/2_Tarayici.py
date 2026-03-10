"""
🔍 ZACHAİRA — Teknik Tarayıcı
BIST hisselerini seçilen formasyonlara göre otomatik tarar.
"""
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import argrelextrema
import sys, os

# ── Analyzer Import ──
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from analyzer import Analyzer

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SAYFA AYARLARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title="Tarayıcı — ZACHAİRA", page_icon="🔍", layout="wide")

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
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #e0e0e0; letter-spacing: 0.5px;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] .stTextArea label {
        color: #a0aec0 !important; font-weight: 500;
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
    .streamlit-expanderHeader {
        font-size: 1.1rem !important; font-weight: 600 !important;
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        color: #e2e8f0 !important; padding: 12px 16px !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: rgba(99,102,241,0.35) !important;
        background: rgba(99,102,241,0.06) !important;
    }
    div[data-testid="stMetricValue"] { color: #818cf8; font-family: 'Inter', monospace; font-weight: 700; }
    div[data-testid="stMetricLabel"] { color: #94a3b8; font-weight: 500; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: none !important; border-radius: 12px !important;
        font-weight: 600 !important; letter-spacing: 0.5px;
        padding: 10px 28px !important; transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
        transform: translateY(-1px) !important;
    }
    .stDataFrame { width: 100% !important; border-radius: 12px; overflow: hidden; }
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #a78bfa, #c084fc) !important;
        border-radius: 8px;
    }
    hr { border-color: rgba(255,255,255,0.06) !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ANALYZER MOTORU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_resource
def get_analyzer():
    """Analyzer motorunu oluştur ve cache'le."""
    return Analyzer()

analyzer_engine = get_analyzer()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HİSSE HAVUZU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TUM_HISSELER_STR = """
A1CAP, ACSEL, ADEL, ADESE, ADGYO, AEFES, AFYON, AGES, AGHOL, AGROT, AGYO, AHGAZ, AHSGY, AKBNK, AKCNS, AKENR, AKFGY, AKGRT, AKMGY, AKSA, AKSEN, AKSGY, AKSUE, AKYHO, ALARK, ALBRK, ALCAR, ALCTL, ALFAS, ALGYO, ALKA, ALKIM, ALMAD, ALTNY, ANELE, ANGEN, ANHYT, ANSGR, ARASE, ARCLK, ARDYZ, ARENA, ARSAN, ARZUM, ASELS, ASGYO, ASTOR, ASUZU, ATAKP, ATATP, ATEKS, ATLAS, ATPSY, AVGYO, AVHOL, AVOD, AVTUR, AYCES, AYDEM, AYEN, AYES, AYGAZ, AZTEK, BAGFS, BAKAB, BALAT, BANVT, BARMA, BASCM, BASGZ, BAYRK, BEGYO, BERA, BERK, BESLR, BEYAZ, BFREN, BIENY, BIGCH, BIMAS, BINBN, BINHO, BIOEN, BIZIM, BJKAS, BLCYT, BMSCH, BMSTL, BNTAS, BOBET, BORLS, BOSSA, BRISA, BRKO, BRKSN, BRKVY, BRLSM, BRMEN, BRSAN, BRYAT, BSOKE, BTCIM, BUCIM, BURCE, BURVA, BVSAN, BYDNR, CANTE, CASA, CATES, CCOLA, CELHA, CEMAS, CEMTS, CEOEM, CIMSA, CLEBI, CMBTN, CMENT, CONSE, COSMO, CRDFA, CRFSA, CUSAN, CVKMD, CWENE, DAGH, DAPGM, DARDL, DAREN, DENGE, DERHL, DERIM, DESA, DESPC, DEVA, DGATE, DGGYO, DGNMO, DIRIT, DITAS, DMSAS, DNISI, DOAS, DOBUR, DOGUB, DOHOL, DOKTA, DOYLE, DURDO, DYOBY, DZGYO, EBEBK, ECILC, ECZYT, EDATA, EDIP, EGEEN, EGGUB, EGPRO, EGSER, EKGYO, EKIZ, EKSUN, ELITE, EMNIS, ENJSA, ENKAI, ENSRI, ENTRA, EPLAS, EREGL, ERSU, ESCAR, ESCOM, ESEN, ETILR, ETYAT, EUHOL, EUREN, EUYO, FADE, FENER, FLAP, FMIZP, FONET, FORMT, FORTE, FRIGO, FROTO, FZLGY, GARAN, GARFA, GEDIK, GEDZA, GENTS, GEREL, GERSAN, GESAN, GGLO, GIPTA, GLBMD, GLRYH, GLYHO, GMTAS, GOKNR, GOLTS, GOODY, GOZDE, GPNTP, GRNYO, GRSEL, GSDDE, GSDHO, GUBRF, GUNDG, GWIND, GZNMI, HALKB, HATEK, HATSN, HDFGS, HEDEF, HEKTS, HKTM, HLGYO, HRKET, HTTBT, HUBVC, HUNER, HURGZ, ICBCT, IDEAS, IDGYO, IEYHO, IHEVA, IHGZT, IHLAS, IHLGM, IHYAY, IMASM, INDES, INFO, INGRM, INTEM, INVEO, INVES, IPEKE, ISATR, ISBIR, ISBTR, ISCTR, ISDMR, ISFIN, ISGSY, ISGYO, ISKPL, ISKUR, ISMEN, ISSEN, ISYAT, IZFAS, IZMDC, IZENR, JANTS, KAPLM, KAREL, KARSN, KARTN, KARYE, KATMR, KAYSE, KBORU, KCAER, KCHOL, KENT, KERVN, KERVT, KFEIN, KGYO, KILIZ, KIMMR, KLGYO, KLKIM, KLMSN, KLNMA, KLRHO, KLSYN, KMPUR, KNFRT, KOCMT, KONKA, KONTR, KONYA, KOPOL, KORDS, KOTON, KOZAL, KOZAA, KRGYO, KRONT, KRPLS, KRSTL, KRTEK, KRVGD, KSTUR, KTLEV, KTSKR, KUTPO, KUVVA, KUYAS, KZBGY, KZGYO, LIDER, LIDFA, LILAK, LINK, LKMNH, LMKDC, LOGO, LUKSK, MAALT, MACKO, MAGEN, MAKIM, MAKTK, MANAS, MARBL, MARKA, MARTI, MAVI, MEDTR, MEGAP, MEKAG, MENTD, MEPET, MERCN, MERIT, MERKO, METRO, METUR, MGROS, MIATK, MHRGY, MIPAZ, MKRS, MNDRS, MOBTL, MPARK, MRGYO, MRSHL, MSGYO, MTRKS, MTRYO, MZHLD, NATEN, NETAS, NIBAS, NTGAZ, NTHOL, NUGYO, NUHCM, OBAMS, OBAS, ODAS, ODINE, OFSYM, ONCSM, ORCAY, ORGE, ORMA, OSMEN, OSTIM, OTKAR, OYAKC, OYLUM, OYOYO, OZGYO, OZKGY, OZRDN, OZSUB, PAGYO, PAMEL, PARSN, PASEU, PATEK, PCILT, PEGYO, PEKGY, PENGD, PENTA, PETKM, PETUN, PGSUS, PINSU, PKART, PKENT, PLAT, PNLSN, PNSUT, POLHO, POLTK, PRDGS, PRKAB, PRKME, PRZMA, PSDTC, PSGYO, QNBFB, QUAGR, RALYH, RAYSG, REEDR, RGYAS, RNPOL, RODRG, ROYAL, RTALB, RUBNS, RYGYO, RYSAS, SAFKR, SAHOL, SAMAT, SANEL, SANFM, SANKO, SARKY, SASA, SAYAS, SDTTR, SEGYO, SEKFK, SEKUR, SELEC, SELGD, SELVA, SEYKM, SILVR, SISE, SKBNK, SKTAS, SMART, SMRTG, SNAI, SNICA, SNPAM, SODSN, SOKE, SOKM, SONME, SRVGY, SUMAS, SUNGW, SURGY, SUWEN, TABGD, TARKM, TATGD, TAVHL, TBORG, TCELL, TDGYO, TEKTU, TERRA, TGSAS, THYAO, TKFEN, TKNSA, TLMAN, TMPOL, TMSN, TNZTP, TOASO, TRCAS, TRGYO, TRILC, TSKB, TSPOR, TTKOM, TTRAK, TUCLK, TUKAS, TUPRS, TUREX, TURGG, TURSG, UFUK, ULAS, ULKER, ULUFA, ULUSE, ULUUN, UMPAS, UNLU, USAK, UZERB, VAKBN, VAKFN, VAKKO, VANGD, VBTYZ, VERUS, VESBE, VESTL, VKFYO, VKGYO, VKING, VRGYO, YAPRK, YATAS, YAYLA, YBTAS, YEOTK, YESIL, YGGYO, YGYO, YKBNK, YKSLN, YONGA, YUNSA, YYAPI, YYLGD, ZEDUR, ZOREN, ZRGYO
"""

BIST30 = "AKBNK,ARCLK,ASELS,ASTOR,BIMAS,BRSAN,EKGYO,ENKAI,EREGL,FROTO,GARAN,GUBRF,HEKTS,ISCTR,KCHOL,KONTR,KOZAL,KRDMD,ODAS,OYAKC,PETKM,PGSUS,SAHOL,SASA,SISE,TCELL,THYAO,TOASO,TUPRS,YKBNK".split(',')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FORMASYON HARİTASI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMASYON_MAP = {
    "TOBO (Ters Omuz Baş Omuz)": "tobo",
    "OBO (Omuz Baş Omuz)": "obo",
    "Fincan Kulp": "cup",
    "Boğa Bayrak": "flag",
    "Flama": "flama",
    "High Tight Flag 🚀": "rocket",
    "RSI Uyumsuzluk": "rsi_div",
    "Mum Formasyonları": "candle",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  VERİ MOTORU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data(ttl=300)
def veri_getir(hisse: str, bar_sayisi: int, interval: str, period: str, resample_rule: str = None) -> pd.DataFrame | None:
    """
    yfinance üzerinden hisse verisi çeker, indikatörleri hesaplar.

    Args:
        hisse: Hisse kodu (örn: THYAO)
        bar_sayisi: Gösterilecek bar sayısı
        interval: yfinance interval (1d, 1wk, 60m vb.)
        period: yfinance period (2y, 5y, max vb.)
        resample_rule: Yeniden örnekleme kuralı (4h, 2h vb.)

    Returns:
        DataFrame veya None
    """
    try:
        symbol = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        try:
            df = yf.download(symbol, period=period, interval=interval, progress=False)
        except:
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.rename(columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close', 'Volume':'Volume'})

        if df.empty or len(df) < 20:
            return None

        # Yeniden Örnekleme
        if resample_rule:
            agg_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}
            df = df.resample(resample_rule).agg(agg_dict).dropna()

        # Hareketli Ortalamalar
        df['SMA20'] = df['Close'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()

        # RSI
        delta = df['Close'].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        gain = up.rolling(window=14).mean()
        loss = down.rolling(window=14).mean()
        loss = loss.replace(0, 0.0001)
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        return df.tail(bar_sayisi)
    except:
        return None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GRAFİK MOTORU (Volume Subplot eklendi)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def grafik_ciz(df: pd.DataFrame, hisse: str, veri: dict) -> go.Figure:
    """İnteraktif Plotly grafiği oluşturur (mumlar + volume)."""

    # Volume subplot ile birleşik grafik
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25]
    )

    # ── Mumlar ──
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name='Fiyat',
        increasing_line_color='#4ade80', decreasing_line_color='#f87171',
        increasing_fillcolor='rgba(74,222,128,0.3)', decreasing_fillcolor='rgba(248,113,113,0.3)',
    ), row=1, col=1)

    # ── SMA Çizgileri ──
    fig.add_trace(go.Scatter(
        x=df.index, y=df['SMA20'],
        line=dict(color='#fbbf24', width=1.2), name='SMA 20', opacity=0.8
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df['SMA50'],
        line=dict(color='#38bdf8', width=1.2), name='SMA 50', opacity=0.8
    ), row=1, col=1)

    # ── Teknik Seviyeler ──
    if 'Tech' in veri:
        try:
            fig.add_trace(go.Scatter(x=df.index, y=veri['Tech']['Upper'],
                line=dict(color='rgba(148,163,184,0.4)', width=1, dash='dot'),
                name='Kanal Üst', visible='legendonly'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=veri['Tech']['Lower'],
                line=dict(color='rgba(148,163,184,0.4)', width=1, dash='dot'),
                name='Kanal Alt', visible='legendonly'), row=1, col=1)
            for res in veri['Tech']['Resistances'][-2:]:
                fig.add_hline(y=res, line_dash="dot", line_color="rgba(248,113,113,0.5)", line_width=1, row=1, col=1)
            for sup in veri['Tech']['Supports'][-2:]:
                fig.add_hline(y=sup, line_dash="dot", line_color="rgba(74,222,128,0.5)", line_width=1, row=1, col=1)
        except:
            pass

    # ── Hedef & Stop ──
    fig.add_hline(y=veri['Hedef'], line_color="#4ade80", line_width=2,
        annotation_text=f"HEDEF: {veri['Hedef']:.2f}",
        annotation_position="top left",
        annotation_font_color="#4ade80",
        annotation_font_size=11,
        row=1, col=1)

    if veri.get('Stop'):
        fig.add_hline(y=veri['Stop'], line_color="#f87171", line_width=2, line_dash="dash",
            annotation_text=f"STOP: {veri['Stop']:.2f}",
            annotation_position="bottom left",
            annotation_font_color="#f87171",
            annotation_font_size=11,
            row=1, col=1)

    # ── Noktalar ──
    if 'Points' in veri and veri['Points']:
        pts = veri['Points']
        try:
            if 't_start' in pts:
                fig.add_trace(go.Scatter(
                    x=[pts['t_start'], pts['t_peak'], pts['t_break']],
                    y=[pts['p_start'], pts['p_peak'], pts['p_break']],
                    mode='markers',
                    marker=dict(size=[10, 10, 15], color=['#4ade80', '#f87171', '#fbbf24'], symbol=['circle', 'circle', 'star']),
                    name='Noktalar'
                ), row=1, col=1)
        except:
            pass

    # ── Volume ──
    if 'Volume' in df.columns:
        colors = ['rgba(74,222,128,0.5)' if c >= o else 'rgba(248,113,113,0.5)'
                  for c, o in zip(df['Close'], df['Open'])]
        fig.add_trace(go.Bar(
            x=df.index, y=df['Volume'], name='Hacim',
            marker_color=colors, opacity=0.7,
            showlegend=False
        ), row=2, col=1)

    # ── Layout ──
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=520,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(color='#94a3b8', size=10),
            bgcolor='rgba(0,0,0,0)'
        ),
        font=dict(color='#94a3b8'),
        xaxis2=dict(gridcolor='rgba(128,128,128,0.08)'),
        yaxis=dict(gridcolor='rgba(128,128,128,0.08)', title=''),
        yaxis2=dict(gridcolor='rgba(128,128,128,0.08)', title=''),
    )
    fig.update_xaxes(rangeslider_visible=False)

    return fig

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ANALİZ MOTORU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def analiz_yap(df: pd.DataFrame, secilen_formasyonlar: list, tolerans: int,
               zaman_etiketi: str, tek_hisse_modu: bool = False) -> list:
    """
    Verilen DataFrame üzerinde seçilen formasyonları tarar.

    Args:
        df: Hisse verisi
        secilen_formasyonlar: Kullanıcının seçtiği formasyonlar
        tolerans: Tarama hassasiyeti
        zaman_etiketi: Zaman dilimi etiketi
        tek_hisse_modu: Tek hisse modunda ise boş dönmesin

    Returns:
        Bulunan formasyon sonuçlarının listesi
    """
    if len(df) < 50:
        return []
    son = df.iloc[-1]

    # İndikatörleri Ekle
    try:
        df_work = df.copy()
        if 'Date' not in df_work.columns:
            df_work['Date'] = df_work.index
        df_ind = analyzer_engine.add_indicators(df_work)
    except:
        df_ind = df.copy()
        if 'Date' not in df_ind.columns:
            df_ind['Date'] = df_ind.index

    # Pattern Config
    analyzer_engine.config['enabled_patterns'] = {
        'tobo': "TOBO (Ters Omuz Baş Omuz)" in secilen_formasyonlar,
        'obo': "OBO (Omuz Baş Omuz)" in secilen_formasyonlar,
        'cup': "Fincan Kulp" in secilen_formasyonlar,
        'flag': "Boğa Bayrak" in secilen_formasyonlar,
        'flama': "Flama" in secilen_formasyonlar,
        'breakout': False,
    }

    sonuclar = []

    try:
        tf_map = {"GÜNLÜK": "Günlük", "HAFTALIK": "Haftalık", "AYLIK": "Aylık",
                  "1 SAAT": "Saatlik", "2 SAAT": "Saatlik", "4 SAAT": "Saatlik"}
        tf = tf_map.get(zaman_etiketi, "Günlük")

        patterns = analyzer_engine.detect_classic_patterns(df_ind, timeframe=tf)

        # RSI Uyumsuzluk
        if "RSI Uyumsuzluk" in secilen_formasyonlar:
            try:
                zz = analyzer_engine.calculate_zigzag(df_ind)
                div_pats = analyzer_engine.detect_rsi_divergence(df_ind, zz, tf)
                patterns.extend(div_pats)
            except: pass

        # Mum Formasyonları
        if "Mum Formasyonları" in secilen_formasyonlar:
            try:
                candle_pats = analyzer_engine.detect_candlestick_patterns(df_ind, tf)
                patterns.extend(candle_pats)
            except: pass

        # High Tight Flag
        if "High Tight Flag 🚀" in secilen_formasyonlar:
            try:
                rocket_pats = analyzer_engine.detect_high_tight_flag(df_ind)
                patterns.extend(rocket_pats)
            except: pass

        for p in patterns:
            curr_price = float(son['Close'])
            target = float(p.get('target', curr_price * 1.05))
            if target <= curr_price:
                target = curr_price * 1.05
            potansiyel = ((target - curr_price) / curr_price) * 100

            sonuclar.append({
                "Formasyon": p.get('name', p.get('Formasyon', 'Bilinmeyen')),
                "Skor": min(p.get('score', 50), 100),
                "Hedef": target,
                "Stop": p.get('stop', curr_price * 0.95),
                "Potansiyel": potansiyel,
                "Fiyat": curr_price,
                "Periyot": zaman_etiketi,
                "Sinyal": p.get('signal', ''),
                "Durum": p.get('status', ''),
                "Kalite": p.get('quality', ''),
                "Strateji": p.get('strategy', p.get('desc', '')),
                "Vade": p.get('vade', ''),
                "Points": p.get('Points', {}),
            })

    except:
        pass

    # Tek hisse modunda boş dönmesin
    if not sonuclar and tek_hisse_modu:
        curr_price = float(son['Close'])
        skor = 50
        try:
            if son['Close'] > son['SMA20']: skor += 10
            if son['SMA20'] > son['SMA50']: skor += 10
            if 45 < son['RSI'] < 70: skor += 20
        except: pass

        sonuclar.append({
            "Formasyon": "Genel Teknik Görünüm",
            "Skor": min(skor, 100),
            "Hedef": curr_price * 1.05,
            "Stop": curr_price * 0.95,
            "Potansiyel": 5.0,
            "Fiyat": curr_price,
            "Periyot": zaman_etiketi,
            "Sinyal": "Nötr",
            "Durum": "",
            "Kalite": "",
            "Strateji": "Belirgin formasyon bulunamadı. Genel teknik görünüm sunuluyor.",
            "Vade": "",
            "Points": {},
        })

    return sonuclar

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SAYFA BAŞLIĞI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div style="text-align:center; padding:10px 0 20px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        🔍 Teknik Tarayıcı
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">BIST hisselerini seçilen formasyonlara göre otomatik tarayan analiz motoru</p>
</div>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SIDEBAR KONTROL PANELİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:10px 0 20px 0;">
        <div style="font-size:1.8rem;">🦅</div>
        <div style="color:#818cf8; font-weight:700; font-size:1.1rem; letter-spacing:1px;">ZACHAİRA</div>
        <div style="color:#475569; font-size:0.7rem; letter-spacing:2px;">TEKNİK ANALİZ MOTORU</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Periyot ──
    st.markdown("##### ⏱️ Zaman Dilimi")
    zaman_secimi = st.selectbox("Periyot", [
        "GÜNLÜK (1D)", "HAFTALIK (1W)", "AYLIK (1M)",
        "4 SAATLİK (4h)", "2 SAATLİK (2h)", "1 SAATLİK (1h)"
    ], label_visibility="collapsed")

    yf_res = None
    if "GÜNLÜK" in zaman_secimi: yf_int, yf_per, z_etiket = "1d", "2y", "GÜNLÜK"
    elif "HAFTALIK" in zaman_secimi: yf_int, yf_per, z_etiket = "1wk", "5y", "HAFTALIK"
    elif "AYLIK" in zaman_secimi: yf_int, yf_per, z_etiket = "1mo", "max", "AYLIK"
    elif "4 SAATLİK" in zaman_secimi: yf_int, yf_per, z_etiket, yf_res = "60m", "730d", "4 SAAT", "4h"
    elif "2 SAATLİK" in zaman_secimi: yf_int, yf_per, z_etiket, yf_res = "60m", "730d", "2 SAAT", "2h"
    else: yf_int, yf_per, z_etiket = "60m", "730d", "1 SAAT"

    st.divider()

    # ── Kaynak ──
    st.markdown("##### 📋 Hisse Kaynağı")
    liste_modu = st.radio("Kaynak", [
        "🎯 TEK HİSSE (Sniper)",
        "⭐ FAVORİLERİM",
        "📊 TÜM BIST",
        "🏆 BIST 30"
    ], label_visibility="collapsed")

    tek_hisse_aktif = False
    if "TEK HİSSE" in liste_modu:
        tek_hisse_input = st.text_input("Hisse kodu girin:", "THYAO", placeholder="Örn: THYAO")
        hisseler = [tek_hisse_input.upper().strip()]
        tek_hisse_aktif = True
    elif "FAVORİLERİM" in liste_modu:
        if 'fav_hisseler' not in st.session_state:
            st.session_state.fav_hisseler = "THYAO, GARAN, ASELS, AKBNK, SASA"
        user_list = st.text_area("Virgülle ayırın:", value=st.session_state.fav_hisseler)
        st.session_state.fav_hisseler = user_list
        hisseler = [h.strip() for h in user_list.split(',')]
    elif "TÜM BIST" in liste_modu:
        hisseler = [h.strip() for h in TUM_HISSELER_STR.replace('\n', '').split(',') if len(h) > 1]
    else:
        hisseler = BIST30

    st.divider()

    # ── Formasyonlar ──
    st.markdown("##### 🧩 Formasyonlar")
    secilen_formasyonlar = st.multiselect("Formasyonlar", [
        "TOBO (Ters Omuz Baş Omuz)",
        "OBO (Omuz Baş Omuz)",
        "Fincan Kulp",
        "Boğa Bayrak",
        "Flama",
        "High Tight Flag 🚀",
        "RSI Uyumsuzluk",
        "Mum Formasyonları",
    ], default=["TOBO (Ters Omuz Baş Omuz)", "Boğa Bayrak", "Fincan Kulp"],
    label_visibility="collapsed")

    st.divider()

    # ── Ayarlar ──
    st.markdown("##### ⚙️ Parametreler")
    bar_sayisi = st.slider("Grafik Derinliği (Bar)", 50, 300, 150)
    tolerans = st.slider("Tolerans", 1, 10, 3)

    st.markdown("<br>", unsafe_allow_html=True)
    btn_baslat = st.button("🚀 TARAMAYI BAŞLAT", type="primary", use_container_width=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SONUÇLAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if btn_baslat:
    temiz_hisseler = sorted(list(set([h.upper() for h in hisseler if len(h) > 1])))

    # Status Info
    st.markdown(f"""
    <div class="glass-card" style="text-align:center; padding:16px;">
        <span style="color:#818cf8; font-weight:600;">🔍 {len(temiz_hisseler)} hisse taranıyor</span>
        <span style="color:#475569;"> | </span>
        <span style="color:#94a3b8;">{z_etiket}</span>
        <span style="color:#475569;"> | </span>
        <span style="color:#94a3b8;">{', '.join(secilen_formasyonlar)}</span>
    </div>
    """, unsafe_allow_html=True)

    bar = st.progress(0)
    bulunanlar = []

    for i, hisse in enumerate(temiz_hisseler):
        bar.progress((i + 1) / len(temiz_hisseler))
        df = veri_getir(hisse, bar_sayisi, yf_int, yf_per, yf_res)
        if df is not None:
            sonuc_listesi = analiz_yap(df, secilen_formasyonlar, tolerans, z_etiket, tek_hisse_aktif)
            for sonuc in sonuc_listesi:
                sonuc['Hisse'] = hisse
                bulunanlar.append(sonuc)
    bar.empty()

    if not bulunanlar:
        if tek_hisse_aktif:
            st.error(f"❌ {temiz_hisseler[0]} için sonuç bulunamadı veya veri alınamadı.")
        else:
            st.warning("❌ Sonuç yok. Toleransı artırın veya daha fazla formasyon seçin.")
    else:
        # Success Message
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:12px;
            border-color:rgba(74,222,128,0.3); background:rgba(74,222,128,0.05);">
            <span style="color:#4ade80; font-weight:700; font-size:1.1rem;">
                🎉 {len(bulunanlar)} Sonuç Bulundu!
            </span>
        </div>
        """, unsafe_allow_html=True)

        # ── SONUÇ KARTLARI ──
        for idx_v, veri in enumerate(bulunanlar):
            f_name = veri['Formasyon']

            # İkon Seçimi
            if "Genel" in f_name: ikon = "📊"
            elif "TOBO" in f_name: ikon = "🔄"
            elif "OBO" in f_name: ikon = "⚠️"
            elif "Fincan" in f_name or "Cup" in f_name: ikon = "☕"
            elif "Roket" in f_name or "Rocket" in f_name or "HTF" in f_name: ikon = "🚀"
            elif "RSI" in f_name or "Divergence" in f_name: ikon = "📉"
            elif "Doji" in f_name or "Hammer" in f_name or "Engulf" in f_name: ikon = "🕯️"
            elif "Bayrak" in f_name or "Flag" in f_name: ikon = "🏁"
            elif "Flama" in f_name: ikon = "🔺"
            else: ikon = "✨"

            sinyal_renk = "🟢" if veri.get('Sinyal') == 'Bullish' else "🔴" if veri.get('Sinyal') == 'Bearish' else ""
            skor_renk = "score-high" if veri['Skor'] >= 70 else "score-mid" if veri['Skor'] >= 50 else "score-low"

            baslik = f"{ikon} {veri['Hisse']} | {f_name} {sinyal_renk} | Skor: {veri['Skor']} | Pot: %{veri['Potansiyel']:.1f}"

            with st.expander(baslik, expanded=True):
                # Grafik
                df_c = veri_getir(veri['Hisse'], bar_sayisi, yf_int, yf_per, yf_res)
                if df_c is not None:
                    fig = grafik_ciz(df_c, veri['Hisse'], veri)
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_{veri['Hisse']}_{idx_v}")

                # Metrikler
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("💰 Fiyat", f"{veri['Fiyat']:.2f}")
                c2.metric("🎯 Hedef", f"{veri['Hedef']:.2f}")
                c3.metric("🛑 Stop", f"{veri.get('Stop', 0):.2f}")
                c4.metric("⭐ Skor", f"{veri['Skor']}/100")

                # Strateji
                if veri.get('Strateji'):
                    st.info(f"💡 **Strateji:** {veri['Strateji']}")

                # Meta Bilgiler
                meta_parts = []
                if veri.get('Durum'): meta_parts.append(f"**Durum:** {veri['Durum']}")
                if veri.get('Kalite'): meta_parts.append(f"**Kalite:** {veri['Kalite']}")
                if veri.get('Vade'): meta_parts.append(f"**Vade:** {veri['Vade']}")
                if meta_parts:
                    st.caption(" | ".join(meta_parts))

                if "Genel" in veri['Formasyon']:
                    st.caption("⚠️ Formasyon bulunamadı, genel görünüm sunuluyor.")

        # ── ÖZET TABLO ──
        st.divider()
        st.markdown("### 📋 Özet Tablo")
        df_final = pd.DataFrame(bulunanlar)
        all_cols = ['Hisse', 'Fiyat', 'Formasyon', 'Sinyal', 'Periyot', 'Potansiyel', 'Hedef', 'Stop', 'Skor', 'Durum', 'Kalite', 'Vade']
        cols = [c for c in all_cols if c in df_final.columns]

        st.dataframe(
            df_final[cols],
            use_container_width=True,
            column_config={
                "Potansiyel": st.column_config.NumberColumn("Potansiyel %", format="%.1f%%"),
                "Fiyat": st.column_config.NumberColumn("Fiyat", format="%.2f"),
                "Hedef": st.column_config.NumberColumn("Hedef", format="%.2f"),
                "Stop": st.column_config.NumberColumn("Stop", format="%.2f"),
            }
        )

        # ── CSV EXPORT ──
        csv = df_final[cols].to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Sonuçları CSV olarak indir",
            data=csv,
            file_name="zachaira_tarama_sonuclari.csv",
            mime="text/csv",
        )
