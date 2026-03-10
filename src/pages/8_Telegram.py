"""
Telegram Bildirim
Alarm ve tarama sonuclarini Telegram uzerinden gonder.
"""
import streamlit as st
import requests
import json
try:
    from src.telegram_utils import send_telegram_alert
except ImportError:
    from telegram_utils import send_telegram_alert

st.set_page_config(page_title="Telegram", page_icon="", layout="wide")

import sys
import os
curr_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(curr_dir)
if curr_dir not in sys.path: sys.path.append(curr_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)
try:
    from src.theme import CSS_STYLE
except ImportError:
    from theme import CSS_STYLE

st.markdown(CSS_STYLE, unsafe_allow_html=True)

import os

CONFIG_FILE = "telegram_config.json"

def load_tg_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_tg_config(token, chat_id):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"token": token, "chat_id": chat_id}, f)

# Session state
config = load_tg_config()
if 'tg_token' not in st.session_state:
    st.session_state.tg_token = config.get("token", "")
if 'tg_chat_id' not in st.session_state:
    st.session_state.tg_chat_id = config.get("chat_id", "")
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
try:
    from src.watchlist_manager import load_watchlist
except:
    from watchlist_manager import load_watchlist

if 'watchlist' not in st.session_state:
    st.session_state.watchlist = load_watchlist()

# Removed local send_telegram function in favor of src.telegram_utils.send_telegram_alert

st.markdown("""
<div style="text-align:center; padding:10px 0 24px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        Telegram Bildirim
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">Alarm ve tarama sonuclarini Telegram uzerinden gonder</p>
</div>
""", unsafe_allow_html=True)

# --- Kurulum Rehberi ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Kurulum Rehberi")

st.markdown("""
<div class="step-card">
    <span style="color:#818cf8; font-weight:700;">Adim 1:</span>
    <span style="color:#e2e8f0;"> Telegram'da </span>
    <code style="color:#c084fc;">@BotFather</code>
    <span style="color:#e2e8f0;"> ile yeni bot olusturun</span>
    <br><span style="color:#94a3b8; font-size:0.85rem;">BotFather'a /newbot yazin, isim verin, token alin</span>
</div>
<div class="step-card">
    <span style="color:#818cf8; font-weight:700;">Adim 2:</span>
    <span style="color:#e2e8f0;"> Chat ID'nizi ogrenmek icin botunuza mesaj atin, sonra </span>
    <code style="color:#c084fc;">https://api.telegram.org/bot{TOKEN}/getUpdates</code>
    <span style="color:#e2e8f0;"> adresini ziyaret edin</span>
</div>
<div class="step-card">
    <span style="color:#818cf8; font-weight:700;">Adim 3:</span>
    <span style="color:#e2e8f0;"> Asagiya token ve chat ID girip 'Kaydet' butonuna basin. Bilgiler sadece cihazinizda kalir.</span>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Baglanti Ayarlari ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Baglanti Ayarlari")

col1, col2 = st.columns(2)
with col1:
    tg_token = st.text_input("Bot Token", value=st.session_state.tg_token, type="password", placeholder="1234567890:ABCDefGhIjKlMnOpQrStUvWxYz")
with col2:
    tg_chat = st.text_input("Chat ID", value=st.session_state.tg_chat_id, placeholder="123456789")

if st.button("AYARLARI KAYDET"):
    st.session_state.tg_token = tg_token
    st.session_state.tg_chat_id = tg_chat
    save_tg_config(tg_token, tg_chat)
    st.success("Tebrikler! Telegram ayarlariniz cihazinizda basariyla kaydedildi. Artık sayfa yenilense de gitmeyecek.")

# Test Butonu
    if st.button("BAGLANTI TESTI", type="primary", use_container_width=True):
        if not tg_token or not tg_chat:
            st.error("Token ve Chat ID gerekli.")
        else:
            # We temporarily save to session state for the test
            save_tg_config(tg_token, tg_chat)
            ok, resp = send_telegram_alert("BIST Teknik Analiz bağlantı testi başarılı.")
            if ok:
                st.success("Telegram mesajı gönderildi. Telegram uygulamanızı kontrol edin.")
            else:
                st.error(f"Gönderilemedi: {resp}")

st.markdown('</div>', unsafe_allow_html=True)

# --- Alarm Bildirimi ---
st.divider()
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Alarm Bildirimlerini Gonder")

alarm_count = len(st.session_state.watchlist)

if alarm_count == 0:
    st.info("Henuz alarm yok. Alarm sayfasindan veya Tarayicidan alarm ekleyin.")
else:
    st.markdown(f"""
    <div style="color:#94a3b8; font-size:0.9rem; margin-bottom:12px;">
        <strong style="color:#e2e8f0;">{alarm_count}</strong> adet alarm mevcut
    </div>
    """, unsafe_allow_html=True)

    if st.button("ALARMLARI TELEGRAM'A GONDER", type="primary", use_container_width=True):
        if not tg_token or not tg_chat:
            st.error("Once token ve chat ID giriniz.")
        else:
            msg = "<b>BIST Teknik Analiz - Alarm Listesi</b>\n\n"
            for i, alarm in enumerate(st.session_state.watchlist, 1):
                msg += f"{i}. <b>{alarm['hisse']}</b> | Hedef: <b>{alarm['hedef']:.2f}</b>"
                if 'stop' in alarm and alarm['stop'] > 0:
                    msg += f" | Stop: <b>{alarm['stop']:.2f}</b>"
                msg += "\n"
            msg += f"\nToplam: {alarm_count} alarm"

            ok, resp = send_telegram_alert(msg)
            if ok:
                st.success("Alarm listesi Telegram'a gonderildi.")
            else:
                st.error(f"Gonderilemedi: {resp}")

st.markdown('</div>', unsafe_allow_html=True)

# --- Ozellestirmis Mesaj ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Ozel Mesaj Gonder")

custom_msg = st.text_area("Mesaj", placeholder="Buraya ozel mesajinizi yazin...", height=80)
    if st.button("MESAJI GONDER", use_container_width=True):
        if not tg_token or not tg_chat:
            st.error("Once token ve chat ID giriniz.")
        elif not custom_msg.strip():
            st.error("Mesaj bos olamaz.")
        else:
            ok, resp = send_telegram_alert(custom_msg)
            if ok:
                st.success("Mesaj gonderildi.")
            else:
                st.error(f"Gonderilemedi: {resp}")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:20px 0; color:#475569; font-size:0.8rem;">
    Bot token'inizi kimseyle paylasmayiniz. Token bu oturumda gecici olarak saklanir.
</div>
""", unsafe_allow_html=True)

