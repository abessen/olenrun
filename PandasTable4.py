import os
import time
from datetime import datetime, timezone, timedelta
import pandas as pd
import altair as alt
import streamlit as st
import colorsys
import re
import openpyxl 
from PIL import Image
import base64
import io
import plotly.graph_objects as go  # Added this line

st.set_page_config(page_title="Olen Limestone Results Summary Table", layout="wide")

from openpyxl.utils.dataframe import dataframe_to_rows

wb_file_path = 'NowData.xlsx'

df = pd.read_excel(
    io=wb_file_path,
    engine='openpyxl',
    sheet_name='Sheet1',
    skiprows=3,
    usecols='AG:AU',
    nrows=11,
)

df = df.drop(df.columns[1], axis=1)

numeric_cols = df.iloc[0:2].apply(pd.to_numeric, errors='coerce').notna().all()
numeric_col_names = df.columns[numeric_cols].tolist()

df.loc[0:2, numeric_col_names] = df.loc[0:2, numeric_col_names].applymap("{:.1f}".format)
df.iloc[4:11, 1:] = df.iloc[4:11, 1:].apply(lambda x: pd.to_numeric(x, errors='coerce')).applymap("{:,.0f}".format)
df.iloc[3, 2:] = pd.to_numeric(df.iloc[3, 2:], errors='coerce')
df.iloc[3, 1:] = (df.iloc[3, 1:] * 100).apply(lambda x: "{:,.1f}%".format(x))
df.iloc[4:11] = df.iloc[4:11].round(0)

df_reset = df.reset_index()
styled_df = df_reset.style.set_properties(**{'text-align': 'center'})
styled_df = styled_df.set_properties(subset=[styled_df.columns[1]], **{'text-align': 'left'})

fig = go.Figure(
    data=[
        go.Table(
            columnwidth=[2.4] + [1] * (df.shape[1] - 1),  # Set column 1 width to 33, other columns to 1
            header=dict(
                values=list(df.columns), 
                fill_color='rgb(17,17,17)',
                align=['left','center'],
                font=dict(color='rgb(255,255,255)', size=12),
                height=20,  # Increase the height of the header row to align text at the bottom
                line_color='rgb(70,70,70)',  # Add this line
            ),
            cells=dict(
                values=[df[col] for col in df.columns],
                align=['left', 'center'],
                font=dict(color='rgb(255,255,255)', size=12),  # Set font color to white for all cells
                fill_color='rgb(0,0,0)',  # Set fill color to black for all cells
                height=20,  # Set row height to 26    
                line_color='rgb(70,70,70)',  # Add this line
            ),
        )
    ],           
)

current_time = datetime.now(timezone(timedelta(hours=-4))).strftime("%Y-%m-%d %H:%M:%S")  # Adjusted timezone to Eastern Daylight Time (EDT)
st.markdown(f"<h2 style='font-size: 16px; line-height: 12px; vertical-align: bottom;'>Olen Limestone Current Day Results -- <span style='font-size: 16px; color: yellow;'>{current_time}</span></h2>", unsafe_allow_html=True)

fig.update_layout(
    margin =dict(l=5,r=5,b=5, t=5), 
    height=310, 
    width=800, 
    paper_bgcolor='rgb(0,0,0)'
)
st.plotly_chart(fig)

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

time.sleep(30)
