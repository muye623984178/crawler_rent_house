from selenium import webdriver

driver = webdriver.Chrome()

driver.maximize_window()

driver.get('https://www.taobao.com')

# href = driver.find_element_by_link_text('女装')
# print(href)

# driver.find_element_by_tag_name('input').send_keys('女装')


