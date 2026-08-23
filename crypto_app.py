import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="◆",
    layout="wide",
)

ACCENT = "#4F46E5"
GREEN = "#059669"
RED = "#DC2626"
INK = "#111827"
MUTED = "#6B7280"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Schibsted Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

.stApp {{
    background-color: #F7F8FA;
    color: {INK};
}}

#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent; }}

.block-container {{
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}}

.app-header {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.6rem;
}}

.app-title {{
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: {INK};
    margin: 0;
}}

.app-title .accent {{ color: {ACCENT}; }}

.last-updated {{
    font-size: 0.82rem;
    font-weight: 500;
    color: {MUTED};
}}

.section-label {{
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: {INK};
    margin: 1.8rem 0 0.7rem 0;
}}

.metric-card {{
    background: #FFFFFF;
    border: 1px solid #EAECF0;
    border-radius: 16px;
    padding: 1.15rem 1.35rem;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04), 0 4px 12px rgba(16, 24, 40, 0.04);
    height: 100%;
}}

.metric-card .metric-label {{
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {MUTED};
    margin-bottom: 0.45rem;
}}

.metric-card .metric-value {{
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: {INK};
    font-variant-numeric: tabular-nums;
}}

.metric-card .metric-delta {{
    display: inline-block;
    margin-top: 0.5rem;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.18rem 0.6rem;
    border-radius: 999px;
    font-variant-numeric: tabular-nums;
}}

.pill-up {{ background: #ECFDF5; color: {GREEN}; }}
.pill-down {{ background: #FEF2F2; color: {RED}; }}

.chart-card {{
    background: #FFFFFF;
    border: 1px solid #EAECF0;
    border-radius: 16px;
    padding: 1rem 1rem 0.4rem 1rem;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04), 0 4px 12px rgba(16, 24, 40, 0.04);
}}

.chart-title {{
    font-size: 0.9rem;
    font-weight: 700;
    color: {INK};
    padding-left: 0.5rem;
}}

div[data-testid="stSidebar"] {{
    background-color: #FFFFFF;
    border-right: 1px solid #EAECF0;
}}

.sidebar-heading {{
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {MUTED};
    margin-bottom: 1rem;
}}

.error-card {{
    background: #FEF2F2;
    border: 1px solid #FECACA;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}}

.error-card h3 {{
    color: {RED};
    font-weight: 700;
    margin: 0 0 0.4rem 0;
}}

.error-card p {{
    color: {MUTED};
    font-size: 0.9rem;
    margin: 0 0 1.2rem 0;
}}
</style>
"""


def render_css():
    st.markdown(CSS, unsafe_allow_html=True)


def fetch_crypto_data(per_page):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def format_compact(value):
    for unit, divisor in (("T", 1e12), ("B", 1e9), ("M", 1e6)):
        if abs(value) >= divisor:
            return f"${value / divisor:.2f}{unit}"
    return f"${value:,.0f}"


def metric_card(label, value, delta=None):
    delta_html = ""
    if delta is not None:
        cls = "pill-up" if delta >= 0 else "pill-down"
        arrow = "&#9650;" if delta >= 0 else "&#9660;"
        delta_html = f'<span class="metric-delta {cls}">{arrow} {abs(delta):.2f}%</span>'
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_table(df):
    table = df[[
        "name", "symbol", "current_price", "market_cap",
        "total_volume", "price_change_percentage_24h",
    ]].copy()
    table.insert(0, "#", range(1, len(table) + 1))
    table.columns = [
        "#", "Name", "Symbol", "Price", "Market Cap", "Volume (24h)", "Change (24h)",
    ]
    table["Symbol"] = table["Symbol"].str.upper()

    def color_change(val):
        color = GREEN if val >= 0 else RED
        sign = "+" if val >= 0 else ""
        return f"color: {color}; font-weight: 600"

    styler = table.style.map(color_change, subset=["Change (24h)"])
    styler = styler.format({
        "Price": lambda v: f"${v:,.2f}",
        "Market Cap": format_compact,
        "Volume (24h)": format_compact,
        "Change (24h)": lambda v: f"{v:+.2f}%",
    })
    return styler


def style_figure(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Schibsted Grotesk, sans-serif", size=12, color=MUTED),
        margin=dict(l=10, r=10, t=48, b=10),
        hovermode="closest",
    )
    fig.update_xaxes(gridcolor="#EEF0F3", zeroline=False)
    fig.update_yaxes(gridcolor="#EEF0F3", zeroline=False)
    return fig


def price_chart(df):
    fig = px.bar(
        df.sort_values("current_price"),
        x="current_price",
        y="name",
        orientation="h",
        color="price_change_percentage_24h",
        color_continuous_scale=[RED, "#F59E0B", GREEN],
        labels={"current_price": "", "name": ""},
    )
    fig.update_coloraxes(
        colorbar=dict(title="24h %", thickness=10, len=0.7),
    )
    fig.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>$%{x:,.2f}<extra></extra>",
    )
    fig.update_xaxes(type="log")
    return style_figure(fig)


def market_cap_chart(df):
    fig = px.pie(
        df,
        values="market_cap",
        names="symbol",
        hole=0.55,
        color_discrete_sequence=["#312E81", "#4338CA", "#4F46E5", "#6366F1", "#818CF8", "#A5B4FC", "#C7D2FE"],
        labels={"market_cap": "", "symbol": ""},
    )
    fig.update_traces(
        textinfo="none",
        marker=dict(line=dict(color="#FFFFFF", width=2)),
        hovertemplate="<b>%{label}</b><br>Market cap: $%{value:,.0f} (%{percent})<extra></extra>",
    )
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Schibsted Grotesk, sans-serif", size=12, color=MUTED),
        margin=dict(l=10, r=10, t=48, b=10),
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, title="Symbol"),
    )
    return fig


def render_error_state():
    st.markdown(
        """
        <div class="error-card">
            <h3>Couldn't reach CoinGecko</h3>
            <p>The API may be rate-limited or temporarily unavailable.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Retry", type="primary"):
        st.rerun()


def render_sidebar():
    with st.sidebar:
        st.markdown('<p class="sidebar-heading">Settings</p>', unsafe_allow_html=True)
        coin_count = st.selectbox("Coins to show", [5, 10, 25, 50], index=1)
        auto_refresh = st.checkbox("Auto-refresh", value=False)
        refresh_interval = st.slider("Refresh interval (seconds)", 10, 120, 30)
        st.caption(f"Last updated {datetime.now().strftime('%H:%M:%S')}")
    return coin_count, auto_refresh, refresh_interval


def main():
    render_css()
    coin_count, auto_refresh, refresh_interval = render_sidebar()

    st.markdown(
        f"""
        <div class="app-header">
            <h1 class="app-title">Crypto<span class="accent">Pulse</span></h1>
            <span class="last-updated">Live prices &middot; powered by CoinGecko</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    data = fetch_crypto_data(coin_count)

    if not data:
        render_error_state()
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()
        return

    df = pd.DataFrame(data)
    avg_change = df["price_change_percentage_24h"].mean()

    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Total Market Cap", format_compact(df["market_cap"].sum()))
    with col2:
        metric_card("Total Volume (24h)", format_compact(df["total_volume"].sum()))
    with col3:
        metric_card("Avg Change (24h)", f"{avg_change:+.2f}%", delta=avg_change)

    st.markdown("<p class='section-label'>Top Cryptocurrencies</p>", unsafe_allow_html=True)
    st.dataframe(
        build_table(df),
        use_container_width=True,
        hide_index=True,
        height=min(35 * (len(df) + 1), 520),
    )

    chart_col, donut_col = st.columns([3, 2])
    with chart_col:
        st.markdown("<p class='section-label'>Current Prices</p>", unsafe_allow_html=True)
        st.plotly_chart(price_chart(df), use_container_width=True)
    with donut_col:
        st.markdown("<p class='section-label'>Market Cap Distribution</p>", unsafe_allow_html=True)
        st.plotly_chart(market_cap_chart(df), use_container_width=True)

    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()


if __name__ == "__main__":
    main()
