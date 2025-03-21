# 기본적인 웹 서버 설정 
# flask 웹프레임워크 로드 
from flask import Flask, render_template, request, redirect, url_for
from database import MyDB
import pandas as pd
import os

# Flask class 생성
app = Flask(__name__)

# MyDB Class 생성
web_db = MyDB()

# 127.0.0.1:5000/ url 생성
@app.route('/')
def index():
    return render_template('index.html')

# dashboard를 보여주는 url 생성 
@app.route("/dashboard")
def dashboard():
    # 유저가 보내는 데이터 존재 : ticker 
    # get 방식  : request.args 존재
    ticker = request.args['ticker']
    print(f"[get] /dashboard : {ticker} ")
    # ticker에 따라 다른 csv을 로드 (데이터프레임)
    # csv 파일의 경로 : ./data/filename.csv
    # pythonanywhere에서는 절대 경로 사용
    # /home/user_name/mysite/data/filename.csv
    # df = pd.read_csv(f"./data/{ticker}.csv")
    base_url = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_url, 'data', f"{ticker}.csv")
    df = pd.read_csv(csv_path)
    # 데이터프레임의 하위 50 추출
    df = df.tail(50)
    # Date 컬럼의 데이터를 리스트로 생성 (x축 데이터)
    date_list = df['Date'].to_list()
    # Adj Close 컬럼의 데이터를 리스트로 생성 (y축 데이터)
    close_list = df['Adj Close'].to_list()
    # 거래량 리스트 생성 
    volume_list = df['Volume'].to_list()
    # 전체 데이터프레임을 dict 형태로 변환
    dict_data = df.to_dict(orient='records')
    # dict에서 첫번째 원소의 키값들을 리스트로 생성
    cols_list = list(dict_data[0].keys())
    # dashboard에 date컬럼의 리스트와 Adj Close 리스트, 
    # dict, keys들을 모두 보낸다
    return render_template('dashboard.html', 
                           x_data = date_list, 
                           y_data = close_list, 
                           y1_data = volume_list,
                           table_data = dict_data, 
                           table_cols = cols_list)

# 웹서버 실행 
app.run(debug=True)