import requests

# url = 'https://exercise.kingname.info/ajax_1_backend'
#
# htm = requests.get(url).content.decode()
#
# print(htm)

url1 = 'https://exercise.kingname.info/ajax_1_postbackend'

htm1 = requests.post(url1, json={'name': '金栩', 'age': 22}).content.decode()

print(htm1)