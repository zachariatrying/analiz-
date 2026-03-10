"""
Hisse Karsilastirma
Iki hisseyi yan yana karsilastirin.
"""
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Karsilastirma", page_icon="", layout="wide")

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
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(168,85,247,0.08) 100%);
        border-radius: 14px; border: 1px solid rgba(99,102,241,0.15);
        padding: 16px; text-align: center;
    }
    .metric-value {
        font-size: 1.4rem; font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .metric-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    div[data-testid="stMetricValue"] { color: #818cf8; font-family: 'Inter', monospace; font-weight: 700; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: none !important; border-radius: 12px !important; font-weight: 600 !important;
    }
    hr { border-color: rgba(255,255,255,0.06) !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_stock_data(ticker, period="1y"):
    try:
        symbol = f"{ticker}.IS" if not ticker.endswith(".IS") else ticker
        df = yf.download(symbol, period=period, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if df.empty or len(df) < 10:
            return None
        df['SMA20'] = df['Close'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        delta = df['Close'].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        gain = up.rolling(14).mean()
        loss = down.rolling(14).mean().replace(0, 0.0001)
        df['RSI'] = 100 - (100 / (1 + gain / loss))
        df['Daily_Return'] = df['Close'].pct_change() * 100
        return df
    except:
        return None

def calc_metrics(df):
    if df is None or len(df) < 2:
        return {}
    close = df['Close'].dropna()
    last = float(close.iloc[-1])
    first = float(close.iloc[0])
    high_52 = float(close.max())
    low_52 = float(close.min())
    change_pct = ((last - first) / first) * 100
    volatility = float(df['Daily_Return'].dropna().std())
    avg_vol = float(df['Volume'].tail(20).mean()) if 'Volume' in df.columns else 0
    rsi = float(df['RSI'].dropna().iloc[-1]) if 'RSI' in df.columns and not df['RSI'].dropna().empty else 50
    return {
        'fiyat': last, 'degisim': change_pct, 'yuksek': high_52,
        'dusuk': low_52, 'volatilite': volatility, 'hacim': avg_vol,
        'rsi': rsi,
    }

# Sayfa
st.markdown("""
<div style="text-align:center; padding:10px 0 24px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        Hisse Karsilastirma
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">Iki hisseyi yan yana karsilastirin</p>
</div>
""", unsafe_allow_html=True)

# Inputs
col_in1, col_in2, col_in3 = st.columns([2, 2, 1])
with col_in1:
    hisse1 = st.text_input("Hisse 1", "THYAO")
with col_in2:
    hisse2 = st.text_input("Hisse 2", "PGSUS")
with col_in3:
    period = st.selectbox("Donem", ["3mo", "6mo", "1y", "2y"], index=2)

btn = st.button("KARSILASTIR", type="primary", use_container_width=True)

if btn:
    h1 = hisse1.upper().strip()
    h2 = hisse2.upper().strip()

    with st.spinner("Veriler yukleniyor..."):
        df1 = get_stock_data(h1, period)
        df2 = get_stock_data(h2, period)

    if df1 is None or df2 is None:
        st.error("Bir veya her iki hisse icin veri alinamadi.")
    else:
        m1 = calc_metrics(df1)
        m2 = calc_metrics(df2)

        # Ozet Kartlari
        st.divider()
        cols = st.columns(2)

        for col, (hisse, metrics) in zip(cols, [(h1, m1), (h2, m2)]):
            with col:
                fiyat_color = "#4ade80" if metrics['degisim'] >= 0 else "#f87171"
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <h3 style="color:#e2e8f0; margin-bottom:16px; font-size:1.3rem;">{hisse}</h3>
                    <div class="metric-value" style="font-size:2rem;">{metrics['fiyat']:.2f} TL</div>
                    <div style="color:{fiyat_color}; font-weight:600; margin-top:4px;">%{metrics['degisim']:.2f} ({period})</div>
                </div>
                """, unsafe_allow_html=True)

        # Karsilastirma Tablosu
        st.divider()
        st.markdown("### Karsilastirma Tablosu")

        compare_data = {
            'Metrik': ['Son Fiyat (TL)', f'Degisim % ({period})', '52H Yuksek', '52H Dusuk', 'Volatilite', 'Ort. Hacim (20G)', 'RSI'],
            h1: [f"{m1['fiyat']:.2f}", f"%{m1['degisim']:.2f}", f"{m1['yuksek']:.2f}", f"{m1['dusuk']:.2f}",
                 f"{m1['volatilite']:.2f}", f"{m1['hacim']:,.0f}", f"{m1['rsi']:.1f}"],
            h2: [f"{m2['fiyat']:.2f}", f"%{m2['degisim']:.2f}", f"{m2['yuksek']:.2f}", f"{m2['dusuk']:.2f}",
                 f"{m2['volatilite']:.2f}", f"{m2['hacim']:,.0f}", f"{m2['rsi']:.1f}"],
        }
        st.dataframe(pd.DataFrame(compare_data), use_container_width=True, hide_index=True)

        # Normalize Fiyat Grafigi
        st.divider()
        st.markdown("### Normalize Fiyat Performansi")
        st.caption("Baslangic noktasindan itibaren yuzdelik performans karsilastirmasi")

        fig = go.Figure()
        norm1 = (df1['Close'] / df1['Close'].iloc[0] - 1) * 100
        norm2 = (df2['Close'] / df2['Close'].iloc[0] - 1) * 100

        fig.add_trace(go.Scatter(x=df1.index, y=norm1, name=h1, line=dict(color='#818cf8', width=2.5)))
        fig.add_trace(go.Scatter(x=df2.index, y=norm2, name=h2, line=dict(color='#f472b6', width=2.5)))
        fig.add_hline(y=0, line_color="rgba(148,163,184,0.3)", line_width=1, line_dash="dash")

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=400, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor='rgba(128,128,128,0.08)'),
            yaxis=dict(gridcolor='rgba(128,128,128,0.08)', title='Degisim %',
                       titlefont=dict(color='#94a3b8')),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        font=dict(color='#94a3b8')),
            font=dict(color='#94a3b8'),
        )
        st.plotly_chart(fig, use_container_width=True)

        # RSI Karsilastirmasi
        st.divider()
        st.markdown("### RSI Karsilastirmasi")

        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=df1.index, y=df1['RSI'], name=h1, line=dict(color='#818cf8', width=1.5)))
        fig_rsi.add_trace(go.Scatter(x=df2.index, y=df2['RSI'], name=h2, line=dict(color='#f472b6', width=1.5)))
        fig_rsi.add_hline(y=70, line_color="rgba(248,113,113,0.4)", line_dash="dot", annotation_text="Asiri Alim", annotation_font_color="#f87171", annotation_font_size=10)
        fig_rsi.add_hline(y=30, line_color="rgba(74,222,128,0.4)", line_dash="dot", annotation_text="Asiri Satim", annotation_font_color="#4ade80", annotation_font_size=10)

        fig_rsi.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=300, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor='rgba(128,128,128,0.08)'),
            yaxis=dict(gridcolor='rgba(128,128,128,0.08)', range=[10, 90]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        font=dict(color='#94a3b8')),
            font=dict(color='#94a3b8'),
        )
        st.plotly_chart(fig_rsi, use_container_width=True)

        # Hacim Karsilastirmasi
        st.divider()
        st.markdown("### Hacim Karsilastirmasi")

        fig_vol = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles=[h1, h2])
        fig_vol.add_trace(go.Bar(x=df1.index, y=df1['Volume'], name=h1, marker_color='rgba(129,140,248,0.5)'), row=1, col=1)
        fig_vol.add_trace(go.Bar(x=df2.index, y=df2['Volume'], name=h2, marker_color='rgba(244,114,182,0.5)'), row=2, col=1)

        fig_vol.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=350, margin=dict(l=10, r=10, t=30, b=10),
            showlegend=False, font=dict(color='#94a3b8'),
        )
        fig_vol.update_xaxes(gridcolor='rgba(128,128,128,0.08)')
        fig_vol.update_yaxes(gridcolor='rgba(128,128,128,0.08)')
        st.plotly_chart(fig_vol, use_container_width=True)
