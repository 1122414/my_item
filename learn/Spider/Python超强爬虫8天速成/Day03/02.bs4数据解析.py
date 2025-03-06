import requests
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
url = "https://www.shicimingju.com/shicimark/shanshuishi.html"
response = requests.get(url, headers=headers)
page_text = response.text
soup = BeautifulSoup(page_text, 'html.parser')
# print(soup)
# 解析题目

# 一下两个效果一样，注意语法
# for tag in soup.find_all('a',class_='show_more_shici'):
#     tag.decompose()
    
for tag in soup.select('div[class="show_more_shici"]'):
    tag.decompose()
# print(soup)

big_div = soup.select('div[class="card shici_card"] > div > div[class="shici_list_main"]')
for i in range(len(big_div)):
    print(big_div[i])

title_list = soup.select('div[class="shici_list_main"] h3 a')
content_list = soup.select('div[class="shici_content"]')
# 去除标签

# print(content_list)
for i in range(len(title_list)):
    print(title_list[i].text)
    print(content_list[i].text)
    print('--------------------------------------------')
# 解析古诗
# print(soup.select('div[class="shici_list_main"]'))

# soup.a              
# print(soup)

