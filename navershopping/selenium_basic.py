from selenium import webdriver
import time

# create browser
browser = webdriver.Chrome('C:/chromedriver.exe')

# open website  
browser.get("https://www.naver.com")

# wait while browser loading
browser.implicitly_wait(10)

# shopping menu click
browser.find_element('a.nav.shop').click()
time.sleep(2)

# search click
search = browser.find_element('')


