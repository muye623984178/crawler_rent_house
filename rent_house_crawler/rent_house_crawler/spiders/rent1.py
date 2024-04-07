import scrapy


class Rent1Spider(scrapy.Spider):
    name = "rent1"
    allowed_domains = ["hz.ziroom.com"]
    start_urls = ["http://hz.ziroom.com/z/"]
    new_url = "https://hz.ziroom.com/z/p%d-q950791567437910017-a950791567437910017/"

    def parse(self, response, *args, **kwargs):
        # pass
        self.logger.info('Parsing URL: %s', response.url)
        house_list = response.xpath('//div[@class="Z_list-box"]//div')
        # print(house_list)
        house = house_list[0].xpath('./div[@class="pic-box"]/a/@href')[0].extract()
        # print(house)
        new_url = 'https:' + house
        print(new_url)
