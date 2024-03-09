import scrapy


class Rent1Spider(scrapy.Spider):
    name = "rent1"
    allowed_domains = ["hz.ziroom.com"]
    start_urls = ["http://hz.ziroom.com/z/"]
    new_url = "https://hz.ziroom.com/z/p%d-q950791567437910017-a950791567437910017/"

    def parse(self, response):
        # pass
        house = response.xpath("/html/body/section/div[3]/div[2]/div")

