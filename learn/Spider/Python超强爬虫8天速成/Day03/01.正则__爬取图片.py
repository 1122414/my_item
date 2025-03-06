import requests
import re
import os

# text 字符串 content 二进制 json 对象

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

url = "https://www.bilibili.com/read/cv17124636/?from=search&spm_id_from=333.337.0.0"

page_text = requests.get(url, headers=headers).text
# # print(page_text)
# ex = '<meta data-vue-meta="true" .*?>'
# img_urls = re.findall(ex, page_text, re.S)
# print(img_urls)

# ex = '<meta data-vue-meta="true" data-n-head="true".*? content="(.*?)>'
# # re.S 匹配单行 re.M 匹配多行
# img_urls = re.findall(ex, page_text, re.S)
# print(img_urls)

ex = '<figure class="img-box" contenteditable="false"><img data-src="(.*?)" .*?></figure>'
# re.S 匹配单行 re.M 匹配多行
img_urls = re.findall(ex, page_text, re.S)
# print(img_urls)

for src in img_urls:
    src = "https:" + src
    img_data = requests.get(src, headers=headers).content
    current_path = os.path.dirname(__file__)
    img_name = src.split("/")[-1]
    imgPath = os.path.join(current_path,"蒂蒂老婆\\", img_name)  
    # imgPath = "B站Day3/蒂蒂老婆/" + img_name
    with open(imgPath, "wb") as fp:
        fp.write(img_data)
        print(img_name, "下载成功!")