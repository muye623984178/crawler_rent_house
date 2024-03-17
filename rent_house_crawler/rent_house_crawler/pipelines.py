# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings
import pymysql

class RentHouseCrawlerPipeline:

    def open_spider(self, item):
        print('开始爬取')

    def close_spider(self, item):
        print('爬取结束')

    def process_item(self, item, spider):
        return item


class save_db:
    def __init__(self):
        self.cursor = None
        self.conn = None
        self.charset = None
        self.name = None
        self.password = None
        self.user = None
        self.port = None
        self.host = None

    def open_spider(self, spider):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.password = settings['DB_PASSWROD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']

        self.connect()

        print(self.host)
        print(self.port)
        print(self.user)
        print(self.password)
        print(self.name)
        print(self.charset)

    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.name,
            charset=self.charset
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        sql = 'insert into book(url,`describe`,price,author) values("{}","{}","{}","{}")'.format(item['url'],
                                                                                                 item['describe'],
                                                                                                 item['price'],
                                                                                                 item['author'])
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
