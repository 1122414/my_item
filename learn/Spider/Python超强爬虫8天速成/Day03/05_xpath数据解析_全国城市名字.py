import requests
from lxml import etree

url = 'https://www.aqistudy.cn/historydata/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
response = requests.get(url, headers=headers)
page_text = response.content.decode('utf-8')

tree = etree.HTML(page_text)

# 获取热门城市名称
hot_cities_list = tree.xpath('//div[@class="hot"]//ul[@class="unstyled"]/li/a/text()')
# 获取全部城市名称
all_cities_first_name = tree.xpath('//div[@class="all"]//ul[@class="unstyled"]/div[1]/b/text()')
for i in range(len(all_cities_first_name)):
  all_cities_list = tree.xpath(f'//div[@class="all"]//ul[@class="unstyled"][{i+1}]/div[2]/li/a/text()')
  print(all_cities_first_name[i])

  print(all_cities_list)


print("\nend!")