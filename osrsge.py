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
        price=int(data["item"]["current"]["price"])
    row=[]
    row.append(int(time.time()))
    row.append(data["item"]["id"])
    row.append(data["item"]["name"])
    row.append(price)
    row.append(data["item"]["members"])
    print(row)
    return 

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
