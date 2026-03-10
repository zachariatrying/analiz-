"""
Piyasa Haberleri
BIST hisselerine ait guncel haberler ve sentiment analizi
"""
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Haberler", page_icon="", layout="wide")

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

POSITIVE_WORDS = ['yukselis', 'kar', 'rekor', 'basari', 'artti', 'artis', 'yuksek', 'olumlu',
                  'buyume', 'kazanc', 'gain', 'rise', 'profit', 'growth', 'surge', 'rally',
                  'positive', 'boost', 'upgrade', 'beat', 'record', 'high', 'strong', 'bull']
NEGATIVE_WORDS = ['dusus', 'zarar', 'kayip', 'azaldi', 'dusuk', 'olumsuz', 'risk', 'kriz',
                  'loss', 'decline', 'drop', 'fall', 'crash', 'bear', 'sell', 'weak',
                  'downgrade', 'miss', 'concern', 'fear', 'inflation', 'recession']

def simple_sentiment(text):
    """Basit kelime bazli sentiment analizi."""
    text_lower = text.lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in text_lower)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
    if pos > neg: return "Pozitif", "sentiment-positive"
    elif neg > pos: return "Negatif", "sentiment-negative"
    else: return "Notr", "sentiment-neutral"

@st.cache_data(ttl=600)
def get_stock_news(ticker):
    """yfinance ile hisse haberlerini cek."""
    try:
        symbol = f"{ticker}.IS" if not ticker.endswith(".IS") else ticker
        stock = yf.Ticker(symbol)
        news = stock.news
        if not news:
            return []
        results = []
        for item in news[:15]:
            content = item.get('content', {})
            title = content.get('title', item.get('title', ''))
            summary = content.get('summary', '')
            provider = content.get('provider', {})
            provider_name = provider.get('displayName', '') if isinstance(provider, dict) else str(provider)
            pub_date = content.get('pubDate', '')
            link = content.get('canonicalUrl', {})
            url = link.get('url', '') if isinstance(link, dict) else ''

            if not title:
                continue

            sentiment, css_class = simple_sentiment(title + ' ' + summary)

            results.append({
                'title': title,
                'summary': summary,
                'publisher': provider_name,
                'date': pub_date,
                'url': url,
                'sentiment': sentiment,
                'css_class': css_class,
            })
        return results
    except:
        return []

st.markdown("""
<div style="text-align:center; padding:10px 0 24px 0;">
    <h1 style="font-size:2.2rem; font-weight:800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom:4px;">
        Piyasa Haberleri
    </h1>
    <p style="color:#64748b; font-size:0.95rem;">Hisse bazli haberler ve sentiment analizi</p>
</div>
""", unsafe_allow_html=True)

# --- Hisse Secimi ---
col1, col2 = st.columns([3, 1])
with col1:
    haber_hisse = st.text_input("Hisse Kodu", "THYAO", placeholder="Orn: THYAO, GARAN, ASELS")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    btn_haber = st.button("HABERLERI GETIR", type="primary", use_container_width=True)

# Birden fazla hisse
hisse_list = [h.strip().upper() for h in haber_hisse.split(',') if h.strip()]

# Populer hisseler
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("##### Populer Hisseler")
pop_cols = st.columns(6)
popular = ["THYAO", "GARAN", "ASELS", "EREGL", "SASA", "BIMAS"]
for col, ticker in zip(pop_cols, popular):
    with col:
        if st.button(ticker, key=f"pop_{ticker}", use_container_width=True):
            hisse_list = [ticker]
            btn_haber = True
st.markdown('</div>', unsafe_allow_html=True)

if btn_haber:
    for hisse in hisse_list:
        st.divider()
        st.markdown(f"### {hisse} Haberleri")

        with st.spinner(f"{hisse} haberleri yukleniyor..."):
            news = get_stock_news(hisse)

        if not news:
            st.info(f"{hisse} icin haber bulunamadi.")
        else:
            # Sentiment ozeti
            sentiments = [n['sentiment'] for n in news]
            pos_count = sentiments.count('Pozitif')
            neg_count = sentiments.count('Negatif')
            notr_count = sentiments.count('Notr')

            if pos_count > neg_count:
                overall = "Genel Olumlu"
                overall_color = "#4ade80"
            elif neg_count > pos_count:
                overall = "Genel Olumsuz"
                overall_color = "#f87171"
            else:
                overall = "Genel Notr"
                overall_color = "#94a3b8"

            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:12px;">
                <span style="color:{overall_color}; font-weight:700; font-size:1.1rem;">{overall}</span>
                <span style="color:#475569;"> | </span>
                <span style="color:#4ade80;">{pos_count} Pozitif</span>
                <span style="color:#475569;"> | </span>
                <span style="color:#f87171;">{neg_count} Negatif</span>
                <span style="color:#475569;"> | </span>
                <span style="color:#94a3b8;">{notr_count} Notr</span>
            </div>
            """, unsafe_allow_html=True)

            # Haber kartlari
            for item in news:
                date_str = ""
                if item['date']:
                    try:
                        dt = datetime.fromisoformat(item['date'].replace('Z', '+00:00'))
                        date_str = dt.strftime('%d.%m.%Y %H:%M')
                    except:
                        date_str = item['date'][:16] if len(item['date']) > 16 else item['date']

                url_link = f'<a href="{item["url"]}" target="_blank" style="color:#818cf8; text-decoration:none; font-size:0.8rem;">Haberi oku</a>' if item['url'] else ''

                st.markdown(f"""
                <div class="news-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div style="flex:1;">
                            <div style="color:#e2e8f0; font-weight:600; font-size:0.95rem; margin-bottom:4px;">{item['title']}</div>
                            <div style="color:#64748b; font-size:0.8rem;">
                                {item['publisher']} {(' | ' + date_str) if date_str else ''} {(' | ' + url_link) if url_link else ''}
                            </div>
                        </div>
                        <span class="{item['css_class']}" style="font-size:0.8rem; white-space:nowrap; margin-left:12px;">{item['sentiment']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:20px 0; color:#475569; font-size:0.8rem;">
    Haberler yfinance uzerinden cekilmektedir. Sentiment analizi basit kelime bazlidir.
</div>
""", unsafe_allow_html=True)

