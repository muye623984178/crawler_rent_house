from selenium import webdriver
import os
import time

driver = webdriver.Chrome()
file_path = 'file:///' + os.path.abspath('../../前端/upload.html')
driver.get(file_path)
driver.find_element_by_id('up_load').send_keys(r"C:\Users\62398\Pictures\联想截图\屏幕截图 2023-07-19 103755.jpg")
# 不能省略r,r将转义字符视为普通字符
time.sleep(2)
driver.quit()
