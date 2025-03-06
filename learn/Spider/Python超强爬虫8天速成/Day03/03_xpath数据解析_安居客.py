# 安居客
import requests
from lxml import etree

def analysis_city():
  # 解析页面数据
  tree = etree.HTML(page_text)
  # title_list = tree.xpath('//div[@class="property-content-title"]')
  # title_list = tree.xpath('//div[@class="property-content-title"]/h3')
  title_list = tree.xpath('//div[@class="property-content-title"]/h3/@title')
  total_price_list = tree.xpath('//div[@class="property-price"]//span[@class="property-price-total-num"]/text()')
  total_area_list = tree.xpath('//div[@class="property-price"]/p[@class="property-price-average"]/text()')

  for i in range(len(title_list)):
      print(f"{i+1}、{title_list[i]}，总价：{total_price_list[i]}万元，面积：{total_area_list[i]}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}


city = input("请输入城市名称拼音：")
area = input("请输入区县名称拼音：")
for i in range(1, 10):
  url = f'https://{city}.anjuke.com/sale/{area}/p{i}'

  print(f"正在访问{url}...")
  print(f"正在爬取{city}市{area}区的二手房信息...")
  # url = 'https://suzhou.anjuke.com/sale/wuzhong/'
  response = requests.get(url, headers=headers)
  page_text = response.text
  if page_text == '':
     break
  analysis_city()






