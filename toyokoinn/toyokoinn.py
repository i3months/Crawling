from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import requests
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

url = "https://www.toyoko-inn.com/korea/search"


# payload에 있는 헤더 정보로 post 요청을 진행해야 정보를 받아올 수 있다.

data_obj = {
    "lcl_id": "ko",
    "prcssng_dvsn": "dtl",    
    "sel_area_txt": "한국",
    "sel_htl_txt": "토요코인 서울강남",
    "chck_in": "2022/09/26",
    "inn_date": "1",
    "sel_area": "8",
    "sel_htl": "00282",
    "rsrv_num": "1",
    "sel_ldgngPpl": "1"
}

response = requests.post(url, data = data_obj)
html = response.text
soup = BeautifulSoup(html, html.parser)
beds = soup.select("ul.btnLink03")

for bed in beds:
    links = bed.select('a')
    if len(links) > 0:
        print("빈 방 있음")
        




