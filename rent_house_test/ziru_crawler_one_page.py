import re

import ddddocr
import requests
from lxml import etree
import requests
import pymysql


# 由于价格为图片所拼接，所以我们需要逐个图片识别数字，组合为价格
def get_price_by_ocr(html):
    # style="background-image: url(//static8.ziroom.com/phoenix/pc/images/2020/list/img_pricenumber_list_red.png);background-position: -140px"
    position = int(re.findall("background-position: -(.*?)px", html, re.S)[0])
    url = "https:" + re.findall("url\((.*?)\)", html, re.S)[0]
    # print(position)
    # print(url)
    img = requests.get(url).content
    price_math = ocr.classification(img)    # 由于ocr需要开启，所以在运行函数前需要ocr = ddddocr.DdddOcr()
    # print(price_math[int(position/30)])
    return price_math[int(position/20)]

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

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'
}
url = "https://hz.ziroom.com/z/"
htm = requests.get(url, headers=headers).content.decode('UTF-8')
html = etree.HTML(htm)
house_list = html.xpath('//div[@class="Z_list-box"]//div[@class="item"]')


ocr = ddddocr.DdddOcr() # ocr识别需要开启
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
    # print(name)
    # print(href)
    info = i.xpath('./div[@class="info-box"]/div[@class="desc"]/div/text()')[0].replace(" ", "").split('|')
    # print(info)
    square = info[0]
    floor = info[1]
    direction = info[2]
    place = i.xpath('./div[@class="info-box"]/div[@class="desc"]/div[@class="location"]/text()')[0].replace(" ", "").replace("\n", "").replace("\t", "")
    # print(place)
    tags = i.xpath('./div[@class="info-box"]/div[@class="tag"]/span/text()')
    tags = ";".join(tags)
    # print(tags)
    price_htm = i.xpath('./div[@class="info-box"]/div[@class="price-content"]/div[@class="price red"]/span['
                        '@class="num"]/@style')
    price = "￥"
    for j in price_htm:
        price = price + get_price_by_ocr(j)
    # print(price)

    house_data = {
        'name': name,
        'price': price,
        'square': square,
        'place': place,
        'href': href,
        'direction': direction,
        'tags': tags
    }
    print(house_data)
    with MysqlTool() as db:
        sql = ("INSERT INTO ziru1(name, price, square, place, direction, tag, href) VALUES ("
               "%s, %s, %s, %s, %s, %s, %s)")
        args = (name, price, square, place, direction,  tags, href)
        db.execute(sql, args, commit=True)
