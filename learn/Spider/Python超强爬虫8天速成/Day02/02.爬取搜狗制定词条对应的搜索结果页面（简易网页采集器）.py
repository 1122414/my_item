import os
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}
query = input("请输入你要搜索的关键字：")
url = 'https://www.sogou.com/web?'
params = {
    'query': query,
}

print("正在搜索：", query)

response = requests.get(url=url, params=params, headers=headers)
page_text = response.text

sub_path = query
# current_path = os.getcwd() os.getcwd() 运行时所在的位置
current_path = os.path.dirname(__file__)  # 脚本所在的位置
full_path = os.path.join(current_path, sub_path)
# print(full_path)

with open(full_path, 'w', encoding='utf-8') as f:
    f.write(page_text)
print("搜索结果已保存至文件：", full_path)