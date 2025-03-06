# https://fanyi.baidu.com/mtpe-individual/multimodal?query=dog&lang=en2zh
# 只能翻译单词
import os
import json
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

url = 'https://fanyi.baidu.com/sug'
query = input('请输入要翻译的词语：')
data = {
    'kw': query,
}
# post请求和get请求的区别
# get请求参数在url中，post请求参数在body中

response = requests.post(url=url, data=data, headers=headers)

# response.encoding = 'UTF-8'
# json.loads()方法将json字符串转换为python对象
datas = json.loads(response.text)
# print(datas)

result = datas['data'][0]['v']

# print(result)

sub_path = '百度翻译：' +query + '.html'
current_path = os.path.dirname(__file__)  # 脚本所在的位置
file_path = os.path.join(current_path, sub_path)  # 拼接出文件路径

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(result)
print('文件保存成功！')