from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('https://cn.bing.com/?mkh=zh-CN')
driver.save_screenshot('全屏截图.png')
time.sleep(2)
driver.find_element_by_id('sb_form_q').screenshot('元素截图.png')
time.sleep(2)
driver.quit()