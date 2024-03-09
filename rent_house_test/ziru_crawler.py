import requests
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'
}

url = "http://hz.ziroom.com/z/"

htm = requests.get(url, headers=headers).content.decode('UTF-8')

html = etree.HTML(htm)

house_list = html.xpath('//div[@class="Z_list-box"]//div')
# print(house_list)
# print(house_list[0].xpath('./div[@class="clue-content"]/text()'))
# print(house_list[0].xpath('./div[@class="pic-box"]/a/@href')[0])
house = house_list[0].xpath('./div[@class="pic-box"]/a/@href')[0]
new_url = 'https:' + house

house_htm = requests.get(new_url, headers=headers).content.decode('UTF-8')
house_html = etree.HTML(house_htm)

name = house_html.xpath('/html/body/div[1]/section/aside/h1/text()')[0]
# print(name)
house_info = house_html.xpath('//div[@class="Z_home_b clearfix"]/dl/dd/text()')
square = house_info[0]
direction = house_info[1]
scale = house_info[2]
floor = house_info[3]
content = house_html.xpath('//div[@class="Z_rent_desc"]/text()')[0].replace("\t", "").replace("\n", "")
live_time = house_html.xpath('//li[@class="tip-tempbox"]/span[@class="info_value"]/text()')[0]
time = house_html.xpath('//*[@id="live-tempbox"]/ul/li[2]/span[@class="info_value"]/text()')[0]
# print(content)
# print(time)
# print(live_time)
house_tag = house_html.xpath('/html/body/div[1]/section/aside/div[2]//span/text()')
print(house_tag)



