import re

import requests

html = requests.get('http://exercise.kingname.info/exercise_requests_get.html')
html_content = html.content.decode('UTF-8')
# print(html_content)

title = re.findall('title>(.*?)</title>', html_content, re.S)[0]
print("页面标题为：" + title)
txt_list = re.findall('<p>(.*?)</p>', html_content, re.S)
txt = '\n'.join(txt_list)
print("页面内容为：" + txt)
