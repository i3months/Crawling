import requests 
from bs4 import BeautifulSoup
import time
import pyautogui

# user input
keyword = pyautogui.prompt("검색어를 입력하세요")
lastpage = int(pyautogui.prompt("몇 페이지까지 가져올까요?"))

page_num = 1
for i in range(1, lastpage * 10, 10):
    print(f"{page_num} 번째 페이지를 가져오고 있습니다.")
    response = requests.get(f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}&start={i}")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.select('div.info_group')

    for article in articles:
        links = article.select("a.info")
        if len(links) >= 2:
            url = links[1].attrs['href']
            response = requests.get(url, headers={'User-agent':'Mozila/5.0'})
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')                    
            content = soup.select_one("#dic_area")
            print(content.text)
            time.sleep(0.3)            
    page_num += 1

