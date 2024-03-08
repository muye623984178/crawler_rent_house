import ddddocr

def get_yanzheng(path):
    ocr = ddddocr.DdddOcr()
    with open(path, 'rb') as f:
        img = f.read()
    res = ocr.classification(img)
    return res