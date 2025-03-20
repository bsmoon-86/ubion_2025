# flask web server start
# 프레임워크 호출 
from flask import Flask, render_template

# 클래스 생성
app = Flask(__name__)

# api 생성하고 함수 생성 (index.html을 render)
@app.route('/')
def index():
    return render_template('index.html')

# 웹 서버 시작
app.run(debug=True)