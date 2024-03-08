import requests
import re

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'}

url = 'https://httpbin.org/post'

data = {
    'name': 'jinxu',
    'age': 22
}

files = {
    'file': open('test.txt', 'rb')
}
htm = requests.post(url, headers=headers,files = files).content.decode('UTF-8')

print(htm)
