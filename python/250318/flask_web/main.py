from flask import Flask, render_template, request, redirect
from database import MyDB

# Flask class 생성
# 생성자 함수에는 파일의 이름
app = Flask(__name__)

# DB server에 웹에서 사용할 table이 존재하는가?
# 존재한다면 아무 행동도 하지 않는다. 
# 존재 하지 않는다면 테이블을 생성 
# 유저 테이블 생성 
create_table = """
    CREATE TABLE  
    IF NOT EXISTS
    `user_list`
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

# 로그인 화면에서 id password를 받아주는 주소를 생성 
# /login, post 방식으로 데이터를 보낸다. 
@app.route('/login', methods=['post'])
def login():
    # post 방식으로 보낸 데이터는 request 안에 form에 존재(dict)
    # { 'user_id' : xxxx ,  'user_pass' : xxxx }
    # 유저가 보낸 아이디값을 변수에 저장 
    input_id = request.form['user_id']
    input_pass = request.form['user_pass']
    # 유저가 보낸 데이터를 확인 
    print(f"[post] /login : {input_id}, {input_pass}")

    # 로그인의 로직
    # user_list table에서 
    # 유저가 보낸 id, password를 모두 존재하는 인덱스가 있는가?
    # sql 쿼리문 : select문 
    login_query = """
        SELECT 
        * 
        FROM 
        `user_list`
        WHERE `id` = %s AND `password` = %s
    """
    # execute_query()함수는 select문을 넣었을때 돌려주는 데이터의 타입은?
    # DataFrame -> 데이터프레임의 길이가 0이면 -> 로그인이 실패
    # 길이가 1이라면 -> 로그인이 성공
    res_sql = web_db.execute_query(login_query, input_id, input_pass)
    if len(res_sql):
        # 로그인이 성공했다면 특정 페이지 보여준다.(render_template(파일의 이름))
        # 로그인이 성공했다면 특정 주소로 이동(redirect(주소값))
        # main.html와 같이 로그인을 한 유저의 이름을 보낸다. 
        # res_sql       id    password    name
        #            0 test    1234       kim
        # res_sql에서 이름만 추출한다면? 
        # res_sql.loc[0, 'name'] // res_sql.iloc[0, 2]
        # res_sql['name'][0]
        logined_name = res_sql.loc[0, 'name']
        # return "로그인 성공"
        # render_template(파일의 이름, key = value, key2 = value2, ...)
        return render_template('main.html', name = logined_name)
    else:
        # 로그인이 실패했다면 로그인 페이지로 돌아간다. 
        # 로그인 주소로 이동('/')
        # return "로그인 실패"
        return redirect('/')
    
# 회원 가입 페이지를 보여주는 api 생성
@app.route("/signup")
def signup():
    return render_template('signup.html')

# 실제 회원 데이터를 받아서 DB에 저장하는 api 생성
@app.route('/signup2', methods=['post'])
def signup2():
    # form 태그를 이용해서 유저가 보낸 데이터 존재
    # id, password, name 의 값들을 각각 다른 변수에 저장

    # 변수들 확인 print

    # insert query문 생성

    # try
        # MyDB class에 내장된 함수 execute_query() 함수를 호출 
        # 로그인 페이지로 이동
    # except
        # return을 회원가입이 실패한 경우 
        # 회원가입 페이지로 이동

# 웹서버의 실행 
app.run(debug=True)
