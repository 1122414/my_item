from DrissionPage import ChromiumPage,ChromiumOptions
page = ChromiumPage()
page.get('https://www.baidu.com/')

tab = page.tab_ids

page.close_tabs(tabs_or_ids = tab)

input()