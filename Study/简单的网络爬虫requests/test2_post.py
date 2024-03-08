import re
import requests

data1 = {
    'name' : 'jinxu',
    'password' : '123456'
}

# 现在使用的是GET方式访问这个页面，请改用POST方式重新访问
html = requests.get('http://exercise.kingname.info/exercise_requests_post').content.decode('UTF-8')
print(html)

# 现在使用的是POST方式访问本页，通过Formdata提交数据，
html_data = requests.post('http://exercise.kingname.info/exercise_requests_post', data=data1).content.decode('UTF-8')
print(html_data)

# 现在使用的是POST方式访问本页，通过JSON提交数据，
html_json = requests.post('http://exercise.kingname.info/exercise_requests_post', json=data1).content.decode('UTF-8')
print(html_json)