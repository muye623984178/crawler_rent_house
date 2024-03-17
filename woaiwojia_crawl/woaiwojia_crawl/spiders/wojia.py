import scrapy


class WojiaSpider(scrapy.Spider):
    name = "wojia"
    allowed_domains = ["hz.5i5j.com"]
    start_urls = ["http://hz.5i5j.com/"]

    def parse(self, response):
        name = response.xpath('./div[@class="listCon"]/h3/text()')
        print(name)
        # pass
