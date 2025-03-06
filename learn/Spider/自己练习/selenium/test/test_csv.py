import json
import csv
 
# 假设json_data是您的JSON数据
json_data = {
    "name":[
     '张三','李四','王五'
    ],
    "age":[
      '25', '30', '35'
    ]
}
'''
需要的格式
json_data = [
    {"name": "John", "age": 30, "city": "New York"},
    {"name": "Anne", "age�": 25, "city": "Chicago"},
    {"name": "Peter", "age": 35, "city": "San Francisco"}
]
'''
# print(json_data)
# print(json_data['name'])
data = []
for i in range(len(json_data['name'])):
    data.append({
        "name": json_data['name'][i],
        "age": json_data['age'][i],
    })
# 打开CSV文件进行写入
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["name", "age", "city"])
    writer.writeheader()
    for d in data:
        writer.writerow(d)