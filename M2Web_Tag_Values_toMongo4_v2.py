from urllib.parse import urlencode
import requests
import json
from datetime import datetime, timedelta
import sys
from pymongo import MongoClient
from pymongo import MongoClient, errors
from io import StringIO
import csv
import time


# Talk2M credentials
t2maccount = "OlenCtrl"
t2mdeveloperid = "722d0ac4-b092-44c3-bc5e-5566ab2f9b4f"
t2musername = "arbqvision1"
t2mpassword = "qvision4me"
t2mdeviceusername = "arbqvision1"
t2mdevicepassword = "qvision4me"
device = 'EwonOlen404'

# eWON credentials
MyName = "arbqvision1"
MyPassword = "qvision4me"

# Scale IDs to retrieve data for
# scale_ids = ["LFC8TOTAL", "LC2TOTAL", "LC6TOTAL", "LC7TOTAL", "LC1BTOTAL", "LC31TOTAL", "LC1CTOTAL", "LC14CTOTAL", "LC17CTOTAL", "LC20CTOTAL", "LC27CTOTAL", "LC11CTOTAL", "LF9TOTAL"]

# Tag name dictionary
name_dict = {
    '2': 'LFC8TOTAL',
    '3': 'LC2TOTAL',
    '4': 'LC6TOTAL',
    '5': 'LC7TOTAL',
    '6': 'LC1BTOTAL',
    '7': 'LC31TOTAL',
    '8': 'LC1CTOTAL',
    '9': 'LC14CTOTAL',
    '10': 'LC17CTOTAL',
    '11': 'LC20CTOTAL',
    '12': 'LC27CTOTAL',
    '13': 'LC11CTOTAL',
    '15': 'LFC9TOTAL'
}

# Endpoint
api_url = 'https://m2web.talk2m.com/t2mapi/get/'  # Base URL

# MongoDB client
client = MongoClient('mongodb://localhost:27017/')

# MongoDB database
db = client['ColLS_4']

# MongoDB collection
collection = db['scale_data']

# Create unique index on fields
collection.create_index(
    [("TagId", 1), ("TimeInt", 1), ("Value", 1)], 
    unique=True
)

data_payload2 = {
        'AST_Param': '$dtHL$ftT$st_d1$et_s0',         
        't2maccount': t2maccount,
        't2musername': t2musername,
        't2mpassword': t2mpassword,
        't2mdeveloperid': t2mdeveloperid,
        't2mdeviceusername': t2mdeviceusername,
        't2mdevicepassword': t2mdevicepassword
    }


# The request URL
url =  f'{api_url}/{device}/rcgi.bin/ParamForm?{urlencode(data_payload2)}'

def update_data():
# Extract tag name/value pairs from semicolon-delimited string
    def tags_from_csv(text):
        values = []
        reader = csv.reader(StringIO(text), delimiter=';')
        rownum = 0
        for r in reader:
            if rownum == 0:
                rownum += 1
            else:
                values.append({
                    'TagId': r[0],
                    'TagName': name_dict[r[0]],
                    'TimeInt': r[1],
                    'TimeStr': r[2],
                    'IsInitValue': r[3],
                    'Value': r[4],
                    'IQuality': r[5],
                    #'tons': r[6] if len(r) > 6 else 'N/A'  # Assuming tons value is in the 7th position
                })
        return values

    url =  f'{api_url}/{device}/rcgi.bin/ParamForm?{urlencode(data_payload2)}'
    response = requests.get(url)

    if response.status_code == 200:
        print('Data retrieved successfully')    
        data = tags_from_csv(response.text)    
        # Store the data into the MongoDB collection

        try:
            collection.insert_many(data, ordered=False)
        except errors.BulkWriteError as e:
            print("Duplicates detected and ignored:")
        #  print(e.details)
    else:
        print('Failed to retrieve data')
        print(f'Response content: {response.text}')

# Continuously update the data
while True:
    update_data()
    time.sleep(30)
