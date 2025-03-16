import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver

url = "https://comp.wisereport.co.kr/company/c1010001.aspx?cmp_cd="

# input()함수를 이용하여 종목 코드 받는다. 
code = []
# 반복문을 이용하여 종목 코드를 여러개 받는다. 
while True:
    input_data = input('종목 코드를 입력하시오 : ')    # input_data가 빈 문자열이면? input_data == ''
    # input_data의 길이가 0이라면? len(input_data) == 0
    if input_data == '':
        break
    # input_data의 길이가 6이 아니라면 반복문으로 되돌아간다. 
    if len(input_data) != 6:
        print('종목 코드는 6자리 입니다.')
        continue

    # input_data code에 추가 
    code.append(input_data)

# 웹 브라우져를 오픈 
driver = webdriver.Chrome()

# code를 기준으로 반복을 생성
for c in code:
    # 웹드라이버를 이용하여 특정 페이지 오픈 
    driver.get(url+c)
    # 딜레이
    time.sleep(3)
    # 웹 페이지의 html를 데이터 파싱 
    soup = bs(driver.page_source, 'html.parser')
    try:
        table_data = soup.find_all(
            'table', 
            attrs = {
                'class' : 'gHead01 all-width'
            }
        )[-1]
        df = pd.read_html(
            str(table_data)
        )[0]
        # 파일의 이름 : 종목코드 + report + 현재시간 .csv
        time_data = datetime.now().strftime('%Y-%m-%d')
        df.to_csv(f"{c} report {time_data}.csv", index=False)
        print(f"{c} report {time_data}.csv 파일이 생성")
    except Exception as e :
        print(e)
        print(f'{c} : 에러 발생')
        continue
# 웹 브라우져 종료
driver.close()