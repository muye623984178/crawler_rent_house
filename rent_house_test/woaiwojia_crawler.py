import time
import pymysql
import requests
from lxml import etree
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

option = webdriver.ChromeOptions()
# 指定为无界面模式
option.add_argument('--headless')
# option.headless=True  或者将上面的语句换成这条亦可
# 创建Chrome驱动程序的实例
driver = webdriver.Chrome(options=option)

url = "https://hz.5i5j.com/zufang/"
# driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)  # 因为为js渲染的动态网页，所以必须强制等待其加载完毕


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


name_list = driver.find_elements_by_xpath('//ul[@class="pList rentList"]//li//div[@class="listCon"]/h3/a')
# print(len(p_list))
name = [p.text for p in name_list][:-1]
# print(name)
href = [p.get_attribute('href') for p in name_list][:-1]
# print(href)
img_list = driver.find_elements_by_xpath('//ul[@class="pList rentList"]/li/div[@class="listImg"]/a/img')
img_src = []
for p in img_list:
    q = p.get_attribute('src')
    if "5i5j.com" in q or "aihome365.cn" in q:
        img_src.append(q)
    elif "data:image/png" in q:
        img_src.append(p.get_attribute('data-src'))
    else:
        print("爬取图片链接出现未知错误" + p.get_attribute('title'))
# print(img_src)

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
# decorate = []
for i in info:
    i = i.split('·')
    # print(i)
    # print(len(i))
    scale.append(i[0].replace(" ", ""))
    square.append(i[1].replace(" ", ""))
    floor.append(i[3].replace(" ", ""))
    # decorate.append(i[4].replace(" ", ""))

tags_list = driver.find_elements_by_xpath('//div[@class="listCon"]/div[@class="listTag rentListTag"]')
tags = []
for p in tags_list:
    span = p.find_elements_by_xpath('./span')
    tag = [i.text for i in span]
    tags.append(';'.join(tag))
    # print(';'.join(tag))

with MysqlTool() as db:
    for j in range(len(name)):
        house_data = {
            'name': name[j],
            'price': price[j] + " 元/月",
            'square': square[j],
            'place': place[j],
            'scale': scale[j],
            'floor': floor[j],
            # 'decorate': decorate[j],
            'href': href[j],
            'img_src': img_src[j],
            'tag': tags[j]
        }
        print(house_data)
        sql = ("INSERT INTO woaiwojia(name, price, square, place, scale, floor, href, img_src, tag) VALUES ("
               "%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        args = (name[j], price[j] + " 元/月", square[j], place[j], scale[j], floor[j], href[j], img_src[j], tags[j])
        db.execute(sql, args, commit=True)
