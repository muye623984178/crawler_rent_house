import requests
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'
}
url = "https://bj.zu.ke.com/zufang"

htm = requests.get(url, headers=headers).content.decode('UTF-8')

html = etree.HTML(htm)

house_list = html.xpath('//*[@id="content"]/div[1]/div[1]/*')
# print(house_list)
# print(etree.tostring(house_list[0]))
# num = 0+63.

for house in house_list:
    house = house.xpath('./div')
    title = house[0].xpath('./p[1]/a/text()')[0].replace(" ", "").replace("\n", "")
    # print(title)
    pla = house[0].xpath('./p[2]/a')
    try:
        place = pla[0].xpath('./text()')[0] + '-' + pla[1].xpath('./text()')[0] + '-' + pla[2].xpath('./text()')[0]
    except Exception as err:
        print(title)
    # print(place)
    square = house[0].xpath('./p[2]/text()[5]')[0].replace(" ", "").replace("\n", "")
    # print(square)
    direction = house[0].xpath('./p[2]/text()[6]')[0].replace(" ", "").replace("\n", "")
    # print(direction)
    scale = house[0].xpath('./p[2]/text()[7]')[0].replace(" ", "").replace("\n", "")
    # print(scale)
    price = house[0].xpath('./span/em/text()')[0] + house[0].xpath('./span/text()')[0]
    # print(price)
    floor = house[0].xpath('p[2]/span/text()[2]')[0].replace(" ", "").replace("\n", "")
    # print(floor)
    house_data = {
        "title": title,
        "scale": scale,
        "place": place,
        "square": square,
        "price": price,
        "floor": floor,
        "direction": direction
    }
    print(house_data)
    # num = num + 1
    # print(num)
# 单个测试
# house = house_list[0].xpath('./div')
# title = house[0].xpath('./p[1]/a/text()')[0].replace(" ", "").replace("\n", "")
# print(title)
# pla = house[0].xpath('./p[2]/a')
# place = pla[0].xpath('./text()')[0] + '-' + pla[1].xpath('./text()')[0] + '-' + pla[2].xpath('./text()')[0]
# print(place)
# square = house[0].xpath('./p[2]/text()[5]')[0].replace(" ", "").replace("\n", "")
# print(square)
# direction = house[0].xpath('./p[2]/text()[6]')[0].replace(" ", "").replace("\n", "")
# print(direction)
# scale = house[0].xpath('./p[2]/text()[7]')[0].replace(" ", "").replace("\n", "")
# print(scale)
# price = house[0].xpath('./span/em/text()')[0] + house[0].xpath('./span/text()')[0]
# print(price)
# floor = house[0].xpath('p[2]/span/text()[2]')[0].replace(" ", "").replace("\n", "")
# print(floor)



