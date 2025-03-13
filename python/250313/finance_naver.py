import pandas as pd 
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

# 웹 브라우져 오픈 
driver = webdriver.Chrome()

# base_url 생성
base_url = "https://finance.naver.com"
sub_url = "/item/main.naver?code="
code = input('종목코드를 입력하시오')

# 특정 웹페이지로 이동
driver.get(base_url+sub_url+code)

# 해당 페이지의 html 소스 코드를 파싱
soup = bs(driver.page_source, 'html.parser')

# div 태그중 class가 news_section 태그를 선택 
div_data = soup.find(
    'div', attrs={'class' : 'news_section'}
)

# div_data에서 li 태그를 모두 찾는다. 
li_list = div_data.find_all(
    'li'
)

# li태그 중 첫번째 a태그의 href속성의 값 리스트로 생성
href_list = list(
    map(
        # lambda li_data : li_data.find('a')['href'] 
        lambda li_data : li_data.a['href'], 
        li_list
    )
)

# 뉴스의 기사들은 저장할수 있는 리스트를 생성
result = []

# href_list를 이용하여 반복문을 실행
for href in href_list:
    try :
        # driver 요청
        driver.get(base_url+href)
        # html 소스코드를 파싱 
        news_soup = bs(driver.page_source, 'html.parser')
        # h2태그중 id가 title_area인 태그의 텍스트 추출
        news_title = news_soup.find(
            'h2', attrs={'id':'title_area'}
        ).get_text()
        # div태그 중 id가 newsct_article인 태그의 텍스트를 추출
        news_content = news_soup.find(
            'div', attrs={'id' : 'newsct_article'}
        ).get_text().replace('\n', '').replace('\t', '')
        news_dict = {
            'title' : news_title, 
            'content' : news_content
        }
        # result에 news_dict을 추가
        result.append(news_dict)
    # 예외 구문 
    except:
        continue
# result를 데이터프레임으로 생성
df = pd.DataFrame(result)
# 데이터프레임을 csv파일로 저장 
df.to_csv(f'news_{code}.csv', index=False)