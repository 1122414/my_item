import time
import json
import requests
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

co = ChromiumOptions().headless()
page = ChromiumPage(co)
page.get('https://www.douyin.com/video/7343865995645226292')
cookies = page.cookies(as_dict=True)
# print(cookies)

url = 'https://www.douyin.com/aweme/v1/web/aweme/detail/?'
params = {
  'aid':'6383',
  'aweme_id': '7343865995645226292',
  'cookie_enabled': 'true',
  # 'webid': '7325711541596521995'
  'msToken': 'shPefEUK3-AFbECDLf0M-Xx4xsxl3dUPzVJ1lsv6AnTsa_vkGIdRj3zgdr2NeqLhNAAkl496ZsBOTsrEDglkTq6S6BkvCVhym21MbDh1BiRr9gwg04AkVSwgZnwk6sw=',
  'a_bogus': 'E7RMQfggmEViff6X5f2LfY3q6l33YDzT0trEMD2f-nfr4g39HMPp9exogLhvPgmjN4/kIeYjy4heTrMMx5Q7A3vIH8WKUIcksjSkKl5Q5xSSs1XyeykgrUkw57sAtMa0sv1liQ8koXdnSY8hlxAJ5kIlO62-zo0/9WY=',
  'verifyFp': 'verify_ly9l2y40_1E6GUYnk_fXJi_4mD1_9L49_XXebVnZL3i5A',
  'fp': 'verify_ly9l2y40_1E6GUYnk_fXJi_4mD1_9L49_XXebVnZL3i5A'
}

response = requests.get(url, headers=headers, params=params, cookies=cookies)

print(response)
# print(response.json())
print(response.content)