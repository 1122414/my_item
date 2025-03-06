import requests
import json
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
url = 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'

query =  input("请输入要查询的市区：")
params = {
    "cname": '',
    "pid": '',
    "keyword": query,
    "pageIndex": 1,
    "pageSize": 100
}
response = requests.post(url, data = params,headers=headers).text
# print(response)
datas = json.loads(response)
count = datas["Table"][0]["rowcount"]

num = 0
# print(count)
# 打印餐厅信息
for data in datas["Table1"]:
  # print(data)
  # data = json.loads(dataI)
  name = data["storeName"]
  address = data["addressDetail"]
  num += 1
  print(f"第{num}家餐厅：{name},\n地址:{address}")


print(f"{query}地区共有{count}家肯德基餐厅")

