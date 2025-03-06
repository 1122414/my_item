from DrissionPage import ChromiumPage,ChromiumOptions
page = ChromiumPage()
page.get('https://www.baidu.com/')
page.ele('x://*[@id="su"]')

page.get('https://www.sogou.com/')
page.ele('x://*[@id="stb"]').click()

input()