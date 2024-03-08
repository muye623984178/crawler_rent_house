from lxml import etree

str = '''<place>
<name>zhangsan</name>
<plan name="北京" type="first"/>
<plan name="上海" type="second"/>
</place>'''

# 标准化
xml = etree.XML(str)
# print(xml)

# 绝对路径
res1 = xml.xpath('/place/*[@name]')
print(res1)

# 相对路径
res2 = xml.xpath('//*[@name]')
print(res2)

res3 = xml.xpath('/place/*[contains(@name, "北")]')
print(res3)

res5 = xml.xpath('/place/plan/@name/')
print(res5)

res6 = xml.xpath('.')
print(res6)