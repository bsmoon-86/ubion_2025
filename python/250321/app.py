# 기본적인 웹 서버 설정 
# flask 웹프레임워크 로드 
from flask import Flask, render_template, request, redirect, url_for
from database import MyDB
import pandas as pd

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
    # ticker에 따라 다른 csv을 로드 (데이터프레임)
    # 데이터프레임의 하위 50 추출
    # Date 컬럼의 데이터를 리스트로 생성 (x축 데이터)
    # Adj Close 컬럼의 데이터를 리스트로 생성 (y축 데이터)
    # 전체 데이터프레임을 dict 형태로 변환
    # dict에서 첫번째 원소의 키값들을 리스트로 생성
    # dashboard에 date컬럼의 리스트와 Adj Close 리스트, 
    # dict, keys들을 모두 보낸다
    return render_template('dashboard.html')

# 웹서버 실행 
app.run()