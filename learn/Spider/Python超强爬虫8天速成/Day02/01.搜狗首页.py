import requests
if __name__ == '__main__':
  # step 1: 指定url
  url = 'https://www.sogou.com/'
  # step 2: 发起请求
  response = requests.get(url=url)
  # step 3: 打印响应内容
  # print(response.text)
  page_text = response.text
  # step 4: 保存响应内容到文件
  with open('2024.7哔站爬虫/Python超强爬虫8天速成/Day02/sogou.html', 'w', encoding='utf-8') as f:
    f.write(page_text)