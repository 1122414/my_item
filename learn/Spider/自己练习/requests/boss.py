import os
import requests
from time import sleep


from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Cookie':'wd_guid=c322cd77-411d-44bb-a911-7b41827c27c9; historyState=state; _bl_uid=0Clmyt1U9UdzmtdI7hs5pdmtwOba; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1723457284; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1723457284; HMACCOUNT=C1C6C1E6B4A3F980; __zp_seo_uuid__=3bbc5163-3dfa-41ba-a688-2a27d4119c46; __g=-; lastCity=100010000; __c=1723457284; __l=r=http%3A%2F%2F127.0.0.1%3A5500%2F&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fcity%3D101190100%26position%3D100109%26page%3D1&s=3&friend_source=0&g=&s=3&friend_source=0; __a=43003532.1709377413.1712837104.1723457284.33.6.19.19; __zp_stoken__=a2eafw4vDncOlCT9aCVVYBU11dl%2FDgk9XYFLCrcK3blPCr1ZWwrZfZcKhQ8KcUMKZVsKoZcKlY8KXwq3ChsKowq3CscO%2BVcSAScKQXMSAwpnCosShxIHDg0nDkMO6wrXCmzskDwkJDg1%2BdHR%2FwoAHERIFBgULCwgHCBISBQZAMcO1cDBCNzxCL0ROThBDU2BFU08NWkZPQT9ZBwhcPys1QkE7wrpnwr4MwrXCosK5FcK3wpjCuSJCOTs1wrhqLi7CuMOGBmoPwrhCDhYPwrgsXcORVcKPJMKYwrvClDE3PMOBxLw8OCA3Qjg%2BOzwzODgwPCPDhVvChDDClcK3wpArQSJAODszQDg4OzVCPiQ7OhomOEIxNg0MCgcRJzvCvsOCwrvDmzg7'
}

url = "https://www.zhipin.com/job_detail/?query=Python%E5%BC%80%E5%8F%91&city=100010000"
current_path = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(current_path, 'boss.html')
with open(full_path, 'w', encoding='utf-8') as f:
    f.write(requests.get(url, headers=headers).text)
params = {
    'city': '101190100',
    'position': '100109',
    'page': 1
}
response = requests.get(url, headers=headers)
page_text = response.text

print(page_text)