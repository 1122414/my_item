import platform
# from puppeteer import launch
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger
 
 
def get_free_ip():
    # url = "https://www.zdaye.com/free/?ip=&adr=&checktime=&sleep=1&cunhuo=&dengji=1&nadr=&https=&yys=&post=&px="
    # browser.get(url, retry=3, interval=1, timeout=15)
    # ip_ports = []
    # for tr in browser.eles('x://table[@id="ipc"]//tr')[1:]:
    #     tds = [td.text for td in tr.eles("x://td")]
    #     ip_ports.append((f"{tds[0]}:{tds[1]}", tds[3]))
    # print(len(ip_ports), ip_ports)
    url = 'http://www.zdopen.com/ShortProxy/GetIP/?api=202408221648199053&akey=8ecbfdf5c2b8c2a0&timespan=2&type=1'
    rsponse = requests.get(url).text
    ip_ports = rsponse.split('\r\n')
    
    return ip_ports
 
 
def switch_ip(ip_port=None):
    global set_proxy
    if ip_port:
        # 设置proxy
        ip, port = ip_port.split(":")
        tab = browser.new_tab()
        tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
        tab.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
        tab.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
        tab.ele('x://a[@ng-click="applyOptions()"]').click()
        tab.wait(1)
        # 提示框
        txt = tab.handle_alert()
        print("提示框", txt)
        tab.handle_alert(accept=False)
        if not omega_proxy:
            # 切换proxy
            tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            tab.wait(1)
            tab.ele('x://span[text()="proxy"]').click()
            set_proxy = True
    else:
        tab = browser.new_tab()
        tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
        tab.ele('x://span[text()="[直接连接]"]').click()
    if len(browser.tab_ids) > 1:
        print("当前tab个数", len(browser.tab_ids))
        tab.close()
 
def query_ip():
    browser.get("https://www.baidu.com/s?ie=UTF-8&wd=ip", retry=0)
    browser.wait(10)
    ip_address = '归属地：'+browser.ele('.c-fwb cu-font-bold').text
    id_operator = '运营商：'+browser.eles('.result-content_4C7SO')[0].text
    ip_self = '本机ip：'+browser.eles('.result-content_4C7SO')[1].text
    html_text = ip_address+'>>>>'+id_operator+'>>>>'+ip_self
    return html_text
 
if platform.system().lower() == 'windows':
    co = ChromiumOptions()  # .set_paths(browser_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
else:
    co = ChromiumOptions().set_paths(browser_path=r"/opt/google/chrome/google-chrome")
    co.headless(True)  # 设置无头加载  无头模式是一种在浏览器没有界面的情况下运行的模式，它可以提高浏览器的性能和加载速
    # co.incognito(True)  # 无痕隐身模式打开的话，不会记住你的网站账号密码的
    co.set_argument('--no-sandbox')  # 禁用沙箱 禁用沙箱可以避免浏览器在加载页面时进行安全检查,从而提高加载速度 默认情况下，所有Chrome 用户都启用了隐私沙盒选项  https://zhuanlan.zhihu.com/p/475639754
    co.set_argument("--disable-gpu")  # 禁用GPU加速可以避免浏览器在加载页面时使用过多的计算资源，从而提高加载速度
    co.set_user_agent(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')  # 设置ua
 
co.set_timeouts(6, 6, 6)
co.set_local_port(9211)
# 1、设置switchyOmega插件
co.add_extension(r"D:\proxy_switchyomega-2.5.20-an+fx")
browser = ChromiumPage(co)
 
# 2、重置switchyOmega插件
omega_proxy = False
switch_ip()

# 查询现在的ip
html_text = query_ip()
logger.success(f"\n>>>>当前的ip： {html_text}")
 
# 3、随机切换代理ip
ip_all = get_free_ip()
# ip_all = [{"ip": "10.1.3.56", "port": 7890, "expire_time": "2024-04-27 22:24:00"}]
for ips in ip_all:
    logger.info(f"~~~切换ip，now {ips}")
    # 重置switchyOmega插件
    ip = ips[:ips.index(':')]
    port = ips[ips.index(':')+1:]
    switch_ip(f"{ip}:{port}")
    browser.wait(1)
    try:
        html_text = query_ip()
        logger.success(f">>>>>>>>切换代理成功： {html_text}")
    except Exception as err:
        logger.error(f"----------切换代理失败 dp {err}")
    browser.wait(10)
browser.quit()