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

wb = openpyxl.Workbook()
ws = wb.create_sheet('코스피')
ws.append(['종목명', 'per','roe', 'pbr', '유보율'])

lastpage = int(pyautogui.prompt("몇 페이지까지 가져올까요? (1페이지 = 50개)"))

for i in range(1,lastpage+1):
    
    url = f"https://finance.naver.com/sise/field_submit.naver?menu=market_sum&returnUrl=http://finance.naver.com/sise/sise_market_sum.naver?&page={i}&fieldIds=per&fieldIds=roe&fieldIds=pbr&fieldIds=reserve_ratio"

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    trs = soup.select("table.type_2 > tbody >tr[onmouseover]")

    for tr in trs:
        # 클래스 정보가 없을 때 nth-child 사용
        name = tr.select_one('td:nth-child(2)').text
        per = tr.select_one('td:nth-child(7)').text
        roe = tr.select_one('td:nth-child(8)').text
        pbr = tr.select_one('td:nth-child(9)').text
        reserve_ratio = tr.select_one('td:nth-child(10)').text

        # NA이면 가져오지 않음
        if per != 'N/A' and roe != 'N/A' and pbr != 'N/A' and reserve_ratio != 'N/A':
            per = float(per.replace(',', ''))
            roe = float(roe.replace(',', ''))
            pbr = float(pbr.replace(',', ''))
            reserve_ratio = float(reserve_ratio.replace(',', ''))

            print(name, per, roe, pbr, reserve_ratio)
            ws.append([name, per, roe, pbr, reserve_ratio])

wb.save("naverfinancial/코스피분석.xlsx")