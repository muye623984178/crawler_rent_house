import re
import time

import ddddocr
import pymysql
import requests
from lxml import etree
from selenium import webdriver


# 连接数据库
class MysqlTool:
    def __init__(self):
        """mysql 连接初始化"""
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = 'root'
        self.db = 'rent_house'
        self.charset = 'utf8'
        self.mysql_conn = None

    def __enter__(self):
        """打开数据库连接"""
        self.mysql_conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password,
            db=self.db,
            charset=self.charset
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """关闭数据库连接"""
        if self.mysql_conn:
            self.mysql_conn.close()
            self.mysql_conn = None

    def execute(self, sql: str, args: tuple = None, commit: bool = False) -> any:
        """执行 SQL 语句"""
        try:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    self.mysql_conn.commit()
                    # print(f"执行 SQL 语句：{sql}，参数：{args}，数据提交成功")
                else:
                    result = cursor.fetchall()
                    # print(f"执行 SQL 语句：{sql}，参数：{args}，查询到的数据为：{result}")
                    return result
        except Exception as e:
            print(f"执行 SQL 语句出错：{e}")
            self.mysql_conn.rollback()
            raise e


# 设定请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
                  'Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'
}


# 若存在图片型价格，数字由图片偏移量确定
def get_price_by_ocr(html, ocr):
    position = float(re.findall("background-position: -(.*?)px", html, re.S)[0])
    url = "https:" + re.findall("url\((.*?)\)", html, re.S)[0]
    # print(position)
    # print(url)
    img = requests.get(url).content
    price_math = ocr.classification(img)  # 由于ocr需要开启，所以在运行函数前需要ocr = ddddocr.DdddOcr()
    return price_math[int(position / 20)]


# 获取自如网站的房屋信息
def get_ziru_house(url, ocr):
    # print(url)
    htm = requests.get(url, headers=headers).content.decode('UTF-8')
    print(htm)
    html = etree.HTML(htm)
    # print(html)
    house_list = html.xpath('//div[@class="Z_list-box"]//div[@class="item"]')
    print(house_list)
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
        print(house_data)
    return all_house


def get_lianjia_house(url):
    htm = requests.get(url, headers=headers).content.decode('UTF-8')
    html = etree.HTML(htm)
    house_list = html.xpath('//div[@class="content__list"]/div')
    all_house = []
    for house in house_list:
        # 注意独栋公寓的不同
        name = house.xpath('./a/@title')[0]
        # print(name)
        href = "https://hz.lianjia.com" + house.xpath('./a/@href')[0]
        # print(href)
        price = house.xpath('./div/span[@class="content__list--item-price"]/em/text()') + house.xpath('./div/span['
                                                                                                      '@class'
                                                                                                      '="content__list'
                                                                                                      '--item-price'
                                                                                                      '"]/text()')
        price = "".join(price)
        # print(price)
        place = "-".join(house.xpath('./div/p[@class="content__list--item--des"]/a/text()'))
        if place == "":
            place = name
        # print(place)
        info = house.xpath('./div/p[@class="content__list--item--des"]/text()')
        # print(len(info))
        if len(info) == 8:
            info = info[4:-1]
            direction = info[1].replace("\n", "").replace(" ", "")
        elif len(info) == 5:
            info = info[2:6]
            direction = ""
        square = info[0].replace("\n", "").replace(" ", "")
        scale = info[2].replace("\n", "").replace(" ", "")
        # print(info)
        # print(square)
        # print(direction)
        # print(scale)
        tags = house.xpath('./div/p[@class="content__list--item--bottom oneline"]/i/text()')
        tags = ";".join(tags)
        # print(tags)
        house_data = {
            'name': name,
            'price': price,
            'square': square,
            'place': place,
            'scale': scale,
            'direction': direction,
            'tags': tags,
            'href': href
        }
        print(house_data)
        all_house.append(house_data)
    return all_house


def get_5a5j_house(url):
    option = webdriver.ChromeOptions()
    # 指定为无界面模式
    option.add_argument('--headless')
    # option.headless=True  或者将上面的语句换成这条亦可
    # 创建Chrome驱动程序的实例
    driver = webdriver.Chrome(options=option)

    # driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)  # 因为为js渲染的动态网页，所以必须强制等待其加载完毕

    name_list = driver.find_elements_by_xpath('//ul[@class="pList rentList"]//li//div[@class="listCon"]/h3/a')
    # print(len(p_list))
    name = [p.text for p in name_list][:-1]
    # print(name)
    href = [p.get_attribute('href') for p in name_list][:-1]
    # print(href)
    price_list = driver.find_elements_by_xpath('//p[@class="redC"]/strong')
    price = [p.text for p in price_list][:-1]
    # print(price)
    place_list = driver.find_elements_by_xpath('//div[@class="listX"]/p[2]')
    place = [p.text for p in place_list][:-1]
    # print(place)
    info_list = driver.find_elements_by_xpath('//div[@class="listX"]/p[1]')
    info = [p.text for p in info_list][:-1]
    # print(info)
    scale = []
    square = []
    floor = []
    decorate = []
    all_house = []
    for i in info:
        i = i.split('·')
        # print(i)
        # print(len(i))
        scale.append(i[0].replace(" ", ""))
        square.append(i[1].replace(" ", ""))
        floor.append(i[3].replace(" ", ""))
        decorate.append(i[4].replace(" ", ""))

    for j in range(len(name)):
        house_data = {
            'name': name[j],
            'price': '￥' + price[j],
            'square': square[j],
            'place': place[j],
            'scale': scale[j],
            'floor': floor[j],
            'decorate': decorate[j],
            'href': href[j]
        }
        print(house_data)
        all_house.append(house_data)
    return all_house


if __name__ == '__main__':
    ocr = ddddocr.DdddOcr()  # ocr识别需要开启
    ziru = "http://hz.ziroom.com/z/"
    lianjia = "https://hz.lianjia.com/zufang/"
    wojia = "https://hz.5i5j.com/zufang/"
    # get_ziru_house("http://hz.ziroom.com/z/", ocr)
    # get_lianjia_house("https://hz.lianjia.com/zufang/")
    # get_5a5j_house("https://hz.5i5j.com/zufang/")
    i = 2
    new_ziru = ziru + "p" + str(i) + "-q961410684041994241-a961410684041994241/"
    new_lianjia = lianjia + "pg" + str(i) + "/#contentList"
    new_wojia = wojia + "n" + str(i) + "/"
    # print(new_wojia)
    print(new_ziru)
    # print(new_lianjia)
    # get_lianjia_house(new_lianjia)
    # get_5a5j_house(new_wojia)
    get_ziru_house(new_ziru, ocr)

