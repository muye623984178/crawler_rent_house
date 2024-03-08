import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException



driver = webdriver.Chrome()
driver.get('https://www.bilibili.com/')
# flag = True
# while flag:
#     try:
#         driver.find_element_by_class_name('bili-avatar-img')
#         flag = False
#         print("已登录，现在为你保存cookie")
#     except NoSuchElementException as e:
#         time.sleep(3)
#     print(driver.get_cookies())
#     driver.close()
# try:
#     driver.find_element_by_class_name('header-login-entry')
#     flag = False
#     print("已登录，现在为你保存cookie")
# except NoSuchElementException as e:
#     time.sleep(3)
# print(driver.get_cookies())

cookies = [{'domain': '.bilibili.com', 'expiry': 1744009140, 'httpOnly': False, 'name': 'buvid4', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'BD409FBB-A0DE-96E8-089B-72041CF178CD39178-024030306-jO0YxpqE%2BuPY%2F%2BhVPOmdjA%3D%3D'}, {'domain': '.bilibili.com', 'expiry': 1740985140, 'httpOnly': False, 'name': 'browser_resolution', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1036-662'}, {'domain': '.bilibili.com', 'expiry': 1740985139, 'httpOnly': False, 'name': 'header_theme_version', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'undefined'}, {'domain': '.bilibili.com', 'expiry': 1740985140, 'httpOnly': False, 'name': 'home_feed_column', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '4'}, {'domain': '.bilibili.com', 'expiry': 1740985139, 'httpOnly': False, 'name': 'enable_web_push', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'DISABLE'}, {'domain': '.bilibili.com', 'expiry': 1740985139, 'httpOnly': False, 'name': '_uuid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'EE6108AE8-7A5A-6B56-37E7-76AD32E9565539232infoc'}, {'domain': '.bilibili.com', 'expiry': 1740985138, 'httpOnly': False, 'name': 'i-wanna-go-back', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '-1'}, {'domain': '.bilibili.com', 'httpOnly': False, 'name': 'b_lsid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '10EBE6BDB_18E031BD408'}, {'domain': '.bilibili.com', 'expiry': 1740985138, 'httpOnly': False, 'name': 'buvid3', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '634EF569-A05D-5C88-49E4-D525DC8EAC7238137infoc'}, {'domain': '.bilibili.com', 'expiry': 1740985138, 'httpOnly': False, 'name': 'b_ut', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '7'}, {'domain': '.bilibili.com', 'expiry': 1740985139, 'httpOnly': False, 'name': 'FEED_LIVE_VERSION', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'V8'}, {'domain': '.bilibili.com', 'expiry': 1744009139, 'httpOnly': False, 'name': 'buvid_fp', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'd8e854693435c030953929ecfbd0fc02'}, {'domain': '.bilibili.com', 'expiry': 1740985138, 'httpOnly': False, 'name': 'b_nut', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1709449138'}]

for cookie in cookies:
    driver.add_cookie(cookie)
