import requests
if __name__ == '__main__':
    url = 'https://www.sogou.com/'
    sogou_response = requests.get(url)
    sougou_text = sogou_response.text
    print(sougou_text)
    with open('./sogou.html', 'w',encoding='utf-8') as fp:
        fp.write(sougou_text)
    print("Done")