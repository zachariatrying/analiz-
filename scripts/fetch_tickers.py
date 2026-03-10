import requests
import json
import os

def fetch_bist_tickers():
    url = "https://raw.githubusercontent.com/ahmeterenodaci/Istanbul-Stock-Exchange--BIST--including-symbols-and-logos/master/bist.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            cleaned_data = []
            for item in data:
                symbol = item.get('symbol') or item.get('code')
                name = item.get('name')
                
                if symbol:
                    # Clean symbol
                    symbol = symbol.strip().upper()
                    # Remove any existing .IS or strange chars if needed
                    ticker = f"{symbol}.IS"
                    
                    cleaned_data.append({
                        'ticker': ticker,
                        'name': name,
                        'date': '2000-01-01' # Dummy date for sorting compatibility
                    })
            
            # Save to src folder
            os.makedirs('src', exist_ok=True)
            with open('src/bist_tickers.json', 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
            
            print(f"Successfully saved {len(cleaned_data)} tickers to src/bist_tickers.json")
        else:
            print("Failed to fetch data")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_bist_tickers()

