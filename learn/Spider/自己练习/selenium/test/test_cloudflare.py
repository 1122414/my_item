# -*- coding: utf-8 -*-
import os
import requests
current_path = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(current_path, "test_hackforum.html")

url = "https://api.cloudbypass.com/"
method = "GET"
headers = {
    "x-cb-apikey": r"682b47c0f68c4377ab8251c069cc46f1",
    "x-cb-host": r"hackforums.net",
    # "x-cb-host": r"www.brownsfashion.com",
    "x-cb-version": r"2",
    "x-cb-part": r"0",
    "x-cb-fp": r"chrome",
    "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "x-cb-proxy": r"http:86313945-dat:aojecnpg:gw.cloudbypass.com:1288",
}

response = requests.request(method, url, headers=headers)

with open(full_path, "w", encoding="utf-8") as f:
    f.write(response.text)

print(response.text)