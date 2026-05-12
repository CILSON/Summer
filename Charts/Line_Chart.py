import streamlit as st
import plotly.express as px

def Line_chart(df):

    fig = px.line(df, x='CloseTime', y='Close', template='plotly_dark')

    fig.update_layout(
        height=500,
        width=1000,
        xaxis_title='',
        yaxis_title='',
        template="plotly_dark",

        margin=dict(l=10, r=10, t=30, b=10),

        uirevision="constant",  # Preserve the chart's state across updates.
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, gridcolor='rgba(255,255,255,0.08)')

    st.plotly_chart(fig, use_container_width=True)