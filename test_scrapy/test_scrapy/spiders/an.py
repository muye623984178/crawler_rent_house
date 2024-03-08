import scrapy
from ..items import AnItem


class AnSpider(scrapy.Spider):
    name = 'an'
    allowed_domains = ['pic.netbian.com']


    # # 单面图片下载
    # def parse(self, response):
    #     # pass
    #     # filename = "test.html"
    #     # open(filename, 'wb').write(response.body)
    #     img = response.xpath("//ul[@class = 'clearfix']/li")
    #     # print(img)
    #     # print(type(img))
    #     item = AnItem()
    #
    #     h = 'http://pic.netbian.com'
    #     for i in img:
    #         img = h + i.xpath('a/img/@src').extract_first()
    #         # print(img)
    #         title = i.xpath('a/b/text()').extract_first()
    #         # print(title)
    #         item['title'] = title
    #         item['link'] = img
    #         # print(item)
    #         yield item

    # 多页面图片下载
    global num
    num = int(input("请输入要爬取多少页："))
    page = 2
    # start_urls = ['http://pic.netbian.com/4kfengjing/index.html']
    # new_url = 'http://pic.netbian.com/4kfengjing/index_%d.html'
    # item = AnItem()

    # 多种类下载
    global kind
    kind = input("请输入爬取的种类：")
    start_urls = ['http://pic.netbian.com/4k{}/index.html'.format(kind)]
    new_url = 'http://pic.netbian.com/4k{}/index_%d.html'.format(kind)
    item = AnItem()
    def parse(self, response):
        img = response.xpath("//ul[@class='clearfix']/li")
        qian_zhui = "http://pic.netbian.com"
        item = AnItem()
        for i in img:
            img_src = i.xpath('a/img/@src').extract_first()
            url = qian_zhui + img_src
            title = i.xpath('a/b/text()').extract_first()
            item['title'] = title
            item['link'] = url
            yield item

        for i in range(self.page, num):
            print("-----------" + str(i))

            if self.page == num:
                break
            yield scrapy.Request(url=self.new_url % i, callback=self.parse)
            self.page += 1
