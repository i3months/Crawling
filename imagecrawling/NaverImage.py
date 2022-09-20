from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import os
import urllib.request

# 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러메세지 없애기 
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬드라이버 매너저를 통해 드라이버를 설치, 서비스를 만들어낸다
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options=chrome_options)

keyword = pyautogui.prompt("이미지를 가져올 검색어를 입력하세요.")

if not os.path.exists(f"imagecrawling/{keyword}"):
    os.mkdir(f"imagecrawling/{keyword}")

url = f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={keyword}"
driver.implicitly_wait(10)
driver.maximize_window()
driver.get(url)

before_h = driver.execute_script("return window.scrollY")

while True:    
    # 아래로 내리기
    driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)

    # 로딩 시간 주기
    time.sleep(1)
    
    # 스크롤 후 높이
    after_h = driver.execute_script("return window.scrollY")
    
    if(after_h == before_h):
        break
    before_h = after_h
    
# 이미지 태그 
images = driver.find_elements(By.CSS_SELECTOR, "._image._listImage")

for i, image in enumerate(images, 1):
    # 이미지 태그 주소 가져오기
    img_src = image.get_attribute("src")
    print(i,img_src)    
    urllib.request.urlretrieve(img_src, f'imagecrawling/{keyword}/{i}.png')