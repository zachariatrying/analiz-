"""
BIST Borsa Teknik Analiz Platformu
Ana uygulama girisi (Multi-page Streamlit)
"""
import streamlit as st

st.set_page_config(
    page_title="BIST Teknik Analiz",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 24px; margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
        transform: translateY(-2px);
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(168,85,247,0.08) 100%);
        border-radius: 14px;
        border: 1px solid rgba(99,102,241,0.15);
        padding: 20px; text-align: center;
    }
    .metric-value {
        font-size: 2rem; font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 4px 0;
    }
    .metric-label {
        font-size: 0.8rem; color: #94a3b8;
        text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600;
    }
    .metric-delta-up { color: #4ade80; font-weight: 600; }
    .metric-delta-down { color: #f87171; font-weight: 600; }
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
    .page-header { text-align: center; padding: 20px 0 30px 0; }
    .page-header h1 {
        font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .page-header p { color: #64748b; font-size: 1.05rem; font-weight: 400; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# Ana Sayfa
st.markdown("""
<div class="page-header">
    <h1>BIST Teknik Analiz</h1>
    <p>Borsa Istanbul Teknik Analiz Platformu</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <h3 style="color:#e2e8f0; margin:0 0 8px 0; font-size:1.1rem;">Dashboard</h3>
        <p style="color:#64748b; font-size:0.85rem; margin:0;">Piyasa genel bakis, sektorel isi haritasi ve anlik veriler</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <h3 style="color:#e2e8f0; margin:0 0 8px 0; font-size:1.1rem;">Teknik Tarayici</h3>
        <p style="color:#64748b; font-size:0.85rem; margin:0;">8 farkli formasyon ile otomatik hisse tarama ve analiz</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <h3 style="color:#e2e8f0; margin:0 0 8px 0; font-size:1.1rem;">Egitim</h3>
        <p style="color:#64748b; font-size:0.85rem; margin:0;">Teknik analiz formasyonlari ve indikator rehberi</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <h3 style="color:#e2e8f0; margin-bottom:16px;">Platform Yetenekleri</h3>
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px;">
        <div style="color:#94a3b8; font-size:0.9rem;">
            <strong style="color:#e2e8f0;">8 Formasyon</strong> -- TOBO, OBO, Cup and Handle, Bayrak, Flama, HTF, RSI Div, Mum<br>
            <strong style="color:#e2e8f0;">ZigZag Algoritmasi</strong> -- Geometrik dogrulama ile hassas tespit<br>
            <strong style="color:#e2e8f0;">Hacim Profili</strong> -- Volume confirmation analizi<br>
        </div>
        <div style="color:#94a3b8; font-size:0.9rem;">
            <strong style="color:#e2e8f0;">500+ Hisse</strong> -- Tum BIST hisseleri taranabilir<br>
            <strong style="color:#e2e8f0;">6 Zaman Dilimi</strong> -- 1H den Aylik a kadar<br>
            <strong style="color:#e2e8f0;">Akilli Skorlama</strong> -- Hedef fiyat ve stop-loss hesaplama<br>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:20px 0; color:#475569; font-size:0.8rem;">
    Sol menuден sayfalara gecis yapabilirsiniz
</div>
""", unsafe_allow_html=True)
