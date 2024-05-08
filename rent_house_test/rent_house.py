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
    position = abs(float(re.findall("background-position: (.*?)px", html, re.S)[0]))
    url = "https:" + re.findall('url\("(.*?)"\)', html, re.S)[0]
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


def get_lianjia_house(url, area):
    htm = requests.get(url, headers=headers).content.decode('UTF-8')
    html = etree.HTML(htm)
    house_list = html.xpath('//div[@class="content__list"]/div')
    all_house = []
    with MysqlTool() as db:
        for house in house_list:
            # 注意独栋公寓的不同
            name = house.xpath('./a/@title')[0]
            href = "https://hz.lianjia.com" + house.xpath('./a/@href')[0]
            img_src = house.xpath('./a/img/@data-src')[0]
            price = house.xpath('./div/span[@class="content__list--item-price"]/em/text()') + house.xpath('./div/span['
                                                                                                          '@class'
                                                                                                          '="content__list'
                                                                                                          '--item-price'
                                                                                                          '"]/text()')
            price = "".join(price)
            place = "-".join(house.xpath('./div/p[@class="content__list--item--des"]/a/text()'))
            if place == "":
                place = name
            info = house.xpath('./div/p[@class="content__list--item--des"]/text()')
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
            tags = house.xpath('./div/p[@class="content__list--item--bottom oneline"]/i/text()')
            tags = ";".join(tags)
            house_data = {
                'name': name,
                'price': price,
                'square': square,
                'place': place,
                'scale': scale,
                'direction': direction,
                'tags': tags,
                'href': href,
                'img_src': img_src,
                'area': area
            }
            print(house_data)
            all_house.append(house_data)
            sql = ("INSERT INTO house_info(name, price, square, place, tag, href, img_src, source, area) VALUES ("
                   "%s, %s, %s, %s, %s, %s, %s, '链家', %s)")
            args = (name, price, square, place, tags, href, img_src, area)
            db.execute(sql, args, commit=True)

    return all_house


def get_5a5j_house(url, area):
    option = webdriver.ChromeOptions()
    # 指定为无界面模式
    option.add_argument('--headless')
    # option.headless=True  或者将上面的语句换成这条亦可
    # 创建Chrome驱动程序的实例
    driver = webdriver.Chrome(options=option)

    driver.get(url)
    time.sleep(3)  # 因为为js渲染的动态网页，所以必须强制等待其加载完毕

    name_list = driver.find_elements_by_xpath('//ul[@class="pList rentList"]//li//div[@class="listCon"]/h3/a')
    name = [p.text for p in name_list][:-1]
    href = [p.get_attribute('href') for p in name_list][:-1]
    img_list = driver.find_elements_by_xpath('//ul[@class="pList rentList"]/li/div[@class="listImg"]/a/img')
    img_src = []
    for p in img_list:
        q = p.get_attribute('src')
        if q is None:
            img_src.append("None")
            print(url)
            print(name)
            continue
        if "5i5j.com" in q or "aihome365.cn" in q:
            img_src.append(q)
        elif "data:image/png" in q:
            img_src.append(p.get_attribute('data-src'))
        else:
            print("爬取图片链接出现未知错误" + p.get_attribute('title'))
    price_list = driver.find_elements_by_xpath('//p[@class="redC"]/strong')
    price = [p.text for p in price_list][:-1]
    place_list = driver.find_elements_by_xpath('//div[@class="listX"]/p[2]')
    place = [p.text for p in place_list][:-1]
    info_list = driver.find_elements_by_xpath('//div[@class="listX"]/p[1]')
    info = [p.text for p in info_list][:-1]
    scale = []
    square = []
    floor = []
    # decorate = []

    for i in info:
        i = i.split('·')
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

    all_house = []
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
                'tag': tags[j],
                'area': area
            }
            print(house_data)
            all_house.append(house_data)
            sql = ("INSERT INTO house_info(name, price, square, place, href, img_src, tag, source, area) VALUES ("
                   "%s, %s, %s, %s, %s, %s, %s, '我爱我家', %s)")
            args = (name[j], price[j] + " 元/月", square[j], place[j], href[j], img_src[j], tags[j], area)
            db.execute(sql, args, commit=True)
    return all_house


def get_ziru_house_new(url, ocr, area):
    options = webdriver.ChromeOptions()
    # 无法使用无头模式，会导致元素缺失
    # options.add_argument('--headless')
    # 添加启动参数 (add_argument)
    options.add_argument("start-maximized")  # 最大化运行（全屏窗口）,不设置的话取元素会报错
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36")
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
    driver.get(url)
    time.sleep(3)  # 因为为js渲染的动态网页，所以必须强制等待其加载完毕
    # 爬取可以简单获取的房屋信息
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
        s_flag = False
        f_flag = False
        d_flag = False

        for s_info in s:
            if '㎡' in s_info:
                square.append(s_info)
                s_flag = True
            elif '层' in s_info:
                floor.append(s_info)
                f_flag = True
            elif '朝' in s_info:
                direction.append(s_info)
                d_flag = True
            else:
                print('-********************')
                print('info出现新的情况' + s)
                print('-********************')

        if not s_flag:
            square.append('None')
        if not f_flag:
            square.append('None')
        if not d_flag:
            square.append('None')

    # 爬取标签，并标准化标签数据
    tags_list = driver.find_elements_by_xpath('//div[@class="info-box"]/div[@class="tag"]')
    tags = []
    for div in tags_list:
        spans = div.find_elements_by_tag_name("span")
        tag = ''
        for span in spans:
            if span.text == '':
                continue
            elif "限时立减" in span.text:
                tag = tag + span.text[0:-2] + ';'
            else:
                tag = tag + span.text + ';'
        tags.append(tag[0:-1])

    # 爬取价格
    price_list = driver.find_elements_by_xpath('//div[@class="price-content"]/div[1]')
    price = []
    for div in price_list:
        spans = div.find_elements_by_class_name('num')
        p = ''
        for span in spans:
            p = p + get_price_by_ocr(span.get_attribute('style'), ocr)
        price.append(p)

    # 爬取房屋图片
    a_list = driver.find_elements_by_xpath('//div[@class="item"]/div[@class="pic-box"]/a[@target="_blank"]')
    img_list = []
    for a in a_list:
        img = a.find_element_by_xpath('./img')
        src = img.get_attribute('src')
        if "imgpro" in src:
            img_list.append(src)
        elif "webimg" in src:
            img_list.append(img.get_attribute('data-original'))
        else:
            print("爬取房屋图片有未知错误")

    all_house = []
    # 房屋信息整合
    with MysqlTool() as db:
        for j in range(len(name)):
            house_data = {
                'name': name[j],
                'price': price[j] + " 元/月",
                'square': square[j],
                'place': place[j],
                'floor': floor[j],
                'direction': direction[j],
                'href': href[j],
                'tags': tags[j],
                'img_src': img_list[j],
                'area': area
            }
            print(house_data)
            all_house.append(house_data)
            sql = ("INSERT INTO house_info(name, price, square, place, tag, href, img_src, source,area) VALUES ("
                   "%s, %s, %s, %s, %s, %s, %s, '自如', %s)")
            args = (name[j], price[j] + " 元/月", square[j], place[j], tags[j], href[j], img_list[j], area)
            db.execute(sql, args, commit=True)
    driver.quit()
    return all_house


if __name__ == '__main__':
    ocr = ddddocr.DdddOcr()  # ocr识别需要开启

    area_ziru = ['北京', '上海', '深圳', '杭州', '南京',
                 '成都', '武汉', '广州', '天津', '苏州']
    dict_ziru = {
        '北京': 'https://www.ziroom.com/z/',
        '上海': 'https://sh.ziroom.com/z/',
        '深圳': 'https://sz.ziroom.com/z/',
        '杭州': 'https://hz.ziroom.com/z/',
        '南京': 'https://nj.ziroom.com/z/',
        '成都': 'https://cd.ziroom.com/z/',
        '武汉': 'https://wh.ziroom.com/z/',
        '广州': 'https://gz.ziroom.com/z/',
        '天津': 'https://tj.ziroom.com/z/',
        '苏州': 'https://su.ziroom.com/z/'
    }

    area_lianjia = ['北京', '上海', '深圳', '杭州', '南京',
                    '成都', '武汉', '广州', '天津', '台州']
    dict_lianjia = {
        '北京': 'https://bj.lianjia.com/zufang/',
        '上海': 'https://sh.lianjia.com/zufang/',
        '深圳': 'https://sz.lianjia.com/zufang/',
        '杭州': 'https://hz.lianjia.com/zufang/',
        '南京': 'https://nj.lianjia.com/zufang/',
        '成都': 'https://cd.lianjia.com/zufang/',
        '武汉': 'https://wh.lianjia.com/zufang/',
        '广州': 'https://gz.lianjia.com/zufang/',
        '天津': 'https://tj.lianjia.com/zufang/',
        '台州': 'https://taizhou.lianjia.com/zufang/'
    }

    area_5ai5jia = ['北京', '上海', '无锡', '杭州', '南京',
                    '成都', '郑州', '常州', '天津', '苏州',
                    '南昌', '太原']
    dict_5ai5jia = {
        '北京': 'https://bj.5i5j.com/zufang/',
        '上海': 'https://sh.5i5j.com/zufang/',
        '无锡': 'https://wx.5i5j.com/zufang/',
        '杭州': 'https://hz.5i5j.com/zufang/',
        '南京': 'https://nj.5i5j.com/zufang/',
        '成都': 'https://cd.5i5j.com/zufang/',
        '郑州': 'https://zz.5i5j.com/zufang/',
        '常州': 'https://cz.5i5j.com/zufang/',
        '天津': 'https://tj.5i5j.com/zufang/',
        '苏州': 'https://sz.5i5j.com/zufang/',
        '南昌': 'https://nc.5i5j.com/zufang/',
        '太原': 'https://ty.5i5j.com/zufang/'
    }

    all_area = ['北京', '上海', '无锡', '杭州', '南京',
                '成都', '郑州', '常州', '天津', '苏州',
                '南昌', '太原', '深圳', '苏州', '台州',
                '广州', '武汉']

    for area in all_area:
        # flag标志是否爬取
        flag1 = False
        flag2 = False
        flag3 = False
        print('爬取区域' + area + '中')
        if area in area_lianjia:
            lianjia = dict_lianjia[area]
            get_lianjia_house(lianjia, area)
            print(area + "链家---第1页爬取完成")
            flag1 = True
        if area in area_5ai5jia:
            wojia = dict_5ai5jia[area]
            get_5a5j_house(wojia, area)
            print(area + "我爱我家---第1页爬取完成")
            flag2 = True
        if area in area_ziru:
            ziru = dict_ziru[area]
            get_ziru_house_new(ziru, ocr, area)
            print(area + "自如---第1页爬取完成")
            flag3 = True

        # 测试单页爬取
        # i = 2
        # new_ziru = ziru + "p" + str(i) + "-q962499368544165889-a962499368544165889/"
        # new_lianjia = lianjia + "pg" + str(i) + "/#contentList"
        # new_wojia = wojia + "n" + str(i) + "/"
        # get_lianjia_house(new_lianjia)
        # print("链家---第" + str(i) + "页爬取完成")
        # get_5a5j_house(new_wojia)
        # print("我爱我家---第" + str(i) + "页爬取完成")
        # get_ziru_house_new(new_ziru, ocr)
        # print("自如---第" + str(i) + "页爬取完成")


        # 测试多页爬取
        for i in range(2, 4):
            if flag1:
                new_lianjia = lianjia + "pg" + str(i) + "/#contentList"
                if get_lianjia_house(new_lianjia, area):
                    print(area + "链家---第" + str(i) + "页爬取完成")
                else:
                    flag1 = False

            if flag2:
                new_wojia = wojia + "n" + str(i) + "/"
                if get_5a5j_house(new_wojia, area):
                    print(area + "我爱我家---第" + str(i) + "页爬取完成")
                else:
                    flag2 = False

            # if flag3:
            #     new_ziru = ziru + "p" + str(i) + "-q961410684041994241-a961410684041994241/"
            #     if get_ziru_house_new(new_ziru, ocr):
            #         print("自如---第" + str(i) + "页爬取完成")
            #     else:
            #         flag3 = False

            if not flag1 and not flag2:
                break

        for i in range(2, 4):
            if flag3:
                new_ziru = ziru + "p" + str(i) + "-q962855554269671425-a962855554269671425/"
                if get_ziru_house_new(new_ziru, ocr, area):
                    print(area + "自如---第" + str(i) + "页爬取完成")
                else:
                    flag3 = False
            else:
                break

#   区域指定杭州的爬取
# if __name__ == '__main__':
#     ocr = ddddocr.DdddOcr()  # ocr识别需要开启
#     ziru = "http://hz.ziroom.com/z/"
#     lianjia = "https://hz.lianjia.com/zufang/"
#     wojia = "https://hz.5i5j.com/zufang/"
#
#     get_lianjia_house(lianjia)
#     print("链家---第1页爬取完成")
#     get_5a5j_house(wojia)
#     print("我爱我家---第1页爬取完成")
#     get_ziru_house_new(ziru, ocr)
#     print("自如---第1页爬取完成")
#
#     # 测试单页爬取
#     # i = 2
#     # new_ziru = ziru + "p" + str(i) + "-q962499368544165889-a962499368544165889/"
#     # new_lianjia = lianjia + "pg" + str(i) + "/#contentList"
#     # new_wojia = wojia + "n" + str(i) + "/"
#     # get_lianjia_house(new_lianjia)
#     # print("链家---第" + str(i) + "页爬取完成")
#     # get_5a5j_house(new_wojia)
#     # print("我爱我家---第" + str(i) + "页爬取完成")
#     # get_ziru_house_new(new_ziru, ocr)
#     # print("自如---第" + str(i) + "页爬取完成")
#
#     # flag标志是否爬取
#     flag1 = True
#     flag2 = True
#     flag3 = True
#     # 测试多页爬取
#     for i in range(2, 6):
#         if flag1:
#             new_lianjia = lianjia + "pg" + str(i) + "/#contentList"
#             if get_lianjia_house(new_lianjia):
#                 print("链家---第" + str(i) + "页爬取完成")
#             else:
#                 flag1 = False
#
#         if flag2:
#             new_wojia = wojia + "n" + str(i) + "/"
#             if get_5a5j_house(new_wojia):
#                 print("我爱我家---第" + str(i) + "页爬取完成")
#             else:
#                 flag2 = False
#
#         # if flag3:
#         #     new_ziru = ziru + "p" + str(i) + "-q961410684041994241-a961410684041994241/"
#         #     if get_ziru_house_new(new_ziru, ocr):
#         #         print("自如---第" + str(i) + "页爬取完成")
#         #     else:
#         #         flag3 = False
#
#         if not flag1 and not flag2:
#             break
#
#     for i in range(2, 6):
#         if flag3:
#             new_ziru = ziru + "p" + str(i) + "-q962855554269671425-a962855554269671425/"
#             if get_ziru_house_new(new_ziru, ocr):
#                 print("自如---第" + str(i) + "页爬取完成")
#             else:
#                 flag3 = False
#         else:
#             break
