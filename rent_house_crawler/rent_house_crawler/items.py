# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RentHouseCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    house_name = scrapy.Field       # 房屋名称
    house_location = scrapy.Field   # 房屋地址
    house_floor = scrapy.Field      # 房屋层数
    house_square = scrapy.Field     # 房屋面积
    house_direction = scrapy.Field  # 房屋朝向
    house_price = scrapy.Field      # 房屋价格
    house_character = scrapy.Field  # 房屋特点
    house_source = scrapy.Field     # 房屋来源
    rent_time = scrapy.Field        # 签约时长
    house_url = scrapy.Field        # 房屋链接
    house_content = scrapy.Field    # 房屋简介
    house_scale = scrapy.Field      # 房屋户型
    house_live_time = scrapy.Field  # 可入住时间
