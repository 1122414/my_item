from DrissionPage import ChromiumPage,ChromiumOptions
page = ChromiumPage()
page.get('https://www.baidu.com/')
# page.ele('x://*[@id="su"]')

# page.get('https://www.sogou.com/')
# page.ele('x://*[@id="stb"]').click()

# page.ele('text:“金色画卷”限时上新').click(by_js=False)

if page.ele('text:特朗普'):
  print('yes')

input()