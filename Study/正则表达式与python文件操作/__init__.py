#coding : UTF-8
import re
import csv

with open('source.txt', 'r', encoding='UTF-8') as f:
    source = f.read()
    # print(source)
result_list = []
# 获取一个楼层的整体HTML
# print(source)
every_reply = re.findall('"l_post l_post_bright j_l_post clearfix  "(.*?)p_props_tail props_appraise_wrap', source, re.S)
# print(every_reply)

# 从楼层HTML中获取发帖人姓名，内容以及发帖时间
for each in every_reply:
    result = {}
    result['name'] = re.findall('target="_blank">(.*?)</a>', each, re.S)[0]
    result['content'] = re.findall('d_post_content j_d_post_content " style="display:;">                    (.*?)</div><br>', each, re.S)
    result['time'] = re.findall('<span class="tail-info">(.*?)</span>', each, re.S)[2]
    # print(result)
    result_list.append(result)

with open('tieba.csv', 'w', encoding='UTF-8') as f:
    writer = csv.DictWriter(f , fieldnames=['name', 'content', 'time'])
    writer.writeheader()
    print(result_list)
    writer.writerows(result_list)
