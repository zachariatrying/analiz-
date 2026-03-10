"""
Backtesting
Gecmis formasyonlarin basari oranini analiz edin.
"""
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from analyzer import Analyzer

st.set_page_config(page_title="Backtesting", page_icon="", layout="wide")

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
        padding: 20px; text-align: center;
    }
    .metric-value {
        font-size: 1.8rem; font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .metric-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
    div[data-testid="stMetricValue"] { color: #818cf8; font-family: 'Inter', monospace; font-weight: 700; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: none !important; border-radius: 12px !important; font-weight: 600 !important;
    }
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #a78bfa, #c084fc) !important; border-radius: 8px;
    }
    hr { border-color: rgba(255,255,255,0.06) !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_analyzer():
    return Analyzer()

analyzer_engine = get_analyzer()

@st.cache_data(ttl=600)
def get_long_data(ticker, period="5y"):
    try:
        symbol = f"{ticker}.IS" if not ticker.endswith(".IS") else ticker
        df = yf.download(symbol, period=period, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if df.empty or len(df) < 100:
            return None
        return df
    except:
        return None

def run_backtest(df, analyzer, pattern_type, secilen_formasyon):
    """Sliding window ile gecmiste formasyon arar ve sonrasindaki performansi olcer."""
    results = []
    window = 150
    step = 20

    if len(df) < window + 30:
        return results

    for start in range(0, len(df) - window - 30, step):
        window_df = df.iloc[start:start + window].copy()
        if 'Date' not in window_df.columns:
            window_df['Date'] = window_df.index

        # Indikatorleri ekle
        try:
            window_df = analyzer.add_indicators(window_df)
        except:
            continue

        # Pattern config
        analyzer.config['enabled_patterns'] = {
            'tobo': pattern_type == 'tobo',
            'obo': pattern_type == 'obo',
            'cup': pattern_type == 'cup',
            'flag': pattern_type == 'flag',
            'flama': pattern_type == 'flama',
            'breakout': False,
        }

        try:
            patterns = analyzer.detect_classic_patterns(window_df)

            if pattern_type == 'rsi_div':
                zz = analyzer.calculate_zigzag(window_df)
                patterns = analyzer.detect_rsi_divergence(window_df, zz)

            for p in patterns:
                # Eger user Boga Bayrak sectiyse, Ayi Bayrak sonuclarini atla
                if secilen_formasyon == "Boga Bayrak" and "Ayı" in p.get('name', ''):
                    continue

                # Benzersizlik kontrolu (ayni formasyon, cok yakin tarihlerde tekrar yakalanmasin)
                current_date = window_df.index[-1]
                p_name = p.get('name', 'Bilinmeyen')
                
                # Eger ayni formasyon adi son 10 gunde zaten eklendiyse, atla (Sliding window kesisimi)
                is_duplicate = False
                for existing in results:
                    if existing['formasyon'] == p_name:
                        delta = abs((current_date - existing['tarih']).days)
                        if delta < 15:  # 15 gun icinde ayni formasyon tipiyse muhtemelen sliding window tekraridir
                            is_duplicate = True
                            break
                if is_duplicate:
                    continue

                # Formasyondan sonraki 10, 20, 30 gunluk performansi olc
                end_idx = start + window
                future = df.iloc[end_idx:end_idx + 30]

                if len(future) < 10:
                    continue

                entry_price = float(window_df['Close'].iloc[-1])
                target = float(p.get('target', entry_price * 1.05))
                stop = float(p.get('stop', entry_price * 0.95))

                perf_10 = ((float(future['Close'].iloc[min(9, len(future)-1)]) - entry_price) / entry_price) * 100
                perf_20 = ((float(future['Close'].iloc[min(19, len(future)-1)]) - entry_price) / entry_price) * 100 if len(future) > 19 else None
                perf_30 = ((float(future['Close'].iloc[min(29, len(future)-1)]) - entry_price) / entry_price) * 100 if len(future) > 29 else None

                max_gain = ((float(future['High'].max()) - entry_price) / entry_price) * 100
                max_loss = ((float(future['Low'].min()) - entry_price) / entry_price) * 100

                hit_target = float(future['High'].max()) >= target
                hit_stop = float(future['Low'].min()) <= stop

                results.append({
                    'tarih': current_date,
                    'formasyon': p_name,
                    'skor': p.get('score', 50),
                    'giris': entry_price,
                    'hedef': target,
                    'stop': stop,
                    'perf_10g': perf_10,
                    'perf_20g': perf_20,
                    'perf_30g': perf_30,
                    'max_kar': max_gain,
                    'max_zarar': max_loss,
                    'hedefe_ulasti': hit_target,
                    'stopa_geldi': hit_stop,
                })
        except:
            continue

    return results

# Sayfa
st.markdown("""
<div style="text-align:center; padding:10px 0 24px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        Backtesting
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">Gecmis formasyonlarin basari oranini test edin</p>
</div>
""", unsafe_allow_html=True)

# Inputlar
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Test Ayarlari")
col1, col2, col3 = st.columns(3)
with col1:
    bt_hisse = st.text_input("Hisse Kodu", "THYAO")
with col2:
    bt_formasyon = st.selectbox("Formasyon", [
        "TOBO", "OBO", "Fincan Kulp", "Boga Bayrak", "Flama", "RSI Uyumsuzluk"
    ])
with col3:
    bt_period = st.selectbox("Gecmis Veri", ["2y", "3y", "5y"], index=1)

pattern_map = {
    "TOBO": "tobo", "OBO": "obo", "Fincan Kulp": "cup",
    "Boga Bayrak": "flag", "Flama": "flama", "RSI Uyumsuzluk": "rsi_div"
}
btn_test = st.button("TESTI BASLAT", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if btn_test:
    hisse = bt_hisse.upper().strip()
    p_type = pattern_map[bt_formasyon]

    with st.spinner(f"{hisse} icin {bt_formasyon} backtesti calisiyor..."):
        df = get_long_data(hisse, bt_period)

    if df is None:
        st.error("Veri alinamadi.")
    else:
        with st.spinner("Formasyonlar taraniyor (bu islem uzun surebilir)..."):
            bar = st.progress(0)
            results = run_backtest(df, analyzer_engine, p_type, bt_formasyon)
            bar.empty()

        if not results:
            st.warning(f"{hisse} icin {bt_formasyon} formasyonu gecmis veride bulunamadi. Farkli hisse veya formasyon deneyin.")
        else:
            res_df = pd.DataFrame(results)

            # Ozet Istatistikler
            total = len(res_df)
            hit_target_pct = (res_df['hedefe_ulasti'].sum() / total) * 100
            hit_stop_pct = (res_df['stopa_geldi'].sum() / total) * 100
            avg_10 = res_df['perf_10g'].mean()
            avg_max = res_df['max_kar'].mean()
            avg_loss = res_df['max_zarar'].mean()

            st.divider()

            c1, c2, c3, c4, c5 = st.columns(5)
            stats = [
                ("Toplam Sinyal", f"{total}"),
                ("Hedefe Ulasma", f"%{hit_target_pct:.0f}"),
                ("Stop Orani", f"%{hit_stop_pct:.0f}"),
                ("Ort. 10G Perf.", f"%{avg_10:.2f}"),
                ("Ort. Max Kar", f"%{avg_max:.2f}"),
            ]
            for col, (label, value) in zip([c1, c2, c3, c4, c5], stats):
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Performans Grafigi
            st.divider()
            st.markdown("### Sinyal Sonrasi Performans Dagilimi")

            fig = go.Figure()
            fig.add_trace(go.Box(
                y=res_df['perf_10g'], name='10 Gun', marker_color='#818cf8',
                boxmean=True
            ))
            if res_df['perf_20g'].notna().any():
                fig.add_trace(go.Box(
                    y=res_df['perf_20g'].dropna(), name='20 Gun', marker_color='#c084fc',
                    boxmean=True
                ))
            if res_df['perf_30g'].notna().any():
                fig.add_trace(go.Box(
                    y=res_df['perf_30g'].dropna(), name='30 Gun', marker_color='#f472b6',
                    boxmean=True
                ))
            fig.add_hline(y=0, line_color="rgba(148,163,184,0.3)", line_dash="dash")
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=350, margin=dict(l=10, r=10, t=10, b=10),
                yaxis=dict(gridcolor='rgba(128,128,128,0.08)', title=dict(text='Performans %', font=dict(color='#94a3b8'))),
                xaxis=dict(gridcolor='rgba(128,128,128,0.08)'),
                font=dict(color='#94a3b8'),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Basari Orani Grafigi
            st.markdown("### Hedef vs Stop Orani")
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Hedefe Ulasti', 'Stopa Geldi', 'Belirsiz'],
                values=[
                    res_df['hedefe_ulasti'].sum(),
                    res_df['stopa_geldi'].sum(),
                    total - res_df['hedefe_ulasti'].sum() - res_df['stopa_geldi'].sum() + (res_df['hedefe_ulasti'] & res_df['stopa_geldi']).sum()
                ],
                marker=dict(colors=['#4ade80', '#f87171', '#94a3b8']),
                hole=0.5,
                textinfo='label+percent',
                textfont=dict(color='#e2e8f0'),
            )])
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                height=350, margin=dict(l=10, r=10, t=10, b=10),
                font=dict(color='#94a3b8'),
                showlegend=False,
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # Detay Tablosu
            st.divider()
            st.markdown("### Detayli Sonuclar")
            display_df = res_df[['tarih', 'formasyon', 'skor', 'giris', 'perf_10g', 'perf_20g', 'perf_30g', 'max_kar', 'max_zarar', 'hedefe_ulasti']].copy()
            display_df.columns = ['Tarih', 'Formasyon', 'Skor', 'Giris Fiyati', '10G %', '20G %', '30G %', 'Max Kar %', 'Max Zarar %', 'Hedefe Ulasti']
            st.dataframe(display_df, use_container_width=True, hide_index=True)

st.markdown("""
<div style="text-align:center; padding:20px 0; color:#475569; font-size:0.8rem;">
    Backtesting sonuclari gecmis performansi gosterir, gelecek performansi garanti etmez.
</div>
""", unsafe_allow_html=True)
