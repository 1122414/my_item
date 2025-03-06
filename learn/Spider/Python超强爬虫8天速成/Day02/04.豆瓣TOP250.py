# 需求，只爬取电影名和名次、评分  未完善
import os
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'cookie':'bid=y0G0yiDQJoQ; dbcl2="219532216:RvdMP2hYCB4"; ck=WCbA; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1730883179%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_id.100001.4cf6=7d5e6ae8ac70763a.1730883179.; _pk_ses.100001.4cf6=1; push_noty_num=0; push_doumail_num=0'
}

url = 'https://movie.douban.com/top250'
params = {
    'start': 0,
    'filter': ''
}
response = requests.get(url, headers=headers, params=params).text
# print(response)

sub_path = '豆瓣TOP250' + '.html'
current_path = os.path.dirname(__file__)  # 脚本所在的位置
file_path = os.path.join(current_path, sub_path)  # 拼接出文件路径

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(response)
print('爬取成功！')