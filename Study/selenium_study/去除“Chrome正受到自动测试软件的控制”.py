from selenium import webdriver
from selenium.webdriver import ActionChains

#####
options = webdriver.ChromeOptions()
# 去除inforbars的具体配置
options.add_experimental_option("excludeSwitches", ['enable-automation'])
#####

driver = webdriver.Chrome(options=options)
driver.get('https://cn.bing.com/?mkh=zh-CN')
driver.find_element_by_xpath('//*[@id="sb_form_q"]').send_keys("川川菜鸟")
b = driver.find_element_by_class_name('search')
ActionChains(driver).click(b).perform()