import requests
import json
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

def send_telegram_alert(message):
    """Sends a message using the configured Telegram bot."""
    config = load_tg_config()
    token = config.get("token")
    chat_id = config.get("chat_id")
    
    if not token or not chat_id:
        return False, "Telegram ayarları eksik."
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        return resp.status_code == 200, resp.json()
    except Exception as e:
        return False, str(e)
