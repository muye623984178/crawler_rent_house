from lxml import etree

str = '''
<div>
<u1>
<li class="first"><a href="https://www.csdn.net/">CSDN</a></li>
<li class="two"><a href="https://wwwzhihucom/hot">zhihu</a></li>
<li class="three"><a href="https://wmw.runoob.com/linux/linux-tutorial.html" class="linux">linux</a></li>
<li class="four"><a href="https://leetcode-cn.com/">leecode</a></li>
<li class="five"><a href="https://www.facebook.com/">facebook</a></li>
<li class="six"><a href="https://www.bilibili.com/">bilibili</a></li>
</u1>
</div>'''

# 将数据转为标签树的方式
htm = etree.HTML(str)
# print(htm)
# print(etree.tostring(htm).decode('UTF-8'))

li = htm.xpath('//li')
# print(li)

li2 = htm.xpath('//li[@class="two"]')
print(li2[0].xpath('./a/text()'))

li3 = htm.xpath('//li[@class!="first"]')
print(li3)
# print(li3[0].xpath('./a/text()'))

li4 = htm.xpath('//li[contains(@class,"tw")]')
print(li4)
print(li4[0].xpath('./a/@href'))

li5 = htm.xpath('//li/a/@href')
print(li5)

li6 = htm.xpath('//li[not(contains(@class,"tw"))]')
print(li6)
print(etree.tostring(li6[0]))

li7 = htm.xpath('//li[contains(@class,"three") and not(contains(@class,"f"))]')
print(etree.tostring(li7[0]))

li8 = htm.xpath('//li[last()]')
print(li8)

li9 = htm.xpath('//li[position()<3]')
print(li9)

