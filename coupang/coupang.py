import requests
from bs4 import BeautifulSoup
import pyautogui
import openpyxl

keyword = pyautogui.prompt("검색어를 입력하세요.")
num = int(pyautogui.prompt("몇 페이지까지 가져올까요?"))

wb = openpyxl.Workbook('coupang/coupang.result.xlsx')
ws = wb.create_sheet(keyword)
ws.append(['순위', '브랜드명', '상품명', '가격', '상세페이지 링크'])

rank = 1

for page in range(1, num + 1):
    # 검색어 
    print(page, "번째 페이지 입니다.")
    main_url = f"https://www.coupang.com/np/search?&q={keyword}&page={page}"

    # 헤더에 User-Agent, Accept-Language 추가해주기.
    header = {
        'Host': 'www.coupang.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    response = requests.get(main_url, headers=header)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.select("a.search-product-link") # 여러개라서 리스트로 반환

    for link in links:

        # 광고 상품 제거
        if len(link.select("span.ad-badge-text")) > 0:
            print("광고 상품 입니다.")
        else:
            sub_url = "https://www.coupang.com/" + link.attrs['href'] # 형식 맞추기 

            response = requests.get(sub_url, headers=header)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            try:
                brand_name = soup.select_one("a.prod-brand-name").text # 상품명은 없을 수도 있다.
            except:
                brand_name = ""
            
            # 상품명
            product_name = soup.select_one("h2.prod-buy-header__title").text

            # 가격
            product_price = soup.select_one("span.total-price > strong").text

            print(rank, brand_name, product_name, product_price)
            ws.append([rank, brand_name, product_name, product_price, sub_url])
            rank += 1

wb.save('coupang_result.xlsx')            