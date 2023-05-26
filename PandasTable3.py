import streamlit as st
import pandas as pd
import openpyxl 
import plotly.express as px
import plotly.graph_objs as go
import time
from datetime import datetime
import os

st.set_page_config(page_title="Olen Limestone Results Summary Table", layout="wide")

from openpyxl.utils.dataframe import dataframe_to_rows

#wb_file_path = r'c:/olenrun/NowData.xlsx'
os.chdir(r'C:\\olenrun')
#wb_file_path = 'NowData.xlsx'

# Get the current directory of the script
#script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current directory to olenrun
#os.chdir(os.path.join(script_dir, 'olenrun'))

#os.chdir('/home/appuser/olenrun')


wb_file_path = 'NowData.xlsx'


df = pd.read_excel(
    io=wb_file_path,
    engine='openpyxl',
    sheet_name='Sheet1',
    skiprows=3,
    usecols='AG:AU',
    nrows=11,
)



# Exclude column 1
df = df.drop(df.columns[1], axis=1)

# Exclude non-numeric columns from formatting
numeric_cols = df.iloc[0:2].apply(pd.to_numeric, errors='coerce').notna().all()
numeric_col_names = df.columns[numeric_cols].tolist()

# Format rows 0 and 1 to always show one decimal place for numeric columns
df.loc[0:1, numeric_col_names] = df.loc[0:1, numeric_col_names].applymap("{:.1f}".format)

# Convert rows 5 through 11 (excluding column 1) to numeric and format as 'x,xxx' with no decimal places
df.iloc[3:11, 1:] = df.iloc[3:11, 1:].apply(lambda x: pd.to_numeric(x, errors='coerce')).applymap("{:,.0f}".format)

# Convert values in row 3 starting from column 3 to numeric
df.iloc[2, 2:] = pd.to_numeric(df.iloc[2, 2:], errors='coerce')

# Convert to percentage and format as string
df.iloc[2, 1:] = (df.iloc[2, 1:] * 100).apply(lambda x: "{:,.1f}%".format(x))

# Round rows 3 through 11 to 0 decimal places
df.iloc[3:11] = df.iloc[3:11].round(0)

# Reset index
df_reset = df.reset_index()

# Center align the data horizontally
styled_df = df_reset.style.set_properties(**{'text-align': 'center'})

# Left justify column 1
styled_df = styled_df.set_properties(subset=[styled_df.columns[1]], **{'text-align': 'left'})


fig = go.Figure(
    data=[
        go.Table(
            columnwidth=[2.5] + [1] * (df.shape[1] - 1),  # Set column 1 width to 33, other columns to 1
            header=dict(
                values=list(df.columns), 
                fill_color='rgb(17,17,17)',
                align=['left','center'],
                font=dict(color='rgb(255,255,255)', size=14),
                height=33  # Set top row height to 40
            ),
            cells=dict(
                values=[df[col] for col in df.columns],
                align=['left', 'center'],
                font=dict(color=['rgb(255,28,0)' if cell == 0 else 'rgb(255,255,150)' for row in df.values for cell in row], size=14),
                fill_color=[['rgb(225,28,0)' if cell == 0 else 'rgb(0,0,0)' for cell in row] for row in df.values],
                height=26  # Set row height to 6    
            ),
        )
    ],           
)

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current time and format it

#st.markdown("---")
st.markdown(f"<h2 style='font-size: 23px; line-height: 33px; vertical-align: bottom;'>Olen Limestone Current Day Results -- <span style='font-size: 20px; color: yellow;'>{current_time}</span></h2>", unsafe_allow_html=True)
#st.markdown("---")


fig.update_layout(
    margin =dict(l=5,r=5,b=5, t=5), 
    height=310, 
    width=1000, 
    paper_bgcolor='rgb(0,0,0)'
)
st.plotly_chart(fig)



time.sleep(30)




























