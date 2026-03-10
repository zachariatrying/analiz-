import json
import os

WATCHLIST_FILE = os.path.join(os.path.dirname(__file__), "watchlist.json")

def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        try:
            with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_watchlist(watchlist):
    try:
        with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(watchlist, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Watchlist save error: {e}")
