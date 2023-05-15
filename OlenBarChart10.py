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

# Set Page Configuration
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Create placeholders
title_placeholder = st.empty()
last_updated_placeholder = st.empty()
chart_placeholder = st.empty()
dataframe_placeholder1 = st.empty()
dataframe_placeholder2 = st.empty()




# List all files in the current directory
##files = os.listdir()
#st.write(files)


pd.options.mode.chained_assignment = None  # default='warn'
current_time = datetime.now(timezone(timedelta(hours=-4), 'EDT')).strftime("%m-%d-%y %H:%M:%S")
page_title = f"Olen Limestone Scale Results - Last Updated: {current_time}"
y_select = st.sidebar.multiselect(
    label="Select Scales",
    options=["LFC8", "LC2", "LC6", "LC7", "LC1B", "LC31", "LC1", "LC14", "LC17", "LC20", "LC27", "LC11", "LFC9"],
    default=["LFC8"]
)


#wb_file_path = r'c:/olenrun/NowData.xlsx'
#os.chdir(r'C:\olenrun')
wb_file_path = 'NowData.xlsx'

# Print the file path
#print(wb_file_path)

def calculate_rolling_average(df, window):
    """Calculate the rolling average for each scale."""
    df_rolling = df.copy()
    for scale in df_rolling["Scale"].unique():
        scale_rows = df_rolling["Scale"] == scale
        df_rolling.loc[scale_rows, "RollingAvg"] = (
            df_rolling.loc[scale_rows, "Value"].rolling(window=window).mean()
        )
    return df_rolling


def load_data(wb_file_path, rolling_window):
    """Load data from an Excel file and return a DataFrame."""
    while True:
        try:
            df = pd.read_excel(
            io=wb_file_path,
            engine='openpyxl',
            sheet_name='Sheet1',
            skiprows=18,
            usecols='BN:CA',
            nrows=1441,
    )

            # save the dataframe to an excel file
            #df.to_excel('c:\olenrun\output.xlsx', index=False)


            df.columns = [col.replace('.2', '') for col in df.columns]
            df = df[['DateTime'] + y_select]
            df = df.melt(id_vars=['DateTime'], var_name='Scale', value_name='Value')

            # Calculate the rolling average for each scale
            df = calculate_rolling_average(df, rolling_window)

            return df
        except PermissionError:
            print("Permission denied while reading the file. Retrying in 10 seconds...")
            time.sleep(10)

    # save the dataframe to an excel file
    #df.to_excel('c:\olenrun\output.xlsx', index=False)




#@st.cache_resource
def get_state():
    return {'y_max': None, 'value_limit': None}

state = get_state()
#state.setdefault('value_limit', 2400)





# Declare the sidebar widgets
opacity1 = st.sidebar.number_input('Enter a value for the opacity', min_value=0.0, max_value=1.0, value=0.4)
rolling_window = st.sidebar.number_input("Rolling Average Minutes", min_value=0, max_value=100, value=30, step=1, key='rolling_window')
value_limit = st.sidebar.number_input("Max y-axis Value", min_value=0, max_value=4000, value=int(state['value_limit'] or 1200), step=100, key='value_limit')
#y_max_value = state.get('y_max', 3000)
#y_max_value = 3000 if y_max_value is None else int(y_max_value)
#state['y_max'] = st.sidebar.number_input("Y-axis Max Value", min_value=0, max_value=4000, value=y_max_value, step=100, key='y_max')





def update_data(value_slider, y_axis_limit):
   

    # Load the data
    df = load_data(wb_file_path, rolling_window)

    # Filter the DataFrame based on the selected scales and values less than 3000
    #filtered_df = df[(df['Scale'].isin(y_select)) & (df['Value'] < value_limit)]   
    filtered_df = df[(df['Scale'].isin(y_select)) & (df['Value'] < value_slider)]


    # Create a new column 'CappedValue' in the DataFrame, containing the capped values based on the selected y-axis max value
    #filtered_df.loc[:, 'CappedValue'] = filtered_df['Value'].apply(lambda x: x if x <= value_limit else value_limit)
    filtered_df.loc[:, 'CappedValue'] = filtered_df['Value'].apply(lambda x: x if x <= value_slider else value_slider)
    print(value_slider)

    # Set y_domain to [0, value_limit]
    y_domain = [0, value_limit]

    max_y = value_limit
   # print(max_y)
    
    tick_interval = max_y // 100 if max_y <= 2000 else max_y // 200

    return filtered_df, y_domain, tick_interval





def lighten_color_fixed(color, amount=100):
    r, g, b = color
    r = max(min(r + amount, 255), 0)
    g = max(min(g + amount, 255), 0)
    b = max(min(b + amount, 255), 0)
    return int(r), int(g), int(b)



def create_chart(df, y_axis_limit, tick_interval):
    charts = []
    color_scale = alt.Scale(
        domain=["LFC8", "LC2", "LC6", "LC7", "LC1B", "LC31", "LC1", "LC14", "LC17", "LC20", "LC27", "LC11", "LFC9"],
        range=['rgb(255, 0, 0)', 'rgb(200, 100, 0)', 'rgb(0, 0, 255)', 'rgb(255, 255, 0)', 'rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)', 'rgb(255, 255, 0)',
               'rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)', 'rgb(255, 255, 0)', 'rgb(255, 0, 0)']
    )

    
    
    for scale in y_select:
        bar_chart = alt.Chart(
            df[df['Scale'] == scale], height=400).mark_bar(opacity=opacity1).encode(
            x=alt.X('DateTime', axis=alt.Axis(labelOverlap="parity", labelAngle=-90, grid=False, labelColor='rgb(220, 255, 160)', titleColor='rgb(220, 255, 160)', labelFontSize=13)),
            y=alt.Y('CappedValue', title="Tons", scale=alt.Scale(domain=(0, y_axis_limit)), axis=alt.Axis(labelColor='rgb(220, 255, 160)', titleColor='rgb(220, 255, 160)', labelFontSize=15, tickCount=tick_interval)),
            color=alt.Color('Scale', scale=color_scale, legend=alt.Legend(orient="right"))
        )


        # Get the original color of the scale
        scale_color = color_scale['range'][color_scale['domain'].index(scale)]

        # Calculate the lighter color for the rolling average line
       # lighter_color = lighten_color(tuple(int(x) for x in re.findall(r'\d+', scale_color)))
        lighter_color = lighten_color_fixed(tuple(int(x) for x in re.findall(r'\d+', scale_color)))

        # Create a line chart for the rolling average
        rolling_avg_chart = alt.Chart(df[df['Scale'] == scale], height=400).mark_line(
            stroke=f"rgb({lighter_color[0]}, {lighter_color[1]}, {lighter_color[2]})", strokeWidth=2).encode(x='DateTime', y='RollingAvg').properties(width='container')
        
   



        # Combine the bar chart and rolling average line chart
        combined_chart = bar_chart + rolling_avg_chart
        charts.append(combined_chart)

    # Layer all the charts for different scales
    final_chart = alt.layer(*charts, height=400).resolve_scale(color='shared')

    # Display the chart
    chart_placeholder.altair_chart(final_chart, use_container_width=True)
    return final_chart





def update_data_and_chart(value_slider, y_axis_limit):
    # Get the updated value_limit from the sidebar
    global value_limit
    value_limit = value_slider
    print(value_limit)

    # Update the data based on the new value_limit
    #filtered_df, y_domain, tick_interval = update_data(value_limit)
    filtered_df, y_domain, tick_interval = update_data(value_slider, y_axis_limit)

    # Create the chart with the updated data
    #final_chart = create_chart(filtered_df, y_domain, tick_interval)
    final_chart = create_chart(filtered_df, y_axis_limit, tick_interval)

    # Display the chart
   # chart_placeholder.altair_chart(final_chart, use_container_width=True)

    # Create an empty placeholder
    processing_message = st.empty()

    processing_message.markdown(
        "<p style='color: yellow; font-family: Arial; font-size: 18px; text-align: center;'>Processing Data... please wait</p>",
        unsafe_allow_html=True,
    )

    # Remove the message after the chart update is complete
    processing_message.empty()
    
    thistime = datetime.now(timezone(timedelta(hours=-4), 'EDT'))
    timenow = thistime.strftime("%m-%d-%y %H:%M:%S")
    last_updated = f"Last updated: {timenow}"

    # Show page title and last updated information on the same line
    title_placeholder.markdown(f"""
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='font-family: Arial; font-size: 18px; text-align: right;'>Olen Limestone Results</h3>
                    <h3 style='font-size: 13px; text-align: center; color: yellow; margin-right: auto;'>{last_updated}</h3>
                </div>
            """, unsafe_allow_html=True)





# Continuously update the chart
value_slider = st.sidebar.number_input("Capped Value (limits data anomoly effects)", min_value=0, max_value=4000, value=1200, step=100, key='value_slider')
print(value_slider)

while True:
    try:
        # Reload the data here
        print("Reloading data...")
        update_data_and_chart(value_slider, value_limit)   # Add the value_limit parameter here
        time.sleep(30)
    except KeyboardInterrupt:
        # Stop the script if the user closes the browser or disconnects
        print("User disconnected, stopping script...")
        break



