"""
Watchlist ve Fiyat Alarmi
Hisselere fiyat alarmi koyun, anlik kontrol edin.
"""
import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Alarm", page_icon="", layout="wide")

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
    .alert-triggered {
        background: rgba(74, 222, 128, 0.08);
        border: 1px solid rgba(74, 222, 128, 0.3);
        border-radius: 12px;
        padding: 16px; margin-bottom: 12px;
        animation: pulse 2s infinite;
    }
    .alert-waiting {
        background: rgba(99, 102, 241, 0.06);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 12px;
        padding: 16px; margin-bottom: 12px;
    }
    .alert-below {
        background: rgba(248, 113, 113, 0.08);
        border: 1px solid rgba(248, 113, 113, 0.3);
        border-radius: 12px;
        padding: 16px; margin-bottom: 12px;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(74,222,128,0.3); }
        50% { box-shadow: 0 0 20px 4px rgba(74,222,128,0.15); }
        100% { box-shadow: 0 0 0 0 rgba(74,222,128,0.3); }
    }
    div[data-testid="stMetricValue"] { color: #818cf8; font-family: 'Inter', monospace; font-weight: 700; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: none !important; border-radius: 12px !important;
        font-weight: 600 !important; padding: 10px 28px !important;
    }
    hr { border-color: rgba(255,255,255,0.06) !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# Session state for watchlist
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

st.markdown("""
<div style="text-align:center; padding:10px 0 24px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        Watchlist ve Alarm
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">Hisselere fiyat alarmi koyun, anlik durumu kontrol edin</p>
</div>
""", unsafe_allow_html=True)

# --- Alarm Ekleme ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Yeni Alarm Ekle")

col_add1, col_add2, col_add3, col_add4 = st.columns([2, 2, 2, 1])

with col_add1:
    alarm_hisse = st.text_input("Hisse Kodu", "THYAO", placeholder="Orn: THYAO")
with col_add2:
    alarm_tur = st.selectbox("Alarm Turu", ["Fiyat Uzerine Ciktiginda", "Fiyat Altina Dustugunde"])
with col_add3:
    alarm_fiyat = st.number_input("Hedef Fiyat (TL)", min_value=0.01, value=100.0, step=0.5)
with col_add4:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("EKLE", type="primary", use_container_width=True):
        new_alarm = {
            'hisse': alarm_hisse.upper().strip(),
            'tur': alarm_tur,
            'hedef': alarm_fiyat,
        }
        st.session_state.watchlist.append(new_alarm)
        st.success(f"{new_alarm['hisse']} alarmi eklendi.")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- Hizli Ekleme ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Toplu Alarm Ekleme")
st.caption("Her satira: HISSE,FIYAT,UST/ALT formatinda yazin")
toplu_input = st.text_area("Toplu alarm", placeholder="THYAO,320,UST\nGARAN,155,ALT\nASELS,80,UST", height=100, label_visibility="collapsed")
if st.button("Toplu Ekle"):
    lines = [l.strip() for l in toplu_input.strip().split('\n') if l.strip()]
    added = 0
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) >= 3:
            try:
                hisse = parts[0].upper()
                fiyat = float(parts[1])
                tur = "Fiyat Uzerine Ciktiginda" if parts[2].upper() in ['UST', 'UZERINE', 'UP'] else "Fiyat Altina Dustugunde"
                st.session_state.watchlist.append({'hisse': hisse, 'tur': tur, 'hedef': fiyat})
                added += 1
            except:
                pass
    if added > 0:
        st.success(f"{added} alarm eklendi.")
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- Alarm Listesi ve Kontrol ---
if st.session_state.watchlist:
    st.divider()

    col_kontrol, col_temizle = st.columns([3, 1])
    with col_kontrol:
        st.markdown("### Alarm Durumu")
    with col_temizle:
        if st.button("Tum Alarmlari Temizle"):
            st.session_state.watchlist = []
            st.rerun()

    btn_kontrol = st.button("ALARMLARI KONTROL ET", type="primary", use_container_width=True)

    if btn_kontrol:
        tickers_to_check = list(set([a['hisse'] for a in st.session_state.watchlist]))
        symbols = [f"{t}.IS" for t in tickers_to_check]

        with st.spinner("Fiyatlar kontrol ediliyor..."):
            try:
                if len(symbols) == 1:
                    data = yf.download(symbols[0], period="2d", progress=False)
                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = data.columns.get_level_values(0)
                    prices = {}
                    close = data['Close'].dropna()
                    if len(close) >= 1:
                        prices[tickers_to_check[0]] = float(close.iloc[-1])
                else:
                    data = yf.download(symbols, period="2d", progress=False, group_by='ticker')
                    prices = {}
                    for ticker, symbol in zip(tickers_to_check, symbols):
                        try:
                            df = data[symbol]
                            close = df['Close'].dropna()
                            if len(close) >= 1:
                                prices[ticker] = float(close.iloc[-1])
                        except:
                            pass
            except:
                prices = {}

        triggered = 0
        waiting = 0

        for alarm in st.session_state.watchlist:
            hisse = alarm['hisse']
            hedef = alarm['hedef']
            tur = alarm['tur']
            current = prices.get(hisse)

            if current is None:
                st.markdown(f"""
                <div class="alert-waiting">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="color:#e2e8f0; font-weight:700; font-size:1.1rem;">{hisse}</span>
                            <span style="color:#64748b; font-size:0.85rem; margin-left:8px;">Veri alinamadi</span>
                        </div>
                        <span style="color:#94a3b8; font-weight:600;">Hedef: {hedef:.2f} TL</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                continue

            if tur == "Fiyat Uzerine Ciktiginda":
                is_triggered = current >= hedef
            else:
                is_triggered = current <= hedef

            diff_pct = ((current - hedef) / hedef) * 100
            distance = abs(current - hedef)

            if is_triggered:
                triggered += 1
                css_class = "alert-triggered"
                status_text = "ALARM TETIKLENDI"
                status_color = "#4ade80"
            else:
                waiting += 1
                if tur == "Fiyat Uzerine Ciktiginda":
                    css_class = "alert-waiting"
                    status_text = f"Hedefe {distance:.2f} TL kaldi"
                    status_color = "#818cf8"
                else:
                    css_class = "alert-waiting"
                    status_text = f"Hedefe {distance:.2f} TL kaldi"
                    status_color = "#818cf8"

            tur_label = "Ust Alarm" if "Uzerine" in tur else "Alt Alarm"
            fiyat_color = "#4ade80" if current >= hedef and "Uzerine" in tur else "#f87171" if current <= hedef and "Altina" in tur else "#e2e8f0"

            st.markdown(f"""
            <div class="{css_class}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="color:#e2e8f0; font-weight:700; font-size:1.15rem;">{hisse}</span>
                        <span style="color:#94a3b8; font-size:0.8rem; margin-left:8px;">{tur_label}</span>
                    </div>
                    <span style="color:{status_color}; font-weight:700; font-size:0.9rem;">{status_text}</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                    <div>
                        <span style="color:#94a3b8; font-size:0.85rem;">Guncel: </span>
                        <span style="color:{fiyat_color}; font-weight:600;">{current:.2f} TL</span>
                    </div>
                    <div>
                        <span style="color:#94a3b8; font-size:0.85rem;">Hedef: </span>
                        <span style="color:#e2e8f0; font-weight:600;">{hedef:.2f} TL</span>
                    </div>
                    <div>
                        <span style="color:#94a3b8; font-size:0.85rem;">Fark: </span>
                        <span style="color:{'#4ade80' if diff_pct >= 0 else '#f87171'}; font-weight:600;">%{diff_pct:.2f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Ozet
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:16px;">
            <span style="color:#4ade80; font-weight:700;">{triggered} tetiklenen</span>
            <span style="color:#475569;"> | </span>
            <span style="color:#818cf8; font-weight:700;">{waiting} bekleyen</span>
            <span style="color:#475569;"> | </span>
            <span style="color:#94a3b8;">Toplam {len(st.session_state.watchlist)} alarm</span>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:40px;">
        <p style="color:#64748b; font-size:1rem;">Henuz alarm eklenmedi</p>
        <p style="color:#475569; font-size:0.85rem;">Yukaridaki formu kullanarak yeni alarm ekleyin</p>
    </div>
    """, unsafe_allow_html=True)

