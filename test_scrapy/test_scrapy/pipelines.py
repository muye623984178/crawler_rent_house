# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os.path
import urllib.request

import requests
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TestScrapyPipeline:

    # def __init__(self):
    #     self.f = open('item.json', 'w', encoding='utf-8')

    def open_spider(self, item):
        print('开始爬取...')

    def process_item(self, item, spider):
        # print(item)
        # self.f.write(json.dumps(dict(item), ensure_ascii=False)+'\n')
        # # ensure_ascii=False 防止中文乱码
        # return item
        title = item['title']
        url = item['link']
        suffix = os.path.splitext(url)[-1]
        # print(suffix)
        urllib.request.urlretrieve(url, filename="photo/%s%s" % (title, suffix))
        print('图片---%s---保存成功' % title)
        return item

    def close_spider(self, item):
        print('爬取结束...')
