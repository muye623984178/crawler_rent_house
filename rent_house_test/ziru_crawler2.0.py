import requests
from lxml import etree
import re
import ddddocr
import pymysql

import pymysql

# 数据库封装
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


# 由于价格为图片所拼接，所以我们需要逐个图片识别数字，组合为价格
def get_price_by_ocr(html):
    position = int(re.findall("background-position:-(.*?)px", html, re.S)[0])
    url = "https:" + re.findall("url\((.*?)\)", html, re.S)[0]
    # print(position)
    # print(url)
    img = requests.get(url).content
    price_math = ocr.classification(img)    # 由于ocr需要开启，所以在运行函数前需要ocr = ddddocr.DdddOcr()
    # print(price_math[int(position/30)])
    return price_math[int(position/30)]


# 第一步，先获取房屋列表，以及房屋详细信息界面链接
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'
}
url = "http://hz.ziroom.com/z/"
htm = requests.get(url, headers=headers).content.decode('UTF-8')
html = etree.HTML(htm)
house_list = html.xpath('//div[@class="Z_list-box"]//div[@class="item"]')


# 第二步，逐个访问详细信息界面，获取房屋信息
ocr = ddddocr.DdddOcr() # ocr识别需要开启
for i in house_list:
    # 解决房屋链接中掺杂广告，导致爬虫无法继续的问题
    try:
        house = i.xpath('./div[@class="pic-box"]/a/@href')[0]
    except:
        i = house_list[house_list.index(i) + 1]
        house = i.xpath('./div[@class="pic-box"]/a/@href')[0]
    if house == "javascript:;":
        i = house_list[house_list.index(i) + 1]
        continue
    new_url = 'https:' + house
    house_htm = requests.get(new_url, headers=headers).content.decode('UTF-8')
    house_html = etree.HTML(house_htm)
    price_htm = house_html.xpath('/html/body/div[1]/section/aside/div[1]//i/@style')
    price = "￥"
    for j in range(0,4):
        price = price + get_price_by_ocr(price_htm[j])
    # print(price)
    name = house_html.xpath('/html/body/div[1]/section/aside/h1/text()')[0]
    house_info = house_html.xpath('//div[@class="Z_home_b clearfix"]/dl/dd/text()')
    square = house_info[0]
    direction = house_info[1]
    scale = house_info[2]
    floor = house_info[3]
    content = house_html.xpath('//div[@class="Z_rent_desc"]/text()')[0].replace("\t", "").replace("\n", "")
    live_time = house_html.xpath('//li[@class="tip-tempbox"]/span[@class="info_value"]/text()')[0].replace("\t",
                                                                                                           "").replace(
        " ", "")
    try:
        time = house_html.xpath('//*[@id="live-tempbox"]/ul/li[2]/span[@class="info_value"]/text()')[0]
    except:
        time = None

    house_tag =(";").join(house_html.xpath('/html/body/div[1]/section/aside/div[2]//span/text()'))
    # print(house_tag)

    house_data = {
        "name": name,
        "price": price,
        "square": square,
        "scale": scale,
        "direction": direction,
        "floor": floor,
        "content": content,
        "time": time,
        "live_time": live_time,
        "tag": house_tag
    }
    with MysqlTool() as db:
        # INSERT INTO ziru(name, price, square, scale, direction, floor, content, time, live_time, tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        sql = ("INSERT INTO ziru(name, price, square, scale, direction, floor, content, time, live_time, tag) VALUES ("
               "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        args = (name, price, square, scale, direction, floor, content, time, live_time, house_tag)
        db.execute(sql, args, commit=True)
    print(house_data)


# 第三步，保存数据到数据库（实际上在上面已经包括）