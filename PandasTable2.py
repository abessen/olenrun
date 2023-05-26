import streamlit as st
import pandas as pd
import pyxlsb
import plotly.express as px  # pip install plotly-express
import plotly.graph_objs as go
import time
import datetime as dt


st.set_page_config(page_title="Olen Limestone Results Summary Table",  layout="wide")
  

wb_file_path = 'C:/_Olen1App/OlenMaster_v1.xlsb'
df = pd.read_excel(
            io=wb_file_path,
            engine='pyxlsb',
            sheet_name='eWon',
            skiprows=3,
            usecols='CX:DK',
            nrows=12,
        )


fig = go.Figure(
        data=[go.Table(columnwidth=(2,1,1,1,1,1,1,1,1,1,1,1,1,1),
            header=dict(values=list(df.columns), 
            fill_color='rgb(17,17,17)',align=['left','center'],font=dict(color='rgb(255,255,255)', size=14),height=14),

            cells=dict(values=[df[col] for col in df.columns],align=['left', 'center'],
            font=dict(color=['rgb(255,28,0)' if cell == 0 else 'rgb(255,255,150)' for row in df.values for cell in row], size=14),
            fill_color=[['rgb(225,28,0)' if cell == 0 else 'rgb(0,0,0)' for cell in row] for row in df.values]      
            ),
    )],
                
    )


st.markdown("""---""")
st.subheader("Olen Limestone Current Day Results")
#left_column, right_column = st.columns(2)
#left_column.plotly_chart(fig, use_container_width=False)
#right_column.plotly_chart(fig, use_container_width=False)

fig.update_layout(margin =dict(l=5,r=5,b=5, t=5), height=310, width=1000, paper_bgcolor='rgb(0,0,0)')
st.plotly_chart(fig)
#st.write(fig)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#Refresh Delay
time.sleep(30)
st.experimental_rerun()