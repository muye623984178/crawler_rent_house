import requests
import lxml.html
import csv

# 对比第一块与第二块的演唱会同一内容可得决定第几块的xpath
# /html/body/div[2]/div[2]/div[1]/div[3]/div[1]/div/div[1]/div/div[2]
# /html/body/div[2]/div[2]/div[1]/div[3]/div[1]/div/div[2]/div/div[2]

# 1.获取网页HTML
htm = requests.get('https://search.damai.cn/search.htm?spm=a2oeg.home.top.dcategory.411623e1wtj02o&order=1').content.decode('UTF-8')
print(htm)

# 2.定位需要获取的元素（通过xpath）
selector = lxml.html.fromstring(htm)
content = selector.xpath('//div[@class="items__txt__title"]/span/text()')
print(content)
