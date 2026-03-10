"""
Derinlik (AKD) Modulu
@borsabilgibot uzerinden kullanici hesabiyla (UserBot) derinlik verisi cekme.
"""
import streamlit as st
import asyncio
import os
import time
import pandas as pd
import yfinance as yf
import re
from datetime import datetime
try:
    from src.telegram_utils import send_telegram_alert
except ImportError:
    from telegram_utils import send_telegram_alert

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
if 'taban_data' not in st.session_state: st.session_state.taban_data = {}
if 'taban_last_update' not in st.session_state: st.session_state.taban_last_update = None
if 'monitoring_active' not in st.session_state: st.session_state.monitoring_active = False
if 'tg_alerts_enabled' not in st.session_state: st.session_state.tg_alerts_enabled = False

BIST100_TICKERS = [
    "AEFES", "AGHOL", "AKBNK", "AKCNS", "AKSA", "AKSEN", "ALARK", "ALBRK", "ALFAS", "ARCLK", "ASELS", "ASTOR", "ASUZU",
    "AYDEM", "BAGFS", "BERA", "BIMAS", "BRSAN", "BRYAT", "BUCIM", "CANTE", "CCOLA", "CIMSA", "CWENE", "DOAS", "DOHOL",
    "EGEEN", "EKGYO", "ENJSA", "ENKAI", "EREGL", "EUPWR", "FROTO", "GARAN", "GENIL", "GESAN", "GLYHO", "GSDHO", "GUBRF",
    "GWIND", "HALKB", "HEKTS", "IPEKE", "ISCTR", "ISMEN", "KARDMD", "KAYSE", "KCHOL", "KCAER", "KLSER", "KONTR", "KONYA",
    "KORDS", "KOZAA", "KOZAL", "KRDMD", "MAVI", "MGROS", "MIATK", "ODAS", "OTKAR", "OYAKC", "PENTA", "PETKM", "PGSUS",
    "QUAGR", "SAHOL", "SASA", "SAYAS", "SDTTR", "SISE", "SKBNK", "SMRTG", "SOKM", "TAVHL", "TCELL", "THYAO", "TKFEN",
    "TKNSA", "TMSN", "TOASO", "TSKB", "TTKOM", "TTRAK", "TUKAS", "TUPRS", "TURSG", "ULKER", "VAKBN", "VESBE", "VESTL",
    "YEOTK", "YKBNK", "YYLGD", "ZOREN"
]

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
        response_msg = ""
        media_path = None
        start_time = time.time()
        clicked_button = False
        
        # Basic polling loops
        while time.time() - start_time < 30:
            # Get last 2 messages from bot
            messages = await client.get_messages(target_bot, limit=2)
            
            for msg in messages:
                if not msg.out:
                    # Capture text unconditionally
                    current_text = msg.text or ""
                    
                    # If message has an image, download it and we are done
                    if msg.media:
                        file_loc = os.path.join(parent_dir, f"tmp_derinlik_{ticker}.jpg")
                        media_path = await client.download_media(msg, file=file_loc)
                        response_msg = current_text or "Derinlik grafiği başarıyla çekildi."
                        break
                        
                    # If no image yet, but the message has inline buttons and we haven't clicked one yet
                    if not clicked_button and hasattr(msg, 'buttons') and msg.buttons:
                        available_buttons = []
                        for row in msg.buttons:
                            for button in row:
                                if button.text:
                                    available_buttons.append(button.text)
                                    btn_text = button.text.lower()
                                    # Check if button matches our target action
                                    if any(kw in btn_text for kw in ["derinlik", "görüntü", "goruntu", "al", "sorgula"]):
                                        try:
                                            await button.click()
                                            clicked_button = True
                                            # Reset timeout since we just requested the image
                                            start_time = time.time()
                                        except Exception:
                                            pass
                        
                        # Add buttons to debug text
                        if available_buttons:
                            current_text += f"\n\n[Mevcut Butonlar: {', '.join(available_buttons)}]"
                            
                    response_msg = current_text

            if media_path:
                break
                
            await asyncio.sleep(1)
            
        if not media_path:
            if response_msg:
                return {"error": f"Bot resim göndermedi. Son durum:\n{response_msg}"}
            return {"error": "Bottan 30 saniye icinde hicbir yanit gelmedi."}
            
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

# == BIST Scanner Logics ==
def get_floor_stocks():
    """Scans BIST100 for stocks at/near floor price (-9.5% to -10.5%)"""
    tickers = [f"{t}.IS" for t in BIST100_TICKERS]
    try:
        data = yf.download(tickers, period="5d", progress=False, group_by='ticker')
        floor_stocks = []
        for full_ticker in tickers:
            try:
                if len(tickers) > 1:
                    df = data[full_ticker]
                else:
                    df = data
                
                if df.empty or len(df) < 2: continue
                
                last = float(df['Close'].dropna().iloc[-1])
                prev = float(df['Close'].dropna().iloc[-2])
                change = ((last - prev) / prev) * 100
                
                if change <= -9.4: # Floor threshold
                    floor_stocks.append({
                        "ticker": full_ticker.replace(".IS", ""),
                        "price": last,
                        "change": change
                    })
            except: continue
        return floor_stocks
    except Exception as e:
        st.error(f"Piyasa tarama hatası: {e}")
        return []

def parse_lot_from_text(text):
    """Attempt to extract lot number from bot text using regex"""
    if not text: return None
    # Look for patterns like "1.234.567" or "1234567" often near "bekleyen" or "lot"
    match = re.search(r'(\d{1,3}(?:\.\d{3})*)', text)
    if match:
        lot_str = match.group(1).replace(".", "")
        try: return int(lot_str)
        except: return None
    return None

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
    # 2. Main Interface with Tabs
    tab1, tab2 = st.tabs(["📊 Tekil Sorgu", "🤖 Taban Avcısı (Otomasyon)"])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Hisse Derinlik Getir")
        col1, col2 = st.columns([3, 1])
        with col1:
            ticker = st.text_input("Hisse Kodu Girin", placeholder="Orn: THYAO, SASA", key="manual_ticker")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_btn = st.button("GETIR", type="primary", use_container_width=True, key="manual_search")
            
        if search_btn and ticker:
            with st.spinner(f"{ticker} verileri Telegram'dan çekiliyor..."):
                result = run_async(get_derinlik(st.session_state.api_id, st.session_state.api_hash, ticker))
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"{ticker} verisi alındı.")
                    if result.get("media"):
                        st.image(result.get("media"), use_column_width=True)
                    if result.get("text"):
                        st.markdown(f"**Bot Yanıtı:**\n\n```\n{result.get('text')}\n```")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Taban Lot İzleme")
        st.caption("Bu mod, BIST'te taban olan hisseleri otomatik bulur ve Telegram üzerinden lot erimesini takip eder.")
        
        col_ctrl1, col_ctrl2 = st.columns(2)
        with col_ctrl1:
            if not st.session_state.monitoring_active:
                if st.button("▶️ OTOMASYONU BASLAT", type="primary", use_container_width=True):
                    st.session_state.monitoring_active = True
                    st.rerun()
            else:
                if st.button("⏹️ OTOMASYONU DURDUR", type="secondary", use_container_width=True):
                    st.session_state.monitoring_active = False
                    st.rerun()
        
        with col_ctrl2:
            interval = st.select_slider("Kontrol Aralığı (Dakika)", options=[1, 2, 5, 10, 15], value=5)
            st.session_state.tg_alerts_enabled = st.checkbox("Telegram Bildirimleri Gönder", value=st.session_state.tg_alerts_enabled)

        if st.session_state.monitoring_active:
            status_placeholder = st.empty()
            status_placeholder.info(f"Otomasyon aktif. {interval} dakikada bir kontrol ediliyor...")
            
            # Check if it's time to scan
            now = time.time()
            if st.session_state.taban_last_update is None or (now - st.session_state.taban_last_update) > (interval * 60):
                status_placeholder.warning("Piyasa taranıyor (Taban hisseler tespit ediliyor)...")
                floors = get_floor_stocks()
                st.session_state.taban_last_update = now
                
                if floors:
                    status_placeholder.info(f"{len(floors)} adet taban hisse bulundu. Telegram derinlik sorguları yapılıyor...")
                    for stock in floors:
                        t = stock['ticker']
                        res = run_async(get_derinlik(st.session_state.api_id, st.session_state.api_hash, t))
                        
                        lot_count = parse_lot_from_text(res.get("text", ""))
                        
                        # Notification for new floor stock
                        if t not in st.session_state.taban_data and st.session_state.tg_alerts_enabled:
                            send_telegram_alert(f"🚨 <b>YENİ TABAN HİSSE: {t}</b>\nFiyat: {stock['price']}\nDeğişim: %{stock['change']:.2f}")

                        # Compare with previous
                        prev_lot = st.session_state.taban_data.get(t, {}).get("lot", 0)
                        diff = 0
                        if prev_lot > 0 and lot_count is not None:
                            diff = lot_count - prev_lot
                            
                            # Notification for lot erosion (if decreased by more than 5%)
                            if diff < 0 and abs(diff) > (prev_lot * 0.05) and st.session_state.tg_alerts_enabled:
                                send_telegram_alert(f"🔥 <b>TABAN ERİMESİ: {t}</b>\nLotlar <b>{abs(diff):,}</b> adet azaldı!\nKalan Lot: <b>{lot_count:,}</b>\n<i>Hisse toplanıyor olabilir.</i>")
                            
                        st.session_state.taban_data[t] = {
                            "price": stock['price'],
                            "change": stock['change'],
                            "lot": lot_count,
                            "diff": diff,
                            "last_sync": datetime.now().strftime("%H:%M:%S"),
                            "raw_text": res.get("text", "")
                        }
                else:
                    status_placeholder.success("Şu an tabanda hisse bulunamadı.")
            
            # Display results
            if st.session_state.taban_data:
                for t, data in st.session_state.taban_data.items():
                    diff_str = ""
                    if data['diff'] < 0:
                        diff_str = f"🔴 Lot Erimesi: {abs(data['diff']):,} lot azaldı!"
                    elif data['diff'] > 0:
                        diff_str = f"⚪ Lot Artışı: {data['diff']:,} lot eklendi."
                        
                    st.markdown(f"""
                    <div style="padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; margin-bottom:10px; border-left:4px solid {'#ef4444' if data['diff'] >= 0 else '#22c55e'}">
                        <div style="display:flex; justify-content:space-between;">
                            <strong style="font-size:1.1rem; color:#e2e8f0;">{t}</strong>
                            <span style="color:#64748b; font-size:0.8rem;">Son Sync: {data['last_sync']}</span>
                        </div>
                        <div style="color:#94a3b8; font-size:0.9rem;">
                            Fiyat: {data['price']} (%{data['change']:.2f}) | 
                            <b>Kilitli Lot: {data['lot']:, if data['lot'] else 'Bilinmiyor'}</b>
                        </div>
                        <div style="color:{'#f87171' if data['diff'] >= 0 else '#4ade80'}; font-weight:bold; margin-top:4px;">
                            {diff_str}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Auto refresh trick for Streamlit
            time.sleep(10)
            st.rerun()

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
