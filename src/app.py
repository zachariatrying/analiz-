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

from src.theme import CSS_STYLE
st.markdown(CSS_STYLE, unsafe_allow_html=True)

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

