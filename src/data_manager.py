import pandas as pd
import datetime
import streamlit as st
import threading
import sys
import os

class DataManager:
    _lock = threading.Lock() # Shared lock across instances (though we usually have one)

    def __init__(self):
        import json
        
        # Add local tvDatafeed to path
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            lib_path = os.path.join(parent_dir, "tvdatafeed_lib", "tvdatafeed-main")
            if lib_path not in sys.path:
                sys.path.append(lib_path)
            
            from tvDatafeed import TvDatafeed
            self.tv = TvDatafeed()
            # print("TradingView Datafeed Initialized.")
        except Exception as e:
            print(f"Error initializing tvDatafeed: {e}")
            self.tv = None

        # Try to load full BIST list
        try:
            file_path = os.path.join(current_dir, 'bist_tickers.json')
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.sample_ipos = json.load(f)
            else:
                self.sample_ipos = self._get_fallback_list()
        except Exception as e:
            print(f"Error loading ticker list: {e}")
            self.sample_ipos = self._get_fallback_list()

    def _get_fallback_list(self):
        # Default to BIST 30 for safety if file missing
        return self.get_bist30_tickers()

    def get_bist30_tickers(self):
        """Returns BIST 30 Tickers (High Quality)"""
        tickers = [
            "AKBNK.IS", "ALARK.IS", "ARCLK.IS", "ASELS.IS", "ASTOR.IS", "BIMAS.IS", "BRSAN.IS",
            "DOAS.IS", "EKGYO.IS", "ENKAI.IS", "EREGL.IS", "FROTO.IS", "GARAN.IS", "GUBRF.IS",
            "HEKTS.IS", "ISCTR.IS", "KCHOL.IS", "KONTR.IS", "KOZAL.IS", "KRDMD.IS", "ODAS.IS",
            "OYAKC.IS", "PETKM.IS", "PGSUS.IS", "SAHOL.IS", "SASA.IS", "SISE.IS", "TCELL.IS",
            "THYAO.IS", "TOASO.IS", "TSKB.IS", "TUPRS.IS", "YKBNK.IS"
        ]
        return [{'ticker': t, 'name': t.replace('.IS', ''), 'date': '2000-01-01'} for t in tickers]

    def get_bist100_tickers(self):
        """Returns BIST 100 Tickers (Expanded High Quality)"""
        # A broader list including BIST 30 and other stars
        bist30 = [t['ticker'] for t in self.get_bist30_tickers()]
        others = [
            "AEFES.IS", "AGHOL.IS", "AHGAZ.IS", "AKFGY.IS", "AKSA.IS", "AKSEN.IS", "ALBRK.IS",
            "ALFAS.IS", "ANHYT.IS", "ANSGR.IS", "ASGYO.IS", "AYDEM.IS", "BAGFS.IS", "BERA.IS",
            "BIOEN.IS", "BRISA.IS", "CANTE.IS", "CCOLA.IS", "CEMTS.IS", "CIMSA.IS", "CWENE.IS",
            "DOHOL.IS", "ECILC.IS", "EGEEN.IS", "ECZYT.IS", "EUPWR.IS", "EUREN.IS", "FUBUT.IS", # FUBUT replacement/proxy? kept populars
            "GENIL.IS", "GESAN.IS", "GLYHO.IS", "GSDHO.IS", "GWIND.IS", "HALKB.IS", "ISDMR.IS",
            "ISGYO.IS", "ISMEN.IS", "IZMDC.IS", "KARSN.IS", "KAYSE.IS", "KCAER.IS", "KMPUR.IS",
            "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "MAVI.IS", "MGROS.IS", "MIATK.IS",
            "ODAS.IS", "OTKAR.IS", "OYAKC.IS", "PENTA.IS", "QUAGR.IS", "REEDR.IS", "RTALB.IS",
            "SDTTR.IS", "SKBNK.IS", "SMRTG.IS", "SOKM.IS", "TABGD.IS", "TAVHL.IS", "TKFEN.IS",
            "TMSN.IS", "TTKOM.IS", "TURSG.IS", "ULKER.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS",
            "YEOTK.IS", "YKBNK.IS", "YYLGD.IS", "ZOREN.IS"
        ]
        all_tickers = sorted(list(set(bist30 + others)))
        return [{'ticker': t, 'name': t.replace('.IS', ''), 'date': '2000-01-01'} for t in all_tickers]


    def get_ipo_list(self, sort_by='Date (Newest)', search_query=''):
        """Returns a dataframe of IPOs for BIST with sorting and filtering."""
        df = pd.DataFrame(self.sample_ipos)
        
        # Filtering
        if search_query:
            search_query = search_query.lower()
            df = df[df['name'].str.lower().str.contains(search_query) | 
                    df['ticker'].str.lower().str.contains(search_query)]
        
        # Sorting
        if sort_by == 'Date (Newest)':
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date', ascending=False)
        elif sort_by == 'Date (Oldest)':
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date', ascending=True)
        elif sort_by == 'Name (A-Z)':
            df = df.sort_values(by='name', ascending=True)
        elif sort_by == 'Name (Z-A)':
            df = df.sort_values(by='name', ascending=False)
            
        elif sort_by == 'Name (Z-A)':
            df = df.sort_values(by='name', ascending=False)
            
        return df

    def get_viop_list(self):
        """Returns a list of BIST 30 / VIOP tickers."""
        # Major BIST 30 companies usually in VIOP
        viop_tickers = [
            'AKBNK.IS', 'ALARK.IS', 'ARCLK.IS', 'ASELS.IS', 'ASTOR.IS',
            'BIMAS.IS', 'BRSAN.IS', 'EKGYO.IS', 'ENKAI.IS', 'EREGL.IS',
            'FROTO.IS', 'GARAN.IS', 'GUBRF.IS', 'HEKTS.IS', 'ISCTR.IS',
            'KCHOL.IS', 'KONTR.IS', 'KOZAL.IS', 'KRDMD.IS', 'ODAS.IS',
            'OYAKC.IS', 'PETKM.IS', 'PGSUS.IS', 'SAHOL.IS', 'SASA.IS',
            'SISE.IS', 'TCELL.IS', 'THYAO.IS', 'TOASO.IS', 'TUPRS.IS',
            'YKBNK.IS'
        ]
        return viop_tickers

    # @st.cache_data(ttl=3600) # Disable ST Cache for Thread Safety
    def fetch_stock_data(self, ticker, start_date=None, interval='1d', currency='TRY'):
        """
        Fetches historical data with SMART DISK CACHING and optional USD conversion.
        """
        import os
        import time
        from datetime import datetime, timedelta

        # Cache Directory
        CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'market_data_cache')
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
            
        # File Path
        safe_ticker = ticker.replace('.IS', '')
        file_path = os.path.join(CACHE_DIR, f"{safe_ticker}_{interval}_{currency}.parquet")
        
        # --- LIVE FETCH ---
        try:
            if self.tv is None:
                return None
                
            from tvDatafeed import Interval
            tv_interval = Interval.in_daily
            if interval == '1h': tv_interval = Interval.in_1_hour
            elif interval == 'W': tv_interval = Interval.in_weekly
            elif interval == 'M': tv_interval = Interval.in_monthly
            
            clean_symbol = ticker.replace('.IS', '')
            df = self.tv.get_hist(symbol=clean_symbol, exchange='BIST', interval=tv_interval, n_bars=500)
                
            if df is None or df.empty:
                return None
            
            df.rename(columns={'open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'}, inplace=True)
            
            # --- USD CONVERSION ---
            if currency == 'USD':
                try:
                    # Ensure both dataframes have 'datetime' as index for joining
                    df.set_index('datetime', inplace=True)
                    
                    usd_df = self.tv.get_hist(symbol='USDTRY', exchange='FX_IDC', interval=tv_interval, n_bars=500)
                    if usd_df is not None and not usd_df.empty:
                        usd_df.rename(columns={'close': 'USDTRY'}, inplace=True)
                        usd_df.set_index('datetime', inplace=True)
                        df = df.join(usd_df['USDTRY'], how='left')
                        df['USDTRY'] = df['USDTRY'].ffill().bfill()
                        for col in ['Open', 'High', 'Low', 'Close']:
                            df[col] = df[col] / df['USDTRY']
                except Exception as e:
                    print(f"USD conversion error: {e}")

            df.reset_index(inplace=True)
            if 'datetime' in df.columns:
                df.rename(columns={'datetime': 'Date'}, inplace=True)
            
            # --- WRITE TO CACHE ---
            try:
                df.to_parquet(file_path, index=False)
            except:
                pass 
                
            return df
        except Exception as e:
            print(f"Error fetching data from TradingView for {ticker}: {e}")
            return None

    @st.cache_data
    def fetch_ownership_stats(_self, ticker):
        """Ownership stats removed as target source is now TradingView OHLCV."""
        return None


    def fetch_multiple_tickers(self, tickers):
        """Fetches data for multiple tickers (useful for pattern matching)."""
        data = {}
        for ticker in tickers:
            df = self.fetch_stock_data(ticker)
            if df is not None:
                data[ticker] = df
        return data

    def get_sector_map(self):
        """Returns a dictionary mapping Tickers to Sector Names."""
        # Manual mapping for major BIST stocks
        sectors = {
            "Bankacılık": ["AKBNK.IS", "GARAN.IS", "ISCTR.IS", "YKBNK.IS", "HALKB.IS", "VAKBN.IS", "TSKB.IS", "ALBRK.IS", "SKBNK.IS", "QNBFB.IS"],
            "Holding": ["KCHOL.IS", "SAHOL.IS", "DOHOL.IS", "AGHOL.IS", "ALARK.IS", "TEKTU.IS", "GSDHO.IS", "IHLAS.IS", "POLHO.IS", "BERA.IS", "TKFEN.IS"],
            "Sanayi & Metal": ["EREGL.IS", "KRDMD.IS", "ISDMR.IS", "TUPRS.IS", "PETKM.IS", "KOZAL.IS", "KOZAA.IS", "IPEKE.IS", "CIMSA.IS", "OYAKC.IS", "BUCIM.IS", "BSOKE.IS", "KCAER.IS"],
            "Otomotiv": ["FROTO.IS", "TOASO.IS", "DOAS.IS", "TTRAK.IS", "KARSN.IS", "OTKAR.IS", "TMSN.IS", "ASUZU.IS"],
            "Enerji": ["ASTOR.IS", "ENKAI.IS", "ODAS.IS", "AKSEN.IS", "ZOREN.IS", "AYDEM.IS", "BIOEN.IS", "HUNER.IS", "SMRTG.IS", "EUPWR.IS", "GWIND.IS", "YEOTK.IS", "ALFAS.IS", "CWENE.IS", "AKFYE.IS", "ENJSA.IS", "AENER.IS"],
            "GYO (Gayrimenkul)": ["EKGYO.IS", "ISGYO.IS", "TRGYO.IS", "AKFGY.IS", "SNGYO.IS", "OZKGY.IS", "HLGYO.IS", "ASGYO.IS", "KLGYO.IS"],
            "Ulaştırma": ["THYAO.IS", "PGSUS.IS", "TAVHL.IS", "CLEBI.IS", "RYSAS.IS", "TLMAN.IS"],
            "Gıda & Perakende": ["BIMAS.IS", "MGROS.IS", "SOKM.IS", "ULKER.IS", "CCOLA.IS", "AEFES.IS", "TUKAS.IS", "TATGD.IS", "KRYST.IS", "PETUN.IS", "SUWEN.IS"],
            "Teknoloji & Yazılım": ["KONTR.IS", "MIATK.IS", "ASELS.IS", "PENTA.IS", "LOGO.IS", "ARDYZ.IS", "VBTYZ.IS", "NETAS.IS", "KFEIN.IS", "SMART.IS", "SDTTR.IS", "REEDR.IS"],
            "Dayanıklı Tüketim": ["ARCLK.IS", "VESBE.IS", "VESTL.IS"],
            "Cam & Seramik": ["SISE.IS", "KLMSN.IS", "EGSER.IS", "KUTPO.IS"],
            "İletişim": ["TCELL.IS", "TTKOM.IS"],
            "Sigorta": ["TURSG.IS", "AKGRT.IS", "ANHYT.IS", "ANSGR.IS"],
        }
        
        # Invert to Ticker -> Sector
        ticker_map = {}
        for sec, ticks in sectors.items():
            for t in ticks:
                ticker_map[t] = sec
        
        return ticker_map
