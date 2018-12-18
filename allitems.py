import requests
from pprint import pprint
from datetime import datetime
import time
item_dict={}
waiting=0
waiting_list=[]
avg_waiting_time=1
def get_item_from_page(letter,page):
    global item_dict
    global avg_waiting_time
    global waiting
    API_URL="http://services.runescape.com/m=itemdb_oldschool/api/catalogue/items.json?category=1"
    URL=API_URL+"&alpha="+str(letter)+"&page="+str(page)
    r=requests.get(URL)
    # if empty request
    # then wait and redo
    if r.text=="":
        time.sleep(avg_waiting_time)
        waiting+=avg_waiting_time
        return get_item_from_page(letter,page)
    if waiting!=0:                      
        waiting_list.append(waiting)
        avg_waiting_time=sum(waiting_list[-10:])/len(waiting_list[-10:])
        waiting=0
        
    data=r.json()["items"]
    if len(data)==0:
        # print("next page letter")
        return 0
    else:
        for item in data:
            # here do i want to write to database
            item_dict[item["id"]]=item["name"]
        return 1
for unicode_letter in range(97,122):
    letter=chr(unicode_letter)
    page=0
    while get_item_from_page(letter,page):
        page+=1
    # this one should be indented one more but aye in the future we want to push to database
pprint(item_dict)
