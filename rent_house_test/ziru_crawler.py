import requests
from lxml import etree
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'
}

url = "http://hz.ziroom.com/z/"

htm = requests.get(url, headers=headers).content.decode('UTF-8')

html = etree.HTML(htm)

house_list = html.xpath('//div[@class="Z_list-box"]//div')
# print(house_list)
# print(house_list[0].xpath('./div[@class="clue-content"]/text()'))
# print(house_list[0].xpath('./div[@class="pic-box"]/a/@href')[0])
house = house_list[0].xpath('./div[@class="pic-box"]/a/@href')[0]
new_url = 'https:' + house

house_htm = requests.get(new_url, headers=headers).content.decode('UTF-8')
house_html = etree.HTML(house_htm)

def switch_red(str):
    if str == "0":
        return "6"
    elif str == "30":
        return "1"
    elif str == "60":
        return "9"
    elif str == "90":
        return "7"
    elif str == "120":
        return "4"
    elif str == "150":
        return "5"
    elif str == "180":
        return "0"
    elif str == "210":
        return "8"
    elif str == "240":
        return "3"
    elif str == "270":
        return "2"


def switch(str):
    if str == "0":
        return "7"
    elif str == "30":
        return "2"
    elif str == "60":
        return "6"
    elif str == "90":
        return "3"
    elif str == "120":
        return "8"
    elif str == "150":
        return "4"
    elif str == "180":
        return "0"
    elif str == "210":
        return "1"
    elif str == "240":
        return "9"
    elif str == "270":
        return "5"


def get_price(html):
    price_html = html.xpath('//div[@class="Z_price"]')
    # print(price_html[0].xpath('./span/@class')[0])
    price_h = price_html[0].xpath('.//i[@class="num"]/@style')
    # print(price_html[0].xpath('.//i[@class="num"]/@style'))
    price = "￥"
    # price_math = []
    if price_html[0].xpath('./span/@class')[0] == "red":
        for i in price_h:
            price = price + switch_red(re.findall('background-position:-(.*?)px;', i)[0])
            # price_math.append(re.findall('background-position:-(.*?)px;', i)[0])
            # price_math.append(switch_red(re.findall('background-position:-(.*?)px;', i)[0]))
        # print(re.findall('background-position:(.*?);', price_h[0]))
        # print(price_math)
    else:
        for i in price_h:
            price = price + switch(re.findall('background-position:-(.*?)px;', i)[0])
            # price_math.append(re.findall('background-position:-(.*?)px;', i)[0])
            # price_math.append(switch(re.findall('background-position:-(.*?)px;', i)[0]))
        # print(re.findall('background-position:(.*?);', price_h[0]))
    # print(price)
    return price


price = get_price(house_html)
# print(price)
name = house_html.xpath('/html/body/div[1]/section/aside/h1/text()')[0]
# print(name)
house_info = house_html.xpath('//div[@class="Z_home_b clearfix"]/dl/dd/text()')
square = house_info[0]
direction = house_info[1]
scale = house_info[2]
floor = house_info[3]
content = house_html.xpath('//div[@class="Z_rent_desc"]/text()')[0].replace("\t", "").replace("\n", "")
live_time = house_html.xpath('//li[@class="tip-tempbox"]/span[@class="info_value"]/text()')[0]
time = house_html.xpath('//*[@id="live-tempbox"]/ul/li[2]/span[@class="info_value"]/text()')[0]
# print(content)
# print(time)
# print(live_time)
house_tag = house_html.xpath('/html/body/div[1]/section/aside/div[2]//span/text()')
# print(house_tag)


# price_html = house_html.xpath('//div[@class="Z_price"]')
# print(price_html[0].xpath('./span/@class'))
# price_h = price_html[0].xpath('.//i[@class="num"]/@style')
# print(price_html[0].xpath('.//i[@class="num"]/@style'))
#
# price_math = []
# for i in price_h:
#     price_math.append(re.findall('background-position:-(.*?)px;', i)[0])
# # print(re.findall('background-position:(.*?);', price_h[0]))
# print(price_math)


