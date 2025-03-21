# 기본적인 웹 서버 설정 
# flask 웹프레임워크 로드 
from flask import Flask, render_template, request, redirect, url_for
from database import MyDB
import pandas as pd

# Flask class 생성
app = Flask(__name__)

# MyDB Class 생성
web_db = MyDB()

# dashboard를 보여주는 url 생성 
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

# 웹서버 실행 
app.run()