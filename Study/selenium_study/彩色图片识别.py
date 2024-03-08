import ddddocr
import requests
from PIL import Image
import logging  # 忽略警告

logging.captureWarnings(True)

url = 'https://so.gushiwen.org/RandCode.ashx'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'
}
response = requests.get(url, headers=headers, verify=False)
with open('./test.png', 'wb') as f:
    f.write(response.content)


# 对色彩进行处理：
def covert_image(path):
    img = Image.open(path)
    img = img.convert('L')
    data = img.load()
    w, h = img.size
    # 对于黑白照片，黑像素值是0，白像素值为255
    for i in range(w):
        for j in range(h):
            if data[i, j] > 135:
                data[i, j] = 255
            else:
                data[i, j] = 0
    img.save('clean.jpg')


def get_yanzheng(path):
    ocr = ddddocr.DdddOcr()
    with open(path, 'rb') as f:
        img = f.read()
    res = ocr.classification(img)
    return res


covert_image('test.png')

print(get_yanzheng('clean.jpg'))
