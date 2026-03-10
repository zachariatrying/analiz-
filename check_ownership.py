import yfinance as yf

def check_ownership():
    tickers = ['ASTOR.IS', 'THYAO.IS', 'GARAN.IS']
    for t in tickers:
        print(f"\n--- {t} ---")
        try:
            stock = yf.Ticker(t)
            print("Major Holders:")
            print(stock.major_holders)
            print("\nInstitutional Holders:")
            print(stock.institutional_holders)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_ownership()
