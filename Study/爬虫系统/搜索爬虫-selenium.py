from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
driver.get('https://cn.bing.com/?mkt=zh-CN')
driver.find_element_by_id('sb_form_q').send_keys('川川菜鸟')
b = driver.find_element_by_class_name('search')

# 单击按钮
ActionChains(driver).click(b).perform()

