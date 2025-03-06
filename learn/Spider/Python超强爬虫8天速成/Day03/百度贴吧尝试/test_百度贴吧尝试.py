# 贴吧控制页数的参数是pn=2
import os
import re
import requests
from bs4 import BeautifulSoup

url = "https://tieba.baidu.com/p/8578212993"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
response = requests.get(url, headers=headers)
# with open("test.html", "w", encoding="utf-8") as f:
#     f.write(response.text)

'''
# 帖子编码
match = re.search(r'\d+', url)  # 使用正则表达式匹配连续的数字
sub_str = match.group()  # 获取匹配到的子字符串
print(sub_str)  # 输出 "123"
'''

with open("test.html", "w", encoding="utf-8") as f:
    f.write(response.text)

soup = BeautifulSoup(response.text, "html.parser")


# 每个楼层层主
nikName_list = soup.find_all("a", class_="p_author_name")
# 每个楼层内容
content_list = soup.find_all("div", class_="d_post_content j_d_post_content")
# 层数
floor_count = len(content_list)
# 每条回复
reply_list = soup.find_all("span", class_="lzl_content_main")

print(reply_list)

current_path = os.path.dirname(__file__)
sub_path = "test_百度贴吧尝试"
full_path = os.path.join(current_path, sub_path)

with open(full_path,"w",encoding="utf-8") as fp:
    for i in range(len(content_list)):
        fp.write(nikName_list[i].text + "\n")
        fp.write(content_list[i].text + "\n")
        for j in range(len(reply_list)):
            fp.write(reply_list[j].text + "\n")
        fp.write("----------\n")
