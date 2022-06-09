import requests
from bs4 import BeautifulSoup
import pandas as pd

import dotenv
import os
import json

import time
import random

import logging
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)


dotenv.load_dotenv()

MARGIN = 0.3
SHOP_URL = f'https://{os.environ.get("API_KEY")}:{os.environ.get("ACCESS_TOKEN")}@automation-genie.myshopify.com/admin'

# data = requests.get(SHOP_URL+"/products.json").json()

# json.dump(data,open("data.json","w"))

url = (lambda x:f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={'+'.join(x.split())}&_sacat=0&LH_BIN=1&_fcid=1&_sop=15&rt=nc&LH_ItemCondition=3")

df = pd.read_csv("products_import.csv")
headers = {"Accept": "application/json", "Content-Type": "application/json"}

for index,row in df.iterrows():
    if index < 1000:
        continue

    try:
        print(row["Title"])
        res = requests.get(url(row["Variant SKU"]))
        print(url(row["Variant SKU"]))
        soup = BeautifulSoup(res.text,"lxml")
        print(soup.find_all("span",{"class":"s-item__detail"}).text)
        item_prices = soup.find_all("span",{"class":"s-item__price"})[1:]
        # ratings = list(map(lambda x : x.text.split()[-1],soup.find_all("span",{"class":"s-item__seller-info-text"})[1:]))
    #print(item_prices)
        price = 0
        # for i in range(len(item_prices)):
            #works on the assumption that every seller has a rating section
            # if float(ratings[i]) > 90:
        price = round((1+MARGIN)*float(item_prices[0].text.split()[-1].replace("$","") if len(item_prices) > 1 else 0 ))
        
        # if variant := list(filter(lambda x: x["title"] == row["Title"], data["products"])):
        print(price)
        # var_id = row["variants"][0]["id"]

        # upload_url = SHOP_URL + f"/api/2022-04/variants/{var_id}.json"
        # payload = {"variant":{"id":var_id,"price":price}}
        # #print()
        # requests.put(upload_url,headers=headers,json=payload).json()
        df.at[index,"Variant Price"] = price
        logging.info(f"Updated {row['Title']} price to {price}")
        time.sleep(random.randint(3,7))
    except Exception as e:
        print(e)
        time.sleep(10)
        df.to_csv("products_import.csv")

    df.to_csv("products_import1.csv")

