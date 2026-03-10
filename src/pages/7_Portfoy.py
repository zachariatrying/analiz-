"""
Portfoy Takibi
Alis/satis kaydi, kar/zarar hesaplama, portfoy dagilimi
"""
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Portfoy", page_icon="", layout="wide")

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

# Session state
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

st.markdown("""
<div style="text-align:center; padding:10px 0 24px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        Portfoy Takibi
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">Alis/satis kaydi, kar/zarar ve portfoy dagilimi</p>
</div>
""", unsafe_allow_html=True)

# --- Islem Ekleme ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Yeni Islem Ekle")

c1, c2, c3, c4, c5 = st.columns([2, 1.5, 1.5, 1.5, 1])
with c1:
    p_hisse = st.text_input("Hisse", "THYAO", key="p_hisse")
with c2:
    p_islem = st.selectbox("Islem", ["ALIS", "SATIS"])
with c3:
    p_lot = st.number_input("Lot", min_value=1, value=100, step=10)
with c4:
    p_fiyat = st.number_input("Fiyat (TL)", min_value=0.01, value=100.0, step=0.5)
with c5:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("EKLE", type="primary", use_container_width=True, key="add_tx"):
        tx = {
            'hisse': p_hisse.upper().strip(),
            'islem': p_islem,
            'lot': p_lot,
            'fiyat': p_fiyat,
            'toplam': p_lot * p_fiyat,
        }
        st.session_state.portfolio.append(tx)
        st.success(f"{tx['islem']} - {tx['hisse']} x{tx['lot']} @ {tx['fiyat']:.2f} TL")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- Toplu Ekleme ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Toplu Islem Ekleme")
st.caption("Her satira: HISSE,ALIS/SATIS,LOT,FIYAT formatinda yazin")
toplu = st.text_area("Toplu islem", placeholder="THYAO,ALIS,100,310\nGARAN,ALIS,200,140\nASELS,ALIS,50,75", height=80, label_visibility="collapsed")
if st.button("Toplu Ekle", key="bulk_tx"):
    lines = [l.strip() for l in toplu.strip().split('\n') if l.strip()]
    added = 0
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) >= 4:
            try:
                st.session_state.portfolio.append({
                    'hisse': parts[0].upper(),
                    'islem': parts[1].upper(),
                    'lot': int(parts[2]),
                    'fiyat': float(parts[3]),
                    'toplam': int(parts[2]) * float(parts[3]),
                })
                added += 1
            except: pass
    if added > 0:
        st.success(f"{added} islem eklendi.")
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- Sekmeler (Tabs) ---
st.divider()
tab_portfoy, tab_takip = st.tabs(["📊 Acik Pozisyonlar", "🎯 Takip Listesi (Alarmlar)"])

with tab_portfoy:
    if st.session_state.portfolio:
        col_h, col_t = st.columns([3, 1])
        with col_h:
            st.markdown("### Portfoy Durumu")
        with col_t:
            if st.button("Tum Islemleri Temizle"):
                st.session_state.portfolio = []
                st.rerun()

        btn_guncelle = st.button("PORTFOYU GUNCELLE (Canli Fiyat)", type="primary", use_container_width=True)

        # Islem tablosu
        tx_df = pd.DataFrame(st.session_state.portfolio)
        st.dataframe(tx_df, use_container_width=True, hide_index=True)

        if btn_guncelle:
            # Net pozisyonlari hesapla
            positions = {}
            for tx in st.session_state.portfolio:
                h = tx['hisse']
                if h not in positions:
                    positions[h] = {'lot': 0, 'maliyet': 0}
                if tx['islem'] == 'ALIS':
                    positions[h]['maliyet'] += tx['toplam']
                    positions[h]['lot'] += tx['lot']
                else:
                    positions[h]['lot'] -= tx['lot']
                    positions[h]['maliyet'] -= tx['toplam']

            # Sifir veya negatif pozisyonlari kaldir
            positions = {k: v for k, v in positions.items() if v['lot'] > 0}

            if not positions:
                st.warning("Acik pozisyon yok.")
            else:
                # Canli fiyatlari cek
                tickers = list(positions.keys())
                symbols = [f"{t}.IS" for t in tickers]

                with st.spinner("Canli fiyatlar yukleniyor..."):
                    try:
                        if len(symbols) == 1:
                            data = yf.download(symbols[0], period="2d", progress=False)
                            if isinstance(data.columns, pd.MultiIndex):
                                data.columns = data.columns.get_level_values(0)
                            prices = {tickers[0]: float(data['Close'].dropna().iloc[-1])}
                        else:
                            data = yf.download(symbols, period="2d", progress=False, group_by='ticker')
                            prices = {}
                            for ticker, symbol in zip(tickers, symbols):
                                try:
                                    df = data[symbol]
                                    prices[ticker] = float(df['Close'].dropna().iloc[-1])
                                except: pass
                    except:
                        prices = {}

                # Portfoy hesaplama
                rows = []
                total_maliyet = 0
                total_guncel = 0
                total_kar = 0

                for hisse, pos in positions.items():
                    guncel_fiyat = prices.get(hisse, 0)
                    ort_maliyet = pos['maliyet'] / pos['lot'] if pos['lot'] > 0 else 0
                    guncel_deger = guncel_fiyat * pos['lot']
                    kar_zarar = guncel_deger - pos['maliyet']
                    kar_pct = ((guncel_fiyat - ort_maliyet) / ort_maliyet) * 100 if ort_maliyet > 0 else 0

                    total_maliyet += pos['maliyet']
                    total_guncel += guncel_deger
                    total_kar += kar_zarar

                    rows.append({
                        'Hisse': hisse,
                        'Lot': pos['lot'],
                        'Ort. Maliyet': f"{ort_maliyet:.2f}",
                        'Guncel Fiyat': f"{guncel_fiyat:.2f}",
                        'Maliyet': f"{pos['maliyet']:,.0f}",
                        'Guncel Deger': f"{guncel_deger:,.0f}",
                        'Kar/Zarar': f"{kar_zarar:,.0f}",
                        'Kar %': f"%{kar_pct:.2f}",
                        '_kar_zarar': kar_zarar,
                        '_deger': guncel_deger,
                    })

                # Ozet kartlari
                total_pct = ((total_guncel - total_maliyet) / total_maliyet) * 100 if total_maliyet > 0 else 0
                pct_color = "#4ade80" if total_kar >= 0 else "#f87171"

                mc1, mc2, mc3, mc4 = st.columns(4)
                summaries = [
                    ("Toplam Maliyet", f"{total_maliyet:,.0f} TL"),
                    ("Guncel Deger", f"{total_guncel:,.0f} TL"),
                    ("Kar / Zarar", f"{total_kar:,.0f} TL"),
                    ("Toplam Getiri", f"%{total_pct:.2f}"),
                ]
                for col, (label, value) in zip([mc1, mc2, mc3, mc4], summaries):
                    with col:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value" style="color:{pct_color if 'Kar' in label or 'Getiri' in label else '#e2e8f0'}">{value}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Detayli tablo
                detail_df = pd.DataFrame(rows)
                display_cols = ['Hisse', 'Lot', 'Ort. Maliyet', 'Guncel Fiyat', 'Maliyet', 'Guncel Deger', 'Kar/Zarar', 'Kar %']
                st.dataframe(detail_df[display_cols], use_container_width=True, hide_index=True)

                # Portfoy dagilimi pasta grafigi
                st.divider()
                col_pie, col_bar = st.columns(2)

                with col_pie:
                    st.markdown("### Portfoy Dagilimi")
                    labels = [r['Hisse'] for r in rows]
                    values = [r['_deger'] for r in rows]
                    colors = ['#818cf8', '#c084fc', '#f472b6', '#4ade80', '#fbbf24', '#38bdf8', '#f87171', '#a78bfa']

                    fig_pie = go.Figure(data=[go.Pie(
                        labels=labels, values=values,
                        marker=dict(colors=colors[:len(labels)]),
                        hole=0.45, textinfo='label+percent',
                        textfont=dict(color='#e2e8f0', size=12),
                    )])
                    fig_pie.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', height=350,
                        margin=dict(l=10, r=10, t=10, b=10),
                        font=dict(color='#94a3b8'), showlegend=False,
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col_bar:
                    st.markdown("### Kar/Zarar Dagilimi")
                    bar_colors = ['#4ade80' if r['_kar_zarar'] >= 0 else '#f87171' for r in rows]
                    fig_bar = go.Figure(data=[go.Bar(
                        x=[r['Hisse'] for r in rows],
                        y=[r['_kar_zarar'] for r in rows],
                        marker_color=bar_colors,
                    )])
                    fig_bar.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        height=350, margin=dict(l=10, r=10, t=10, b=10),
                        xaxis=dict(gridcolor='rgba(128,128,128,0.08)'),
                        yaxis=dict(gridcolor='rgba(128,128,128,0.08)', title='TL'),
                        font=dict(color='#94a3b8'),
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:40px;">
            <p style="color:#64748b; font-size:1rem;">Henuz islem eklenmedi</p>
            <p style="color:#475569; font-size:0.85rem;">Yukaridaki formu kullanarak alis/satis islemleri ekleyin</p>
        </div>
        """, unsafe_allow_html=True)


with tab_takip:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    try:
        from src.watchlist_manager import load_watchlist, save_watchlist
    except:
        from watchlist_manager import load_watchlist, save_watchlist

    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = load_watchlist()

    if len(st.session_state.watchlist) == 0:
        st.info("Henüz alarma eklenmis bir hisse yok. Tarayici sayfasindan tespit edilen formasyonlari alarma ekleyebilirsiniz.")
    else:
        st.markdown("### Takip Listem (Alarmlar)")
        
        btn_takip = st.button("TAKIP LİSTESİNİ GUNCELLE (Canli Fiyat)", type="primary", use_container_width=True, key="btn_takip")
        
        # Baslangic DataFrame'i
        takip_df = pd.DataFrame(st.session_state.watchlist)
        if 'giris' not in takip_df.columns:
            takip_df['giris'] = 0.0
        if 'stop' not in takip_df.columns:
            takip_df['stop'] = 0.0
            
        takip_df.rename(columns={'hisse': 'Hisse', 'tur': 'Tur', 'hedef': 'Hedef', 'stop': 'Stop', 'giris': 'Giris'}, inplace=True)
        takip_cols = ['Hisse', 'Tur', 'Giris', 'Hedef', 'Stop']
        
        display_df = takip_df[takip_cols].copy()
        display_df['Giris'] = display_df['Giris'].apply(lambda x: f"{x:.2f}" if float(x) > 0 else "Bilinmiyor")
        display_df['Hedef'] = display_df['Hedef'].apply(lambda x: f"{x:.2f}")
        display_df['Stop'] = display_df['Stop'].apply(lambda x: f"{x:.2f}" if float(x) > 0 else "-")
        
        if not btn_takip:
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            # Canli Fiyat Cek ve Kar Zarar goster
            tickers = list(takip_df['Hisse'].unique())
            symbols = [f"{t}.IS" for t in tickers]
            
            with st.spinner("Canli fiyatlar yukleniyor..."):
                try:
                    if len(symbols) == 1:
                        data = yf.download(symbols[0], period="2d", progress=False)
                        if isinstance(data.columns, pd.MultiIndex):
                            data.columns = data.columns.get_level_values(0)
                        prices = {tickers[0]: float(data['Close'].dropna().iloc[-1])}
                    else:
                        data = yf.download(symbols, period="2d", progress=False, group_by='ticker')
                        prices = {}
                        for ticker, symbol in zip(tickers, symbols):
                            try:
                                df = data[symbol]
                                prices[ticker] = float(df['Close'].dropna().iloc[-1])
                            except: pass
                except:
                    prices = {}
                    
            # Fiyatlari Guncelle
            live_rows = []
            for _, row in takip_df.iterrows():
                h = row['Hisse']
                c_price = prices.get(h, 0.0)
                g_price = float(row['Giris']) if row['Giris'] else 0.0
                h_price = float(row['Hedef'])
                s_price = float(row['Stop'])
                
                pct_change = ((c_price - g_price) / g_price) * 100 if g_price > 0 else 0
                
                # Hedefe / Stoba yaklasikligi hesaplama (opsiyonel gorsel stat)
                dist_target = ((h_price - c_price) / c_price) * 100 if c_price > 0 else 0
                
                # Sinyal Durumu
                status_icon = "⏳"
                if c_price >= h_price and h_price > 0:
                    status_icon = "✅ (Hedef)"
                elif c_price <= s_price and s_price > 0:
                    status_icon = "❌ (Stop)"
                
                live_rows.append({
                    'Hisse': h,
                    'Sinyal Fiyati (Giris)': f"{g_price:.2f}" if g_price > 0 else "-",
                    'Anlik Fiyat': f"{c_price:.2f}" if c_price > 0 else "-",
                    'Degisim': f"%{pct_change:.2f}",
                    'Hedef': f"{h_price:.2f}",
                    'Hedefe Uzaklik': f"%{dist_target:.2f}" if c_price > 0 else "-",
                    'Stop': f"{s_price:.2f}" if s_price > 0 else "-",
                    'Durum': status_icon
                })
                
            ldf = pd.DataFrame(live_rows)
            st.dataframe(ldf, use_container_width=True, hide_index=True)
            
            # Formisyon temizleme butonu
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Tum Alarmlari Temizle"):
                    st.session_state.watchlist = []
                    save_watchlist([])
                    st.rerun()

