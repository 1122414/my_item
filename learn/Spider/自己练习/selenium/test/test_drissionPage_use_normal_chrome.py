from DrissionPage import ChromiumPage,ChromiumOptions

co = ChromiumOptions().set_browser_path(r'C:\Program Files\Google\Chrome\Application\chrome.exe')

page = ChromiumPage(addr_or_opts=co)
page.get('http://www.baidu.com')