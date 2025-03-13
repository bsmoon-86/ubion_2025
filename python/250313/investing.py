import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 웹 브라우져 오픈 
driver = webdriver.Chrome()

driver.get('https://kr.investing.com/economic-calendar/')
# 로그인 팝업 제거
try:
    driver.find_element(By.CLASS_NAME, 'popupCloseIcon ').click()
except:
    print('로그인 팝업 에러')

# 해당 페이지의 html을 파싱 
soup = bs(driver.page_source, 'html.parser')

# table 태그중 id가 economicCalendarData 인 태그를 추출 
table_data = soup.find(
    'table', 
    attrs={
        'id' : 'economicCalendarData'
    }
)

# table_data에서 태그 tbody
tbody_data = table_data.tbody

td_list = tbody_data.find_all(
    'td', 
    attrs={
        'class' : 'event'
    }
)

# td_list에서 각 td_data의 
# 첫번째 a태그를 추출하여 href 속성의 값을 리스트로 생성
link_list = list(
    map(
        lambda td_data : td_data.a['href'], 
        td_list
    )
)

base_url = "https://kr.investing.com/"

i=0
for link in link_list:
    try:
        driver.get(base_url+link)
        time.sleep(10)
        # driver의 html 파싱 
        soup2 = bs(driver.page_source, 'html.parser')
        # section 태그에서 id 가 'leftColumn'태그를 추출
        section_data = soup2.find(
            'section', 
            attrs={
                'id' : 'leftColumn'
            }
        )
        file_name = section_data.h1.get_text().strip()
        # div 태그 중 id가 'eventTabDiv_history_0'태그를 추출 
        div_data = soup2.find(
            'div', 
            attrs={
                'id' : 'eventTabDiv_history_0'
            }
        )
        # div_data을 문자열로 변경 -> pandas에 내장된 read_html함수를 호출
        df = pd.read_html(
            str(div_data)
        )[0]
        # 데이터프레임을 파일로 저장 
        df.to_csv(f"{file_name[:10]}.csv", index=False)
        print(f"{file_name} 파일 생성")
        if i ==2:
            break
        i+=1
    except:
        continue

driver.close()
