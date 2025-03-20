import requests

url_data = 'https://xcx.cxsjqy.cn:8085/get_data'

data = {"links": [{"url":"0.05 复制打开抖音，看看【胖龙龙的作品】后续，上市公司总裁骗钱全过程  https://v.douyin.com/irgx6D6v/Gic:/K@W.MW08/18","userId":"1","numberId":"2"},{ "url":"5.69 复制打开抖音，看看【🌈孔肥肥*的作品】高速路上遇到的修狗狗🐶 一家子整整齐齐🥰 # 被小... https://v.douyin.com/irgxMK4X/ PKw:/ 10/01 x@s.Eh ","userId":"1","numberId":"2"},{"url":"6.48 复制打开抖音，看看【风起时相拥的图文作品】# java  https://v.douyin.com/irgaj2HH/ 07/16 CuS:/ K@W.mD ","userId":"1", "numberId":"2"}]
}
# requests.packages.urllib3.disable_warnings()
response = requests.post(url_data, json=data,verify=False)
if response.status_code == 200:
    print(response.json())
else:
    print(f'请求失败{response.status_code}')