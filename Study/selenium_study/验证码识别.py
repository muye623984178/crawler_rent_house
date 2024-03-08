import ddddocr

ocr = ddddocr.DdddOcr()

with open(r'C:\Users\62398\Pictures\联想截图\1.png', 'rb') as f:
    img = f.read()
res = ocr.classification(img)
print(res)
