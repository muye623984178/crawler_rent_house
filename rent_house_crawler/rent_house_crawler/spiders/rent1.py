import scrapy
import re

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


class Rent1Spider(scrapy.Spider):
    name = "rent1"
    allowed_domains = ["hz.ziroom.com"]
    start_urls = ["http://hz.ziroom.com/z/"]
    new_url = "https://hz.ziroom.com/z/p%d-q950791567437910017-a950791567437910017/"

    def parse(self, response):
        # pass
        house_list = response.xpath('//div[@class="Z_list-box"]//div')
        # print(house_list)
        house = house_list[0].xpath('./div[@class="pic-box"]/a/@href')[0].extract()
        # print(house)
        new_url = 'https:' + house
        print(new_url)
