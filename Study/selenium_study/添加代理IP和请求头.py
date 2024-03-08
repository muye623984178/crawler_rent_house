from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
# 去除inforbars的具体配置
options.add_experimental_option("excludeSwitches", ['enable-automation'])

#####
options.add_argument(
    'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"'
)
# options.add_argument(f"--proxy-server=http://223.70.126.84:3128") #添加代理失败！！！
#####

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://cn.bing.com/?mkh=zh-CN')
driver.find_element_by_xpath('//*[@id="sb_form_q"]').send_keys("川川菜鸟")
b = driver.find_element_by_class_name('search')
ActionChains(driver).click(b).perform()