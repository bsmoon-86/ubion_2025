import pandas as pd
import os
# 환율 정보 csv 저장 자동화
file_name = "환율.csv"
# 저장하려고 하는 주소에 file_name이 존재하는가?
header_bool = not os.path.exists(file_name)
# file_name not in os.listdir('./')
df = pd.read_html(
        'https://finance.naver.com/marketindex/exchangeList.naver', 
        encoding='cp949'
    )[0]
df.to_csv(
    file_name, 
    mode='a', 
    index = False, 
    header= header_bool
)
