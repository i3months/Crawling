from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import time
import pyautogui
import os
import urllib.request
import openpyxl

# 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러메세지 없애기 
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬드라이버 매너저를 통해 드라이버를 설치, 서비스를 만들어낸다
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options=chrome_options)

#---- selenium 기본설정 끝----#

keyword = pyautogui.prompt("검색어를 입력해주세요.")

url = f"https://www.youtube.com/results?sp=mAEB&search_query={keyword}"

driver.implicitly_wait(10)
driver.maximize_window()
driver.get(url)

# 무한스크롤 시 끝없이 내려감. 조금만..

scroll_cnt = int(pyautogui.prompt("얼마나 내릴까요?"))

i = 1
while True:
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

    # 로딩시간
    time.sleep(3)
    if i==scroll_cnt:
        break
    i+=1

# selenium은 느림. beautifulsoup + selenium 사용

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

infos = soup.select("div.text-wrapper") # 정보를 가지고있는 박스를 싹다 가져와서 처리

for info in infos:
    title = info.select_one("a#video-title").text

    try:
        views = info.select_one("div#metadata-line > span:nth-child(1)").text
        date = info.select_one("div#metadata-line > span:nth-child(2)").text
    except:
        views = "스트리밍"
        date = "스트리밍"

    print(title,views,date)

