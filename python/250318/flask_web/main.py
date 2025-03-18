from flask import Flask, render_template, request
from database import MyDB

# Flask class 생성
# 생성자 함수에는 파일의 이름
app = Flask(__name__)

# DB server에 웹에서 사용할 table이 존재하는가?
# 존재한다면 아무 행동도 하지 않는다. 
# 존재 하지 않는다면 테이블을 생성 
# 유저 테이블 생성 
create_table = """
    CREATE TABLE `user_list` 
    IF NOT EXIST
    (
        `id` varchar(32) primary key, 
        `password` varchar(64) not null, 
        `name` varchar(32)
    )
"""
# MyDB를 이용하여 서버의 접속하고 쿼리문 보낸다. 
web_db = MyDB()

# create_table 쿼리문을 실행 
web_db.execute_query(create_table)

# 유저와 서버간의 데이터를 주고 받는 부분 생성 
# api 생성

# localhost:5000/ 요청이 들어왔을때
@app.route('/')
def index():
    # 로그인 화면을 보여준다. 
    return render_template('signin.html')






# 웹서버의 실행 
app.run()
