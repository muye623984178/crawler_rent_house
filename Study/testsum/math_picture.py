import re

import ddddocr
import requests

ocr = ddddocr.DdddOcr()


# # with open(r'C:\Users\62398\Pictures\联想截图\1.png', 'rb') as f:
# #     img = f.read()
# img = requests.get("https://static8.ziroom.com/phoenix/pc/images/2019/price/eb0d3275f3c698d1ac304af838d8bbf0.png").content
# res = ocr.classification(img)
# print(res)
# # n = 93.72
# # print(int(n/30))
# # print(res[int(n/30)])

def get_price_by_img(src):
    img = requests.get(src).content
    res = ocr.classification(img)
    print(res)
    return res


# get_price_by_img("https://static8.ziroom.com/phoenix/pc/images/2019/price/eb0d3275f3c698d1ac304af838d8bbf0.png")

# background-position:-30px;background-image: url(//static8.ziroom.com/phoenix/pc/images/2020/info/img_pricenumber_detail_red.png)

def get_price_by_ocr(html):
    position = int(re.findall("background-position:-(.*?)px", html, re.S)[0])
    url = "https:" + re.findall("url\((.*?)\)", html, re.S)[0]
    # print(position)
    # print(url)
    img = requests.get(url).content
    price_math = ocr.classification(img)
    # print(price_math[int(position/30)])
    return price_math[int(position/30)]

get_price_by_ocr(
    "background-position:-30px;background-image: url(//static8.ziroom.com/phoenix/pc/images/2020/info/img_pricenumber_detail_red.png)")
