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

driver.implicitly_wait(5) # 로딩 5초까지는 기다림
driver.maximize_window()

driver.get("https://13months.tistory.com")

# 반복문으로?



# # 아이디
# id = driver.find_element(By.CSS_SELECTOR, "#id")
# id.click()
# # 너무 빨리 치면 봇으로 의심받음.
# #id.send_keys("idinput") 
# pyperclip.copy("id")
# pyautogui.hotkey("ctrl", "v")
# time.sleep(2)

# # 비번
# pw = driver.find_element(By.CSS_SELECTOR, "#pw")
# pw.click()
# pyperclip.copy("password")
# pyautogui.hotkey("ctrl", "v")
# time.sleep(2)

# # 로그인 버튼
# login_btn = driver.find_element(By.CSS_SELECTOR, "#log\.login")
# login_btn.click()