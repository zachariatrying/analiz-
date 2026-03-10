"""
Derinlik (AKD) Modulu
@borsabilgibot uzerinden kullanici hesabiyla (UserBot) derinlik verisi cekme.
"""
import streamlit as st
import asyncio
import os
import time

# Tema entegrasyonu
import sys
curr_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(curr_dir)
if curr_dir not in sys.path: sys.path.append(curr_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)
try:
    from src.theme import CSS_STYLE
except ImportError:
    from theme import CSS_STYLE

from telethon import TelegramClient, events

st.set_page_config(page_title="Derinlik & AKD", page_icon="", layout="wide")
st.markdown(CSS_STYLE, unsafe_allow_html=True)

SESSION_FILE = os.path.join(parent_dir, 'userbot.session')

# Session states
if 'api_id' not in st.session_state: st.session_state.api_id = ""
if 'api_hash' not in st.session_state: st.session_state.api_hash = ""
if 'phone' not in st.session_state: st.session_state.phone = ""
if 'auth_msg' not in st.session_state: st.session_state.auth_msg = ""
if 'is_authorized' not in st.session_state: st.session_state.is_authorized = False
if 'awaiting_code' not in st.session_state: st.session_state.awaiting_code = False
if 'phone_code_hash' not in st.session_state: st.session_state.phone_code_hash = ""
if 'client' not in st.session_state: st.session_state.client = None

st.markdown("""
<div style="text-align:center; padding:10px 0 24px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        Derinlik Analizi
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">Telegram @borsabilgibot uzerinden gercek zamanli derinlik goruntusu</p>
</div>
""", unsafe_allow_html=True)

# Helper function
def get_client(api_id, api_hash):
    try:
        api_id_int = int(api_id) if api_id else 0
    except ValueError:
        api_id_int = 0
        
    # Telethon needs non-empty strings, pass a dummy string if empty
    safe_hash = api_hash if hasattr(api_hash, 'strip') and api_hash.strip() else "dummy_hash"
    
    return TelegramClient(SESSION_FILE, api_id_int, safe_hash)

import threading
import concurrent.futures

def run_async(coro):
    """
    Safely runs an async coroutine. 
    To bypass Streamlit's main thread asyncio restrictions and 'Timeout should be used inside a task' errors in Python 3.14+,
    we execute the Telethon client operations in a completely isolated background thread running a pristine asyncio.run() environment.
    This prevents nest_asyncio's global event loop patches from stripping context variables needed by Telethon.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(asyncio.run, coro)
        return future.result()

async def check_auth(api_id, api_hash):
    if not (api_id and api_hash):
        return False
    client = get_client(api_id, api_hash)
    await client.connect()
    try:
        return await client.is_user_authorized()
    finally:
        await client.disconnect()

async def send_code(api_id, api_hash, phone):
    client = get_client(api_id, api_hash)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            sent_code = await client.send_code_request(phone)
            return {"status": "success", "msg": "Dogrulama kodu SMS veya Telegram'dan gonderildi.", "phone_code_hash": getattr(sent_code, "phone_code_hash", "")}
        return {"status": "already_auth", "msg": "Zaten giris yapilmis."}
    except Exception as e:
        return {"status": "error", "msg": f"Hata: {str(e)}"}
    finally:
        await client.disconnect()

async def sign_in(api_id, api_hash, phone, code, phone_code_hash):
    client = get_client(api_id, api_hash)
    await client.connect()
    try:
        await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
        return {"status": "success", "msg": "Giris basarili! Artik sorgu yapabilirsiniz."}
    except Exception as e:
        return {"status": "error", "msg": f"Giris Hatasi: {str(e)}"}
    finally:
        await client.disconnect()

async def get_derinlik(api_id, api_hash, ticker):
    client = get_client(api_id, api_hash)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            return {"error": "Lutfen once giris yapin."}

        target_bot = "@borsabilgibot"
        command = f"/derinlik {ticker.upper()}"
        
        # Send message
        await client.send_message(target_bot, command)
        
        # Wait for response (timeout 30 sec for two-step interaction)
        response_msg = None
        media_path = None
        start_time = time.time()
        clicked_button = False
        
        # Basic polling loops
        while time.time() - start_time < 30:
            # Get last 2 messages from bot
            messages = await client.get_messages(target_bot, limit=2)
            
            for msg in messages:
                if not msg.out:
                    # If message has an image, download it and we are done
                    if msg.media:
                        file_loc = os.path.join(parent_dir, f"tmp_derinlik_{ticker}.jpg")
                        media_path = await client.download_media(msg, file=file_loc)
                        response_msg = msg.text or "Derinlik grafiği başarıyla çekildi."
                        break
                        
                    # If no image yet, but the message has inline buttons and we haven't clicked one yet
                    if not clicked_button and hasattr(msg, 'buttons') and msg.buttons:
                        for row in msg.buttons:
                            for button in row:
                                btn_text = button.text.lower()
                                # Check if button matches our target action
                                if any(kw in btn_text for kw in ["derinlik", "görüntü", "goruntu", "al"]):
                                    await button.click()
                                    clicked_button = True
                                    # Reset timeout since we just requested the image
                                    start_time = time.time()
                                    break
                            if clicked_button:
                                break
                    
                    # If it's just text without buttons and no media yet, store it but keep waiting
                    if not msg.media and not hasattr(msg, 'buttons'):
                        response_msg = msg.text

            if media_path:
                break
                
            await asyncio.sleep(1)
            
        if not media_path:
            if response_msg:
                return {"error": f"Bot resim göndermedi. Son gelen mesaj:\n{response_msg}"}
            return {"error": "Bottan 30 saniye icinde yanit gelmedi veya sunucu yogun."}
            
        return {"text": response_msg, "media": media_path}
    finally:
        await client.disconnect()

async def log_out_client(api_id, api_hash):
    client = get_client(api_id, api_hash)
    await client.connect()
    try:
        await client.log_out()
    finally:
        await client.disconnect()

# == UI Logics ==

# 1. Login State check
has_valid_creds = bool(st.session_state.api_id and str(st.session_state.api_id).strip() and 
                      st.session_state.api_hash and str(st.session_state.api_hash).strip())

if has_valid_creds:
    try:
        is_auth = run_async(check_auth(st.session_state.api_id, st.session_state.api_hash))
        st.session_state.is_authorized = is_auth
    except Exception as e:
        st.session_state.is_authorized = False
        st.session_state.auth_msg = f"Baglanti Hatasi: {e}"

if not st.session_state.is_authorized:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🔐 Telegram API Baglantisi")
    st.caption("Verileri @borsabilgibot uzerinden cekebilmemiz icin kisisel Telegram API ID ve Hash bilgilerinize ihtiyacimiz var. Bu bilgiler sadece burada, kendi cihazinizda tutulur.")
    st.markdown("API ID almak icin [my.telegram.org](https://my.telegram.org)'a girip 'API Development tools' bolumunden uygulama olusturun.")
    
    with st.form("auth_form"):
        api_id = st.text_input("API ID", value=st.session_state.api_id)
        api_hash = st.text_input("API HASH", value=st.session_state.api_hash)
        phone = st.text_input("Telefon Numarasi", value=st.session_state.phone, placeholder="+905xxxxxxxxx")
        submit_btn = st.form_submit_button("Dogrulama Kodu Gonder", type="primary")
        
        if submit_btn:
            if api_id and api_hash and phone:
                st.session_state.api_id = api_id
                st.session_state.api_hash = api_hash
                st.session_state.phone = phone
                res = run_async(send_code(api_id, api_hash, phone))
                
                if res["status"] in ["success"]:
                    st.session_state.awaiting_code = True
                    st.session_state.phone_code_hash = res.get("phone_code_hash", "")
                elif res["status"] == "already_auth":
                    st.session_state.awaiting_code = False
                    st.session_state.is_authorized = True
                
                st.session_state.auth_msg = res["msg"]
                st.rerun()
            else:
                st.error("Lutfen tum alanlari doldurun.")
                
    if st.session_state.auth_msg:
        st.info(st.session_state.auth_msg)
        
    if st.session_state.awaiting_code:
        st.divider()
        with st.form("code_form"):
            code = st.text_input("Telegramdan veya SMS'ten gelen 5 haneli kod")
            code_btn = st.form_submit_button("Giris Yap", type="primary")
            if code_btn and code:
                res = run_async(sign_in(st.session_state.api_id, st.session_state.api_hash, st.session_state.phone, code, st.session_state.phone_code_hash))
                if res["status"] == "success":
                    st.session_state.is_authorized = True
                    st.session_state.awaiting_code = False
                
                st.session_state.auth_msg = res["msg"]
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # 2. Main Derinlik Interface
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Derinlik Getir")
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker = st.text_input("Hisse Kodu Girin", placeholder="Orn: THYAO, SASA")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("GETIR", type="primary", use_container_width=True)
        
    if search_btn and ticker:
        with st.spinner(f"{ticker} derinlik tablosu Telegramdan cekiiliyor... Lutfen bekleyin (Maks 15sn)"):
            result = run_async(get_derinlik(st.session_state.api_id, st.session_state.api_hash, ticker))
            
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"{ticker} derinlik verisi basariyla alindi.")
                if result.get("text"):
                    st.markdown(f"**Bot Yaniti:**\n\n```\n{result.get('text')}\n```")
                
                if result.get("media"):
                    st.image(result.get("media"), use_column_width=True, caption=f"{ticker} Derinlik Goruntusu")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Oturumu kapat butonu
    if st.button("❌ Oturumu Kapat", type="secondary"):
        run_async(log_out_client(st.session_state.api_id, st.session_state.api_hash))
        st.session_state.is_authorized = False
        st.session_state.api_id = ""
        st.session_state.api_hash = ""
        st.session_state.phone = ""
        st.session_state.phone_code_hash = ""
        st.session_state.client = None
        st.rerun()
