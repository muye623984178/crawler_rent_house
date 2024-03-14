# -*- coding:utf-8 -*-
import requests, re, pickle, sys, json
import urllib3
from bs4 import BeautifulSoup

import pandas as pd

urllib3.disable_warnings()
from pymongo import MongoClient

# mongodb数据库，用于将爬取的租房信息存下来
mongo = MongoClient('localhost', 27017).zufang.ziru
# 全局变量
room_info_list = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Origin': 'http://www.ziroom.com'
}
# requests的会话对象
s = requests.Session()


# 爬取每个小区的租房信息
def spider(info):
    room_info_list = []

    # 当前页
    pg = 1
    # 总的页数
    pages = 1
    url = 'http://www.ziroom.com/map/room/list'
    # 自如将地图划分成一个个矩形的小格子，每个小格式表示一个小区的范围，小格子的区域使用经纬度来表示
    # 提交的参数
    # 通过观察可以发现所有提交的参数中，格子边界距离中心的距离为固定值，这样就比较容易构造参数了
    lat_diff = 0.011443
    lng_diff = 0.025871
    # 这里所有参数值均为字符串
    params = {
        "max_lng": "%.6f" % (info['touch_lng'] + lng_diff),  # 最大经度
        "min_lng": "%.6f" % (info['touch_lng'] - lng_diff),  # 最小经度
        "max_lat": "%.6f" % (info['touch_lat'] + lat_diff),  # 最大纬度
        "min_lat": "%.6f" % (info['touch_lat'] - lat_diff),  # 最小纬度
        "clng": "%.6f" % info['touch_lng'],
        "clat": "%.6f" % info['touch_lat'],
        "zoom": "16",
        "p": "1"
    }

    while pg <= pages:
        params['p'] = str(pg)
        r = s.get(url=url, params=params, headers=headers)
        if r.status_code == 200:
            data = r.json()
            pages = data['data']['pages']

            for item in data['data']['rooms']:
                try:
                    # 将结果存入数据库
                    mongo.update(
                        {"id": item['id']},
                        {
                            '$set': item
                        },
                        upsert=True
                    )
                    # 将结果存储为csv格式
                    item['location'] = item['location'][0]['name']
                    for k, v in item.items():
                        # 将list类型转化为str类型
                        if str(type(v)) == "<class 'list'>":
                            item[k] = str(v)

                        # 将//开关的url转化为http://开头
                        if str(type(v)) == "<class 'str'>" and v.startswith('//'):
                            item[k] = 'http:' + v
                    room_info_list.append(item)
                    print(item['name'])
                except:
                    pass
        print(info['name'], pg, pages)
        pg += 1

    # 将结果导入为csv格式，每个小区一个csv文件，方便筛选
    if room_info_list:
        pickle.dump(room_info_list, open('ziru_result/%s.db' % info['name'], 'wb'))
        df = pd.DataFrame(room_info_list)[['name', 'desc', 'price', 'location', 'detail_url']]
        df.to_excel('ziru_result/%s.xls' % info['name'])


def main():
    # 获取北京所有小区的租房信息,
    url = 'http://www.ziroom.com/map/room/count?min_lng=116.228373&max_lng=116.486653&min_lat=40.019069&max_lat=40.123091&clng=116.357513&clat=40.0711&zoom=14'
    r = s.get(url, headers=headers)

    if r.status_code == 200:
        data = r.json()['data']
        for item in data:
            # 爬取每个小区的租房信息
            print(item)
            spider(item)


main()
