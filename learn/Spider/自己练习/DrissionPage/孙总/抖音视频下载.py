import os
import requests

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
  'a': '6383',
  'ch': '26',
  'cr': '3',
  'dr': '0',
  'lr': 'all',
  'cd': '0|0|0|3',
  'cv': '1',
  'br': '2247',
  'bt': '2247',
  'cs': '0',
  'ds': '6',
  'ft': 't2zLrtjjM95MxrKqoZmCE1RSYV58UMDtGsvHchyq8_45a',
  'mime_type': 'video_mp4',
  'qs': '0',
  'rc': 'aWY4ZDQ0ZTZnOzU8ZGg6M0BpanY8N2c6ZnU4ZTMzNGkzM0A2NTBfXzEyXjYxYjIxX2EwYSNxYTBpcjQwa2NgLS1kLS9zcw==',
  'btag': '80000e00028000',
  'dy_q': '1742302005',
  'l': '20250318204645C7110DCA7BEBD1359550',
  '__vid': '7124233808735456548'
}
# url = 'https://v5-dy-o-abtest.zjcdn.com/155cafe4028a7af42d544c71c3bcfa7f/67da5b56/video/tos/cn/tos-cn-ve-15/oQOHAEFE9CnfHTmjGgQRPENhIAemvpDXMYJAFB/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=378&bt=378&cs=2&ds=3&ft=CZcaELO_DDhNF5VQ9wly0mahd.JQWk~73-ApQX&mime_type=video_mp4&qs=15&rc=ODY8N2dmOTNpN2dmZWY8OkBpajp2PG45cnBrdDMzNGkzM0BgYTJiNl81X2IxYTFeLTY1YSNlYnFzMmQ0Ni9gLS1kLS9zcw%3D%3D&btag=c0000e00028000&cc=46&cquery=100w_100B_100x_100z_100o&dy_q=1742352587&feature_id=8129a1729e50e93a9e951d2e5fa96ae4&l=20250319104947246E2515EF63834757C1&req_cdn_type=&__vid=7387334010986335540'
# url = 'https://v3-web.douyinvod.com/46c9a57926ec5acdd2d78985cc4ca1a8/67d995fc/video/tos/cn/tos-cn-ve-15c001-alinc2/664b255e80084268a34a347888e02e27/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=2247&bt=2247&cs=0&ds=6&ft=t2zLrtjjM95MxrKqoZmCE1RSYV58UMDtGsvHchyq8_45a&mime_type=video_mp4&qs=0&rc=aWY4ZDQ0ZTZnOzU8ZGg6M0BpanY8N2c6ZnU4ZTMzNGkzM0A2NTBfXzEyXjYxYjIxX2EwYSNxYTBpcjQwa2NgLS1kLS9zcw%3D%3D&btag=80000e00028000&dy_q=1742302005&l=20250318204645C7110DCA7BEBD1359550&__vid=7124233808735456548'
url = 'https://v5-dy-o-abtest.zjcdn.com/b1852d156b8acda745594439cf927abb/67da5f6f/video/tos/cn/tos-cn-ve-15c001-alinc2/o4skIC7aFzAEO7HMlRfJAeyQyA4gpBK2EYNZyh/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=342&bt=342&cs=2&ds=3&ft=CZcaELO_DDhNF5VQ9wAu0mahd.JQWk~73-ApQX&mime_type=video_mp4&qs=15&rc=aWU1NTY7Ozg7Nzg7ODk0M0Bpajw2aDw6ZjU2cDMzNGkzM0BiMzQtXl5gX2AxXy0uLjMzYSNxZW9hcjRnMW1gLS1kLS9zcw%3D%3D&btag=c0000e00028000&cc=46&cquery=100B_100x_100z_100o_100w&dy_q=1742353546&feature_id=8129a1729e50e93a9e951d2e5fa96ae4&l=202503191105468ED4AC3D6B04AE48B587&req_cdn_type=&__vid=7327974972339670324'
response = requests.get(url=url, headers=headers, stream=True)

# //*[@id="douyin-right-container"]/div[2]/div/div/div[1]/div[2]/div/xg-video-container/video
# //*[@id="douyin-right-container"]/div[2]/div/div/div[1]/div[2]/div/xg-video-container/video/source[1]
# /html/body/div[2]/div[1]/div[4]/div[2]/div/div/div[1]/div[2]/div/xg-video-container/video

current_path = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_path, 'test.mp4')

# 保存视频
if response.status_code == 200:
  with open(save_path, 'wb') as f:
      for chunk in response.iter_content(chunk_size=1024 * 1024):  # 每次下载1MB数据
          if chunk:
              f.write(chunk)
  print(f"视频下载完成：{save_path}")
else:
  print(f"请求失败，状态码：{response.status_code}")
