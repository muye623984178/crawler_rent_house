# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RentHouseCrawlerPipeline:

    def open_spider(self):
        print('开始爬取')

    def close_spider(self):
        print('爬取结束')
    def process_item(self, item, spider):
        return item
