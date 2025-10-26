import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional


def render_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str = ""):
    try:
        fig = px.line(df, x=x_col, y=y_col, title=title)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering line chart: {e}")


def render_pie_chart(df: pd.DataFrame, names: str, values: str, title: str = ""):
    try:
        fig = px.pie(df, names=names, values=values, title=title, hole=0.4)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering pie chart: {e}")


def render_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str = "", orientation: str = 'v'):
    try:
        if orientation == 'h':
            fig = px.bar(df, x=y_col, y=x_col, orientation='h', title=title)
        else:
            fig = px.bar(df, x=x_col, y=y_col, title=title)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering bar chart: {e}")
