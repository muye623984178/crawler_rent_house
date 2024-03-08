import requests
from lxml import etree
import time
import os

dirpath = "图片/"
if not os.path.exists(dirpath):
    os.mkdir(dirpath)
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'
    }
def get_htm(url):
    ht = requests.get(url, headers=headers).content.decode('UTF-8')
    htm = etree.HTML(ht)
    return htm

def get_photo_save():
    url = "https://sc.chinaz.com/tupian/huanghuntupian.html"
    photos = get_htm(url).xpath('/html/body/div[3]/div[2]/div')
    for photo in photos:
        photo1 = "https:" + photo.xpath('./img/@data-original')[0]
        name = photo.xpath('./img/@alt')[0]
        # print(photo1)
        # print(name)
        response = requests.get(photo1, headers=headers)
        with open(dirpath + name + ".jpg", "wb") as f:
            f.write(response.content)
            print(name + "下载成功")

if __name__ == '__main__':
    start = time.time()
    get_photo_save()
    end = time.time()
    running_time = end - start
    print('总共消耗%f.5秒'%running_time)










