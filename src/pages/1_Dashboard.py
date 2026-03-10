"""
📊 ZACHAİRA — Piyasa Dashboard
BIST endeks bilgisi, sektörel ısı haritası, en çok yükselen/düşen hisseler
"""
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SAYFA AYARLARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title="Dashboard — ZACHAİRA", page_icon="📊", layout="wide")

# Premium CSS (app.py ile aynı temayı uygula)
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
        padding: 24px;
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(168,85,247,0.08) 100%);
        border-radius: 14px;
        border: 1px solid rgba(99,102,241,0.15);
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(99,102,241,0.2); }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    .metric-delta-up { color: #4ade80; font-weight: 600; font-size: 0.9rem; }
    .metric-delta-down { color: #f87171; font-weight: 600; font-size: 0.9rem; }
    div[data-testid="stMetricValue"] { color: #818cf8; font-family: 'Inter', monospace; font-weight: 700; }
    .stProgress > div > div { background: linear-gradient(90deg, #6366f1, #a78bfa, #c084fc) !important; border-radius: 8px; }
    hr { border-color: rgba(255,255,255,0.06) !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SEKTÖR HARİTASI (Statik veri — API gerektirmez)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTOR_MAP = {
    "Bankacılık": ["AKBNK", "GARAN", "HALKB", "ISCTR", "VAKBN", "YKBNK", "SKBNK", "ALBRK", "QNBFB", "TSKB"],
    "Havacılık & Savunma": ["THYAO", "ASELS", "PGSUS", "TAVHL"],
    "Otomotiv": ["TOASO", "FROTO", "DOAS", "OTKAR", "ASUZU"],
    "Enerji": ["AKSEN", "AYEN", "CWENE", "ENKAI", "TUPRS", "AKENR", "AKSA"],
    "Holding": ["KCHOL", "SAHOL", "DOHOL", "AGHOL", "GSDHO", "KOZAL"],
    "Demir Çelik": ["EREGL", "KRDMD", "BRSAN"],
    "Perakende": ["BIMAS", "SOKM", "MGROS", "BIZIM"],
    "Teknoloji": ["LOGO", "ARENA", "INDES", "NETAS", "KAREL", "FONET"],
    "Telekomünikasyon": ["TCELL", "TTKOM"],
    "Kimya & Petrokimya": ["PETKM", "SASA", "GUBRF", "SISE"],
    "Gıda & İçecek": ["CCOLA", "ULKER", "TATGD", "AEFES", "BANVT"],
    "İnşaat & GYO": ["EKGYO", "ISGYO", "KLGYO", "ENKAI"],
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  VERİ ÇEKME FONKSİYONLARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data(ttl=600)
def get_index_data(symbol: str, period: str = "6mo") -> pd.DataFrame:
    """Endeks verisi çeker."""
    try:
        df = yf.download(symbol, period=period, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_sector_performance(sector_tickers: dict) -> pd.DataFrame:
    """Her sektörün ortalama performansını hesaplar."""
    results = []
    all_tickers = []
    ticker_sector = {}

    for sector, tickers in sector_tickers.items():
        for t in tickers:
            all_tickers.append(f"{t}.IS")
            ticker_sector[f"{t}.IS"] = sector

    try:
        data = yf.download(all_tickers, period="5d", progress=False, group_by='ticker')
    except:
        return pd.DataFrame()

    sector_changes = {}
    ticker_data = []

    for full_ticker in all_tickers:
        try:
            if len(all_tickers) > 1:
                df = data[full_ticker] if full_ticker in data.columns.get_level_values(0) else None
            else:
                df = data

            if df is None or df.empty or len(df) < 2:
                continue

            close_vals = df['Close'].dropna()
            if len(close_vals) < 2:
                continue

            last = float(close_vals.iloc[-1])
            prev = float(close_vals.iloc[-2])
            change_pct = ((last - prev) / prev) * 100

            sector = ticker_sector[full_ticker]
            ticker_clean = full_ticker.replace('.IS', '')

            if sector not in sector_changes:
                sector_changes[sector] = []
            sector_changes[sector].append(change_pct)

            ticker_data.append({
                'Hisse': ticker_clean,
                'Sektör': sector,
                'Fiyat': last,
                'Değişim': change_pct
            })
        except:
            continue

    return pd.DataFrame(ticker_data) if ticker_data else pd.DataFrame()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SAYFA İÇERİĞİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div style="text-align:center; padding:10px 0 24px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        📊 Piyasa Dashboard
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">BIST anlık piyasa özeti ve sektörel analiz</p>
</div>
""", unsafe_allow_html=True)

# ── Endeks Verileri ──
with st.spinner("📡 Piyasa verileri yükleniyor..."):
    xu030 = get_index_data("XU030.IS", "6mo")
    xu100 = get_index_data("XU100.IS", "6mo")

# ── Endeks Kartları ──
if not xu030.empty and not xu100.empty:
    c1, c2, c3, c4 = st.columns(4)

    for col, (label, df_idx) in zip(
        [c1, c2],
        [("BIST 30", xu030), ("BIST 100", xu100)]
    ):
        close = df_idx['Close'].dropna()
        if len(close) >= 2:
            last_val = float(close.iloc[-1])
            prev_val = float(close.iloc[-2])
            change = ((last_val - prev_val) / prev_val) * 100
            delta_class = "metric-delta-up" if change >= 0 else "metric-delta-down"
            arrow = "▲" if change >= 0 else "▼"

            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{last_val:,.0f}</div>
                    <div class="{delta_class}">{arrow} %{change:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

    # USD/TRY ve Altın
    usd = get_index_data("USDTRY=X", "5d")
    gold = get_index_data("GC=F", "5d")

    for col, (label, df_item, fmt) in zip(
        [c3, c4],
        [("USD/TRY", usd, ",.4f"), ("Altın (USD)", gold, ",.0f")]
    ):
        close = df_item['Close'].dropna() if not df_item.empty else pd.Series()
        if len(close) >= 2:
            last_val = float(close.iloc[-1])
            prev_val = float(close.iloc[-2])
            change = ((last_val - prev_val) / prev_val) * 100
            delta_class = "metric-delta-up" if change >= 0 else "metric-delta-down"
            arrow = "▲" if change >= 0 else "▼"

            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{last_val:{fmt}}</div>
                    <div class="{delta_class}">{arrow} %{change:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── BIST 30 Grafik ──
if not xu030.empty:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📈 BIST 30 Endeks Grafiği")

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=xu030.index,
        open=xu030['Open'],
        high=xu030['High'],
        low=xu030['Low'],
        close=xu030['Close'],
        name='BIST 30',
        increasing_line_color='#4ade80',
        decreasing_line_color='#f87171'
    ))

    # SMA 20
    sma20 = xu030['Close'].rolling(20).mean()
    fig.add_trace(go.Scatter(
        x=xu030.index, y=sma20,
        line=dict(color='#818cf8', width=1.5),
        name='SMA 20'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor='rgba(128,128,128,0.1)', rangeslider_visible=False),
        yaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(color='#94a3b8')),
        font=dict(color='#94a3b8')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Sektörel Isı Haritası & Top Movers ──
with st.spinner("📊 Sektörel veriler hesaplanıyor..."):
    sector_df = get_sector_performance(SECTOR_MAP)

if not sector_df.empty:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🗺️ Sektörel Isı Haritası")

        # Treemap
        # NaN değerleri temizle
        treemap_df = sector_df.dropna(subset=['Değişim', 'Fiyat']).copy()
        treemap_df['Fiyat_abs'] = treemap_df['Fiyat'].abs().clip(lower=1)

        fig_tree = px.treemap(
            treemap_df,
            path=['Sektör', 'Hisse'],
            values='Fiyat_abs',
            color='Değişim',
            color_continuous_scale=['#dc2626', '#991b1b', '#1e1e2e', '#166534', '#22c55e'],
            color_continuous_midpoint=0,
            custom_data=['Değişim'],
        )
        fig_tree.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=450,
            margin=dict(l=5, r=5, t=5, b=5),
            font=dict(color='#e2e8f0', size=12),
            coloraxis_colorbar=dict(
                title=dict(text="Değişim %", font=dict(color='#94a3b8')),
                tickfont=dict(color='#94a3b8'),
                bgcolor='rgba(0,0,0,0)'
            )
        )
        fig_tree.update_traces(
            textinfo="label+text",
            texttemplate="<b>%{label}</b><br>%{customdata[0]:.1f}%",
            textfont=dict(size=11)
        )
        st.plotly_chart(fig_tree, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # Top Gainers
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🟢 En Çok Yükselenler")
        top_up = sector_df.nlargest(8, 'Değişim')[['Hisse', 'Sektör', 'Değişim', 'Fiyat']]
        for _, row in top_up.iterrows():
            color = "#4ade80"
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
                <div>
                    <span style="color:#e2e8f0; font-weight:600;">{row['Hisse']}</span>
                    <span style="color:#64748b; font-size:0.75rem; margin-left:6px;">{row['Sektör']}</span>
                </div>
                <span style="color:{color}; font-weight:600;">▲ %{row['Değişim']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Top Losers
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔴 En Çok Düşenler")
        top_down = sector_df.nsmallest(8, 'Değişim')[['Hisse', 'Sektör', 'Değişim', 'Fiyat']]
        for _, row in top_down.iterrows():
            color = "#f87171"
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
                <div>
                    <span style="color:#e2e8f0; font-weight:600;">{row['Hisse']}</span>
                    <span style="color:#64748b; font-size:0.75rem; margin-left:6px;">{row['Sektör']}</span>
                </div>
                <span style="color:{color}; font-weight:600;">▼ %{abs(row['Değişim']):.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ Sektörel veri yüklenemedi. İnternet bağlantınızı kontrol edin.")

# ── Piyasa Nabzı ──
st.markdown("<br>", unsafe_allow_html=True)
if not sector_df.empty:
    avg_change = sector_df['Değişim'].mean()
    positive_pct = (sector_df['Değişim'] > 0).mean() * 100

    if avg_change > 1:
        mood, mood_color, mood_icon = "Aşırı Açgözlülük", "#4ade80", "🟢"
    elif avg_change > 0:
        mood, mood_color, mood_icon = "Pozitif", "#86efac", "🟡"
    elif avg_change > -1:
        mood, mood_color, mood_icon = "Temkinli", "#fbbf24", "🟠"
    else:
        mood, mood_color, mood_icon = "Korku", "#f87171", "🔴"

    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <h3 style="color:#e2e8f0; margin-bottom:12px;">🌡️ Piyasa Nabzı</h3>
        <div style="font-size:2.5rem; margin:8px 0;">{mood_icon}</div>
        <div style="font-size:1.3rem; color:{mood_color}; font-weight:700;">{mood}</div>
        <div style="color:#64748b; font-size:0.85rem; margin-top:8px;">
            Yükselen hisse oranı: <strong style="color:#e2e8f0;">%{positive_pct:.0f}</strong> |
            Ortalama değişim: <strong style="color:{mood_color};">%{avg_change:.2f}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
