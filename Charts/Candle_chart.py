import plotly.graph_objects as go
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def Candle_chart(df):

    fig = go.Figure(data=[go.Candlestick(
        x=df['CloseTime'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])

    fig.update_layout(
        height=500,
        width=1000,
        xaxis_rangeslider_visible=False,
        template="plotly_dark",

        margin=dict(l=10, r=10, t=30, b=10),

        # title="BTC/USDT Candlestick Chart",

        xaxis=dict(
            showgrid=False
        ),

        yaxis=dict(
            showgrid=False,
            gridcolor='rgba(255,255,255,0.08)'
        ),
        uirevision="constant",  # Preserve the chart's state across updates.
    )

    st.plotly_chart(fig, use_container_width=True)

    