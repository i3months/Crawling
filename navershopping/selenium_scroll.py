from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#auto update
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip

# 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 에러메세지 없애기 (불필요)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬드라이버 매너저를 통해 드라이버를 설치, 서비스를 만들어낸다
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options=chrome_options)

# before scroll
before_h = browser.execute_script("return window.scrollY")

# infinite scroll
while True:
    browser.find_element_by