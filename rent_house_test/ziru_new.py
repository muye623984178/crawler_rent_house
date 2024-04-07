import re
import time

import ddddocr
import pymysql
import requests
from lxml import etree
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
# 指定为无界面模式
# options.add_argument('--headless') # 无法使用无头模式，会导致元素缺失
# option.headless=True  或者将上面的语句换成这条亦可
# options.add_experimental_option('excludeSwitches',
#                                         ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium


# 添加启动参数 (add_argument)
options.add_argument("start-maximized")  # 最大化运行（全屏窗口）,不设置的话取元素会报错
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
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
url = "http://hz.ziroom.com/z/"

driver.get(url)
# driver.add_cookie({"name": "__jsl_clearance_s", "value": "1712458940.221|0|6TVadtL/USEt7jrzm6My108dW1w="})
# driver.add_cookie({"name": "_csrf", "value": "Uo-iVQQMzPxBdNNZ0reZfMXma_xTSEuh"})
# driver.add_cookie({"name": "__jsluid_s", "value": "95fe1c813c4fbb0db20dca65b7c1fdfd"})
# driver.add_cookie({"name": "Hm_lpvt_4f083817a81bcb8eed537963fc1bbf10", "value": "1712459009"})


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


def get_price_by_ocr(html, ocr):
    position = abs(float(re.findall("background-position: (.*?)px", html, re.S)[0]))
    url = "https:" + re.findall('url\("(.*?)"\)', html, re.S)[0]
    # print(position)
    # print(url)
    img = requests.get(url).content
    price_math = ocr.classification(img)  # 由于ocr需要开启，所以在运行函数前需要ocr = ddddocr.DdddOcr()
    return price_math[int(position / 20)]


name_list = driver.find_elements_by_xpath('//div[@class="item"]/div[@class="info-box"]/h5/a')
name = [p.text for p in name_list][:-1]
href = [p.get_attribute('href') for p in name_list][:-1]
info_list = driver.find_elements_by_xpath('//div[@class="info-box"]/div[@class="desc"]/div')
info = [p.text for p in info_list][:-2]
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

# tags_list = driver.find_elements_by_xpath('//div[@class="info-box"]/div[@class="tag"]/span[position()>1]')
# tags = [p.text for p in tags_list][:-1]
# print(tags)
# tag = []
# temp = []
# for t in tags:
#     if '限时立减' in t:
#         tag.append(";".join(temp))
#         temp.append(t)
#     elif t == '':
#         continue
#     else:
#         temp.append(t)
# print(tag)

ocr = ddddocr.DdddOcr()
price_list = driver.find_elements_by_xpath('//div[@class="price-content"]/div[1]')
price = []
for div in price_list:
    spans = div.find_elements_by_class_name('num')
    p = '￥'
    for span in spans:
        # print(span.get_attribute('style'))
        p = p + get_price_by_ocr(span.get_attribute('style'), ocr)
    # print(p)
    price.append(p)
# print(price)

for j in range(len(name)):
    house_data = {
        'name': name[j],
        'price': '￥' + price[j],
        'square': square[j],
        'place': place[j],
        'floor': floor[j],
        'direction': direction[j],
        'href': href[j]
    }
    print(house_data)
