import requests
from bs4 import BeautifulSoup
import pandas as pd

import dotenv
import os
import json

import time
import random



dotenv.load_dotenv()

MARGIN = 0.3
SHOP_URL = f'https://{os.environ.get("API_KEY")}:{os.environ.get("ACCESS_TOKEN")}@automation-genie.myshopify.com/admin'

# data = requests.get(SHOP_URL+"/products.json").json()

# json.dump(data,open("data.json","w"))


log_url = "http://21fc-223-196-163-5.ngrok.io"

print = (lambda x: requests.post(log_url,json={"data":x}))


url = (lambda x:f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={'+'.join(x.split())}&_sacat=0&LH_BIN=1&_fcid=1&_sop=15&rt=nc&LH_ItemCondition=3")

df = pd.read_csv("products.csv")
data = json.load(open("products1.json"))
headers = {"Accept": "application/json", "Content-Type": "application/json"}

df["SKU"] = df["product_title"].str.replace("-","").str.split().str[0]
SKUS = [i["variants"][0]["sku"] for i in data]

common = []

for index,i in enumerate(SKUS):
    common.extend(data[index] for j in df["SKU"] if i.replace("-","") == j)

for row in common:
    try:
        print(row["title"])
        res = requests.get(url(row["variants"][0]["sku"]))
        print(row["variants"][0]["sku"])
        soup = BeautifulSoup(res.text,"lxml")
        item_prices = soup.find_all("span",{"class":"s-item__price"})[1:]
        price = 0
        price = round((1+MARGIN)*float(item_prices[0].text.split()[-1].replace("$","").replace(",","") if len(item_prices) > 1 else 0 ))
        
        print(price)
        var_id = row["variants"][0]["id"]

        upload_url = SHOP_URL + f"/api/2022-04/variants/{var_id}.json"
        payload = {"variant":{"id":var_id,"price":price}}
        #print()
        requests.put(upload_url,headers=headers,json=payload).json()
        time.sleep(random.randint(3,7))
    except Exception as e:
        print(e)
        time.sleep(10)
