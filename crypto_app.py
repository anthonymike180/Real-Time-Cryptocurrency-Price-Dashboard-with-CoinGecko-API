import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="💰",
    layout="wide"
)

# Title
st.title("🚀 Real-Time Cryptocurrency Dashboard")

# Sidebar controls
st.sidebar.header("⚙️ Settings")
auto_refresh = st.sidebar.checkbox("Auto-refresh", value=False)
refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 10, 120, 30)

# Fetch data function (same as before)
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None

# Main dashboard
def display_dashboard():
    # Show last update time
    st.sidebar.write(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    # Fetch data
    data = fetch_crypto_data()
    
    if not data:
        st.error("Failed to fetch data")
        return
    
    df = pd.DataFrame(data)
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Market Cap",
            f"${df['market_cap'].sum():,.0f}"
        )
    
    with col2:
        st.metric(
            "Total Volume",
            f"${df['total_volume'].sum():,.0f}"
        )
    
    with col3:
        avg_change = df['price_change_percentage_24h'].mean()
        st.metric(
            "Avg Price Change",
            f"{avg_change:.2f}%",
            delta=f"{avg_change:.2f}%"
        )
    
    # Display table
    st.subheader("📊 Top 10 Cryptocurrencies")
    display_df = df[['name', 'symbol', 'current_price', 'market_cap', 
                     'total_volume', 'price_change_percentage_24h']].copy()
    display_df.columns = ['Name', 'Symbol', 'Price (USD)', 'Market Cap', 
                          'Volume (24h)', 'Change (24h) %']
    st.dataframe(display_df, use_container_width=True)
    
    # Display charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(df, x='name', y='current_price', 
                      title='Current Prices',
                      color='price_change_percentage_24h',
                      color_continuous_scale=['red', 'yellow', 'green'])
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.pie(df, values='market_cap', names='name', 
                      title='Market Cap Distribution', hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

# Run dashboard
display_dashboard()

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()