import re
import pymysql
import ddddocr
import requests
from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)


# @app.route('/ziru', methods=['get'])
# def your_function():
#     # 从请求中获取数据
#     data = request.json
@app.route('/ziru')
def your_function():
    # 从请求中获取数据
    data = "杭州"
    # 在这里处理你的业务逻辑
    place = process_data(data)
    print(place)
    url = "https://" + place + "ziroom.com/z/"
    house_data = get_ziru_house(url)
    print(house_data)
    # 返回响应
    return jsonify(house_data)


def process_data(data):
    # 你的数据处理逻辑
    if data == "杭州":
        p = 'hz.'
    elif data == "深圳":
        p = 'sz.'
    elif data == "北京":
        p = ''
    elif data == "上海":
        p = 'sh.'
    elif data == "南京":
        p = 'nj.'
    elif data == "成都":
        p = 'cd.'
    elif data == "武汉":
        p = 'wh.'
    elif data == "广州":
        p = 'gz.'
    elif data == "天津":
        p = 'tj.'
    elif data == "苏州":
        p = 'su.'  # 苏州的网页缩写不同
    else:
        p = 'none'

    return p


# 由于价格为图片所拼接，所以我们需要逐个图片识别数字，组合为价格
def get_price_by_ocr(html, ocr):
    position = float(re.findall("background-position: -(.*?)px", html, re.S)[0])
    url = "https:" + re.findall("url\((.*?)\)", html, re.S)[0]
    # print(position)
    # print(url)
    img = requests.get(url).content
    price_math = ocr.classification(img)  # 由于ocr需要开启，所以在运行函数前需要ocr = ddddocr.DdddOcr()
    return price_math[int(position / 20)]


def get_ziru_house(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'
    }
    htm = requests.get(url, headers=headers).content.decode('UTF-8')
    html = etree.HTML(htm)
    house_list = html.xpath('//div[@class="Z_list-box"]//div[@class="item"]')
    ocr = ddddocr.DdddOcr()  # ocr识别需要开启
    all_house = []
    for i in house_list:
        # 注意第五个房屋位置为广告，有两种形式，
        try:
            house = i.xpath('./div[@class="pic-box"]/a/@href')[0]
        except:
            i = house_list[house_list.index(i) + 1]
            house = i.xpath('./div[@class="pic-box"]/a/@href')[0]
        if house == "javascript:;":
            # i = house_list[house_list.index(i) + 1]
            continue

        href = 'https:' + house
        name = i.xpath('./div[@class="info-box"]/h5/a/text()')[0]
        info = i.xpath('./div[@class="info-box"]/div[@class="desc"]/div/text()')[0].replace(" ", "").split('|')
        square = info[0]
        floor = info[1]
        direction = info[2]
        place = i.xpath('./div[@class="info-box"]/div[@class="desc"]/div[@class="location"]/text()')[0].replace(" ",
                                                                                                                "").replace(
            "\n", "").replace("\t", "")
        tags = i.xpath('./div[@class="info-box"]/div[@class="tag"]/span/text()')
        tags = ";".join(tags)
        price_htm = i.xpath('./div[@class="info-box"]/div[@class="price-content"]/div[@class="price red"]/span['
                            '@class="num"]/@style')
        if not price_htm:  # 注意price后面有一个空格
            price_htm = i.xpath('./div[@class="info-box"]/div[@class="price-content"]/div[@class="price "]/span['
                                '@class="num"]/@style')
        price = "￥"
        for j in price_htm:
            price = price + get_price_by_ocr(j, ocr)
        house_data = {
            'name': name,
            'price': price,
            'square': square,
            'place': place,
            'href': href,
            'direction': direction,
            'tags': tags
        }
        all_house.append(house_data)
        # print(house_data)
    return all_house


if __name__ == '__main__':
    app.run(debug=True)
    # house_data = get_ziru_house("http://hz.ziroom.com/z/")
    # print(house_data)

