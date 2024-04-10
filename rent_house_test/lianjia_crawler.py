import requests
from lxml import etree
import requests
import pymysql


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
url = "https://hz.lianjia.com/zufang/pg7/#contentList"
htm = requests.get(url, headers=headers).content.decode('UTF-8')
html = etree.HTML(htm)
house_list = html.xpath('//div[@class="content__list"]/div')

# # 单个房屋信息爬虫
# house_url = "https://hz.lianjia.com" + house_list[0].xpath('./a/@href')[0]
# # print(house_url)
# house_htm = requests.get(house_url, headers=headers).content
# house_html = etree.HTML(house_htm)

for house in house_list:
    # 注意独栋公寓的不同
    name = house.xpath('./a/@title')[0]
    # print(name)
    href = "https://hz.lianjia.com" + house.xpath('./a/@href')[0]
    print(href)
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
    # print(info)
    # print(len(info))
    if len(info) == 8:
        # 如['\n                ', '-', '-', '\n        ', '\n        89.00㎡\n        ', '南        ', '\n
        # 3室1厅1卫        ', '\n      ']
        info = info[4:-1]
        direction = info[1].replace("\n", "").replace(" ", "")
    elif len(info) == 5:
        info = info[2:6]
        direction = ""
    elif len(info) == 9:
        # 即info中含有精选 如['\n                  精选          ', '\n                ', '-', '-', '\n        ', '\n
        # 8.70㎡\n        ', '南        ', '\n          4室1厅1卫        ', '\n      ']
        info = info[5:-1]
        direction = info[1].replace("\n", "").replace(" ", "")

    square = info[0].replace("\n", "").replace(" ", "")
    scale = info[2].replace("\n", "").replace(" ", "")
    # print(direction)
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
    with MysqlTool() as db:
        sql = ("INSERT INTO lianjia(name, price, square, place, scale, direction, tag, href) VALUES ("
               "%s, %s, %s, %s, %s, %s, %s ,%s)")
        args = (name, price, square, place, scale, direction, tags, href)
        db.execute(sql, args, commit=True)
