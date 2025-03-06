from lxml import etree

html = open(r'C:\Users\Lenovo\Desktop\vscode_python\2024.7哔站爬虫\自己练习\selenium\my_selenium_utils\search_result.html',encoding='utf-8').read()

print(html)


# 解析html
# 批量获取搜索结果视频标题
# title_list = driver.find_elements(By.XPATH, '//div[@class=bili-video-card__info--right]//h3')
# 批量获取搜索结果视频url
# url_list = driver.find_element(By.XPATH, '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/a')

tree = etree.HTML(html,etree.HTMLParser())
title_list1 = tree.xpath('//div[@class="bili-video-card__info--right"]')
title_list2 = tree.xpath('//div[@class="bili-video-card__info--right"]//h3')
title_list3 = tree.xpath('//div[@class="bili-video-card__info--right"]//h3/text()')
url_list = tree.xpath('//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/a/@href')
print(url_list)