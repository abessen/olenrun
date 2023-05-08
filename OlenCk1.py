import os
import time
from datetime import datetime, timezone, timedelta
import pandas as pd
import altair as alt
import streamlit as st
import colorsys
import re
import openpyxl


# Set Page Configuration
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Create placeholders
title_placeholder = st.empty()
last_updated_placeholder = st.empty()
chart_placeholder = st.empty()
dataframe_placeholder1 = st.empty()
dataframe_placeholder2 = st.empty()



pd.options.mode.chained_assignment = None  # default='warn'
current_time = datetime.now(timezone(timedelta(hours=-4), 'EDT')).strftime("%m-%d-%y %H:%M:%S")
page_title = f"Olen Limestone Scale Results - Last Updated: {current_time}"
y_select = st.sidebar.multiselect(
    label="Select Scales",
    options=[
        "LFC8", "LC2", "LC6", "LC7", "LC1B", "LC31", "LC1", "LC14", "LC17",
        "LC20", "LC27", "LC11", "LFC9"
    ],
    default=["LFC8"]
)

wb_file_path = r'c:\olenrun\NowData.xlsx'

# Print the file path
print(wb_file_path)








df = pd.read_excel(
            io=wb_file_path,
            engine='openpyxl',
            sheet_name='Sheet1',
            skiprows=18,
            usecols='BN:CA',
            nrows=1441,
    )

    



   
# save the dataframe to an excel file
df.to_excel('c:\olenrun\output.xlsx', index=False)

