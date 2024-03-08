import lxml.html
import requests

htm = requests.get('https://baike.baidu.com/item/%E5%91%A8%E6%9D%B0%E4%BC%A6/129156').content.decode('UTF-8')

selector = lxml.html.fromstring(htm)

content = selector.xpath('//dl[@class="basicInfoBlock_Q2ixE left"]')
con = content[0].xpath('string(.)')
print(con)