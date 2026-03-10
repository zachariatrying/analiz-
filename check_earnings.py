import yfinance as yf
import pandas as pd

def check_earnings():
    tickers = ['THYAO.IS', 'ASTOR.IS', 'REEDR.IS']
    for t in tickers:
        print(f"\n--- {t} ---")
        try:
            stock = yf.Ticker(t)
            # Try different methods
            cal = stock.calendar
            print("Calendar:")
            print(cal)
            
            earnings = stock.earnings_dates
            print("\nEarnings Dates:")
            if earnings is not None and not earnings.empty:
                print(earnings.head())
            else:
                print("No earnings dates found via earnings_dates")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_earnings()
