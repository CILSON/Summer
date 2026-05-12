from Charts.Candle_chart import Candle_chart
from Charts.Line_Chart import Line_chart

from Data.hist_data import fetch_historical_data
from Data.bybit import fetch_historical_data1 

import streamlit as st
from datetime import datetime

# =================================
# LOAD CSS
# =================================

def load_css():
    with open("Style/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()


# =================================
# TITLE AND PAGE CONFIG
# =================================

st.set_page_config(layout="wide")
st.title('Personalised Crypto Dashboard')

coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT']
timeframes = ['5m', '15m', '1h', '4h', '1d', '1M', '1w']

col1,  col2, col3 = st.columns([1,1,1])

with col1:
    selected_coin = st.selectbox(
        "Select Coin", 
        coins
        )


with col2:
    selected_timeframe = st.selectbox(
        "Select Timeframe", 
        timeframes
        )


with col3:
    chart = st.selectbox(
        "How would you like to visualize the price data?",
        ("Candle", "Line"),
        index=None,
        placeholder="Select the type of Chart to Visualize"
    )


# =================================
# LIVE PRICE
# =================================

@st.fragment(run_every='2s')
def live():

    df = fetch_historical_data(selected_coin, selected_timeframe, limit=5)
    
    if df.empty or len(df) < 2:
        st.warning("Not enough market data")
        st.stop()

    latest = float(df['Close'].iloc[0])
    previous = float(df['Close'].iloc[1])
    change = ((latest / previous) - 1) * 100

    st.metric(
        label=f"{selected_coin} Price Binance",
        value=f"${latest:,.2f}",
        delta=f"{change:.2f}%"
    )
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


live()


@st.fragment(run_every='2s')
def live1():

    df = fetch_historical_data1(selected_coin, selected_timeframe)

    if df.empty or len(df) < 2:
        st.warning("Bybit comparison temporarily unavailable")
        return

    latest = float(df['Close'].iloc[0])
    previous = float(df['Close'].iloc[1])
    change = ((latest / previous) - 1) * 100

    st.metric(
        label=f"{selected_coin} Price Binance",
        value=f"${latest:,.2f}",
        delta=f"{change:.2f}%"
    )
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

live1()


# =================================
# CHART DATA
# =================================
@st.cache_data(ttl=120)
def live_chart(chart):

    df = fetch_historical_data(selected_coin, selected_timeframe)

    chart_df = df.sort_values(
        'OpenTime',
        ascending=True
    ).reset_index(drop=True)

    if chart == "Candle":
        Candle_chart(chart_df)
    elif chart == "Line":
        Line_chart(chart_df)

# =================================
# TABS
# =================================

tab1, tab2 = st.tabs([
    "Chart",
    "Historical Data"
])


# =================================
# CHARTS
# =================================

with tab1:

    st.subheader(f"{selected_timeframef}{selected_coin} Price Chart")

    if chart == "Candle" or chart == None:
        live_chart("Candle")

    elif chart == "Line":
        live_chart("Line")


# =================================
# LIVE TABLE
# =================================

with tab2:

    st.subheader(f"{selected_timeframe} Historical Data")

    @st.cache_data(ttl=120)
    def live_table():

        df = fetch_historical_data(selected_coin, selected_timeframe, limit=1000)
        st.dataframe(df)

    live_table()


