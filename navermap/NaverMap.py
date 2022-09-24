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

url = "https://map.naver.com/v5/"

driver.implicitly_wait(10)
driver.maximize_window()
driver.get(url)

keyword = pyautogui.prompt("검색어를 입력해주세요.")

wb = openpyxl.Workbook()
ws = wb.create_sheet(keyword)
ws.append(["순위", "이름", "별점", "방문자리뷰", "블로그리뷰"])

# 검색창
search = driver.find_element(By.CSS_SELECTOR, "input.input_search")
search.click()
time.sleep(2)
search.send_keys(f"{keyword}")
time.sleep(2)
search.send_keys(Keys.ENTER)
time.sleep(2)

# iframe 내부로 들어가기
driver.switch_to.frame("searchIframe") # 나오려면 switch_to_default_content

# iframe 내부 클릭해주기 (눌러도 문제 없는 부분)
driver.find_element(By.CSS_SELECTOR, "li.UEzoS.rTjJo.cZnHG").click()

# 로딩된 데이터 개수 확인
lis = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS")
before_len = len(lis)

# 무한스크롤

while True:
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END) # 아무 태그나 선택 body
    
    time.sleep(2)
    lis = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS")
    after_len = len(lis)
    
    if before_len == after_len:
        break
    else:
        before_len = after_len

driver.implicitly_wait(0)

rank = 1

for li in lis:

    # 광고는 제거해줌
    if len(li.find_elements(By.CSS_SELECTOR, "svg.dPXjn")) == 0:        
        
        # 별점이 있는거만 가져옴
        # if len(driver.find_elements(By.CSS_SELECTOR, "span.h69bs.a2RFq > em")) > 0:
        if len(li.find_elements(By.CSS_SELECTOR, "span.h69bs.a2RFq > em")) > 0:
            name = li.find_element(By.CSS_SELECTOR, "span.TYaxT").text
            star = li.find_element(By.CSS_SELECTOR, "span.h69bs.a2RFq > em").text
            
            # 영업 관련 정보가 있으면 
            if len(li.find_elements(By.CSS_SELECTOR, "span.h69bs.KvAhC")) > 0:
                try:
                    visit_review = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(3)").text
                except:
                    visit_review = 0
                try:
                    blog_review = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(4)").text
                except:
                    blog_review = 0
            else:
                try:                
                    visit_review = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(2)").text
                except:
                    visit_review = 0
                try:
                    blog_review = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(3)").text
                except:
                    blog_review = 0

            visit_review = visit_review.replace("방문자리뷰 ", "").replace(",", "")
            blog_review = blog_review.replace("블로그리뷰 ", "").replace(",", "")
            
            print(rank, name, star, visit_review, blog_review)
            ws.append([rank, name, float(star), int(visit_review), int(blog_review)])
            rank += 1

wb.save(f"navermap/{keyword}.xlsx")                        
            
