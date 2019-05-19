import requests
import json
from pprint import pprint
import time 
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


# Setup the google API
SCOPES = "https://www.googleapis.com/auth/drive"
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# read and write parameters:
SPREADSHEET_ID = '1L4xjmfMSWZlsB8FZ8xAqR_dOZqrGoGBuzAEYR1HTu60'
RANGE_NAME = 'data!A:E'
# How the input data should be interpreted.
value_input_option = 'USER_ENTERED'  
# How the input data should be inserted.
insert_data_option = 'INSERT_ROWS' 

# read data from google sheet
def data_reader():
    #the api call
    read = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()
    values = read.get('values', [])
    if not values:
        return print('No data found.')
    else:
        return print(values)
    
#write data to google sheet
def data_writer(unix_date,item_ID,item_name,price,member_item):
    value_range_body={
        "values": [
            [
                unix_date,
                item_ID,
                item_name,
                price,
                member_item
            ]
        ]
    }
    request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()
#some global variables
x=0
l=[]
avg_l=0.1

def read_OSRS_GE(item_id):
    global x
    global l
    global avg_l
    api_url="http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item="
    r=requests.get(api_url+str(item_id))
    # if response is empty
    # wait for the average time we had to wait for in the past
    if r.text=="":
        print("sleeping for",avg_l)
        time.sleep(avg_l)
        x=x+avg_l
        return read_OSRS_GE(item_id)
    if x!=0:
        l.append(x)
        avg_l=sum(l)/len(l)
        x=0
    data=r.json()
    # print("dataid",data["item"]["id"])
    # pprint(data)
    strprice=str(data["item"]["current"]["price"])
    lastchar=strprice[-1:]
    if str(lastchar)=="k":
        price=int(float(str(data["item"]["current"]["price"])[:len(strprice)-1])*1000)
    else:
        price=data["item"]["current"]["price"]
    row=[]
    row.append(int(time.time()))
    row.append(data["item"]["id"])
    row.append(data["item"]["name"])
    row.append(price)
    row.append(data["item"]["members"])
    print(row)
    data_writer(int(time.time()),data["item"]["id"],data["item"]["name"],price,data["item"]["members"])
    time.sleep(1)
    return print("wrote line")

# get all items
def get_items():
    api_url="https://rsbuddy.com/exchange/summary.json"
    r=requests.get(api_url)
    data=r.json()
    counter=1
    for key, value in data.items():
        print("item id:",key)
        print("call:",counter)
        read_OSRS_GE(key)
        counter+=1
    return 
while 1:
    get_items()
