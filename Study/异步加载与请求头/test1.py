import json

import requests
import re

url = 'https://exercise.kingname.info/exercise_ajax_2.html'
htm = requests.get(url).content.decode()
json_str = re.search("secret = '(.*?)'", htm, re.S).group(1)
print(json_str)
json_dict = json.loads(json_str)
print(json_dict['code'])
