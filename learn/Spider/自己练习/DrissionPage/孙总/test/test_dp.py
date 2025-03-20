from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.common import By
from DrissionPage.common import Keys

page = ChromiumPage()
page.get('https://www.baidu.com/')
tabs = page.get_tabs()

new_page = page.new_tab('https://v.douyin.com/_jNFfEtoRA8/')

# page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[3]/div/div[1]/button').click(by_js=True)
try:
  text = new_page.ele('x://*[@id="search-content-area"]/div/div[1]/div[1]/div[1]/div/div/span[1]').text
except Exception as e:
  print(e)

# text = page.ele('x://*[@id="input"]').text

# text = page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]').text

# page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[1]/div/div/div[2]/span').click.at(-200,0)

# page.actions.key_down('SPACE')  # 输入按键名称
new_page.actions.key_down(Keys.SPACE)       # 从Keys获取按键

now_tab = page.get_tab()

tabs = page.get_tabs()

page.close_tabs(now_tab)

now_page = page.get_tab()

print(now_page.title)
print(now_page.ele('x://*[@id="s_new_search_guide"]/div/a/div[2]').text)

page.wait(50)