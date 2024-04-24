# s = "12.3㎡ | 31/33层 | 朝南"
# print(s.replace(" ", "").split('|'))
import re
import time

import pymysql
import requests
from flask import jsonify
from selenium import webdriver
import ddddocr


# # 连接数据库
# db = pymysql.connect(host='localhost', user='root', password='root', db='rent_house')
# cursor = db.cursor()
# sql = 'SELECT houseId FROM store_info WHERE userId=%s'
# openId = 'oWoWf5AO2X81wOjaQehQtSEK3Nr4'
# try:
#     cursor.execute(sql, openId)
#     result = cursor.fetchall()
#     favoriteMap = {}
#     for item in result[:-1]:
#         favoriteMap[item[0]] = True
#     print(favoriteMap)
#     print(type(favoriteMap))
#
# except Exception as e:
#     print(f"An error occurred: {e}")
#     print({'error': str(e)}, 500)

# 若存在图片型价格，数字由图片偏移量确定
def get_price_by_ocr(html, ocr):
    position = abs(float(re.findall("background-position: (.*?)px", html, re.S)[0]))
    url = "https:" + re.findall('url\("(.*?)"\)', html, re.S)[0]
    # print(position)
    # print(url)
    img = requests.get(url).content
    price_math = ocr.classification(img)  # 由于ocr需要开启，所以在运行函数前需要ocr = ddddocr.DdddOcr()
    return price_math[int(position / 20)]


def get_ziru_house_new(url, ocr, area):
    options = webdriver.ChromeOptions()
    # 无法使用无头模式，会导致元素缺失
    # options.add_argument('--headless')
    # 添加启动参数 (add_argument)
    options.add_argument("start-maximized")  # 最大化运行（全屏窗口）,不设置的话取元素会报错
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36")
    # 创建Chrome驱动程序的实例
    driver = webdriver.Chrome(options=options)
    # 此步骤很重要，防止被各大网站识别出来使用了Selenium
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.get(url)
    time.sleep(3)  # 因为为js渲染的动态网页，所以必须强制等待其加载完毕
    # 爬取可以简单获取的房屋信息
    name_list = driver.find_elements_by_xpath('//div[@class="item"]/div[@class="info-box"]/h5/a')
    name = [p.text for p in name_list][:-1]
    href = [p.get_attribute('href') for p in name_list][:-1]
    info_list = driver.find_elements_by_xpath('//div[@class="info-box"]/div[@class="desc"]/div')
    info = [p.text for p in info_list][:-2]
    print(info)
    place = info[1::2]
    info = info[::2]
    square = []
    floor = []
    direction = []
    for p in info:
        s = p.replace(" ", "").split('|')
        square.append(s[0])
        floor.append(s[1])
        direction.append(s[2])

    # 爬取标签，并标准化标签数据
    tags_list = driver.find_elements_by_xpath('//div[@class="info-box"]/div[@class="tag"]')
    tags = []
    for div in tags_list:
        spans = div.find_elements_by_tag_name("span")
        tag = ''
        for span in spans:
            if span.text == '':
                continue
            elif "限时立减" in span.text:
                tag = tag + span.text[0:-2] + ';'
            else:
                tag = tag + span.text + ';'
        tags.append(tag[0:-1])

    # 爬取价格
    price_list = driver.find_elements_by_xpath('//div[@class="price-content"]/div[1]')
    price = []
    for div in price_list:
        spans = div.find_elements_by_class_name('num')
        p = ''
        for span in spans:
            p = p + get_price_by_ocr(span.get_attribute('style'), ocr)
        price.append(p)

    # 爬取房屋图片
    a_list = driver.find_elements_by_xpath('//div[@class="item"]/div[@class="pic-box"]/a[@target="_blank"]')
    img_list = []
    for a in a_list:
        img = a.find_element_by_xpath('./img')
        src = img.get_attribute('src')
        if "imgpro" in src:
            img_list.append(src)
        elif "webimg" in src:
            img_list.append(img.get_attribute('data-original'))
        else:
            print("爬取房屋图片有未知错误")

    all_house = []
    # 房屋信息整合
    for j in range(len(name)):
        house_data = {
            'name': name[j],
            'price': price[j] + " 元/月",
            'square': square[j],
            'place': place[j],
            'floor': floor[j],
            'direction': direction[j],
            'href': href[j],
            'tags': tags[j],
            'img_src': img_list[j],
            'area': area
        }
        print(house_data)

    driver.quit()
    return all_house

ocr = ddddocr.DdddOcr()  # ocr识别需要开启
ziru = "http://hz.ziroom.com/z/"
get_ziru_house_new(ziru,ocr,'杭州')