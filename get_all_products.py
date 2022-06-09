import requests
import dotenv
import os

import json

data = []

dotenv.load_dotenv()

visited = set()

SHOP_URL = f'https://{os.environ.get("API_KEY")}:{os.environ.get("ACCESS_TOKEN")}@automation-genie.myshopify.com/admin/products.json?limit=250'

next_url = ""

while next_url != None and next_url not in visited:
    print(next_url)
    visited.add(next_url)
    res = requests.get(f"{SHOP_URL}{next_url}")
    data += res.json()["products"]
    links = requests.utils.parse_header_links(res.headers["link"])
    if next_links := [*filter(lambda x: x["rel"] == "next", links)]:
        next_url = next_links[0]["url"]
        next_url = f"&{next_url}"

    json.dump(data,open("products1.json","w+"))