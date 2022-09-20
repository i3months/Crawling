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

#---- selenium 기본설정 끝----#

keyword = pyautogui.prompt("이미지를 가져올 검색어를 입력하세요.")

if not os.path.exists(f"imagecrawling/{keyword}"):
    os.mkdir(f"imagecrawling/{keyword}")

url = f"https://www.google.com/search?q={keyword}&sxsrf=ALiCzsZoREwf1RYipnTo3vBUVmroeABBfg:1663652357625&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjVgbn-06L6AhUNO3AKHRtcAKIQ_AUoAXoECAIQAw&biw=1280&bih=569&dpr=1.5"
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
    
# 썸네일 이미지 태그 
images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")

for i, image in enumerate(images, 1):
    # 썸네일 클릭해서 저장
    # 클릭 시 셀레니움 대신 자바스크립트 활용 
    driver.execute_script("arguments[0].click()", image)
    time.sleep(1)

    # 큰 이미지 사용하기 base64 사용 x
    if i == 1:
        target = driver.find_elements(By.CSS_SELECTOR, "img.n3VNCb")[0]
    else:
        target = driver.find_elements(By.CSS_SELECTOR, "img.n3VNCb")[1]
     
    img_src = target.get_attribute("src")

    # Forbidden 에러 해결 (사람이 하는거로 인식하도록)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozila/5.0')]
    urllib.request.install_opener(opener)
    
    print(i,img_src)    

    # urllib.error.URLError: <urlopen error [SSL: WRONG_SIGNATURE_TYPE] wrong signature type (_ssl.c:997)
    # 위의 오류는 크롤링 방지 문구이다. try - except로 처리해주자.

    try:
        urllib.request.urlretrieve(img_src, f'imagecrawling/{keyword}/{i}.png')
    except:
        pass