from selenium import webdriver

driver = webdriver.Chrome()
# 读取js文件内容
with open(r'C:\Users\Lenovo\Desktop\vscode_python\2024.7哔站爬虫\自己练习\selenium\test\stealth.min.js','r',encoding='utf-8') as fp:
    content = fp.read()
# 处理selenium中webdriver特征值
driver.execute_cdp_cmd(
    'Page.addScriptToEvaluateOnNewDocument',
    {
        'source':content
    }
)

driver.get('https://hackforums.net/')

input()