# flask web server start
# 프레임워크 호출 
from flask import Flask, render_template, session, request, redirect
import random
from database import MyDB
# 클래스 생성
app = Flask(__name__)

web_db = MyDB(
    host = '172.30.1.60', 
    port = 3306, 
    user = 'ubion', 
    pwd= '1234', 
    db= 'ubion'
)

# 세션을 사용하기위한 secret_key 설정
app.secret_key = 'asdfqwer'


# api 생성하고 함수 생성 (index.html을 render)
@app.route('/')
def index():
    return render_template('index.html')

# /game인 get 방식으로 url을 생성 
@app.route('/game')
def game():
    # 세션에 데이터가 존재한다면?
    # session 데이터 안에 user_nick 키값이 존재하는가?
    if 'user_nick' in session:
        return render_template('game.html', 
                               nick_name = session['user_nick'])
    else:
        # index.html을 이용하여 보낸 데이터를 변수에 저장 
        # get 방식으로 들어온 데이터는 request.args 존재
        try:
            # 정상적으로 작동하는 경우 
            user_nick = request.args['nickname']
            print(f"[get] /game : {user_nick}")
            # 세션에 데이터 저장
            session['user_nick'] = user_nick
            return render_template('game.html', 
                                   nick_name = user_nick)
        except Exception as e:
            print(e)
            # 에러가 발생한다면 첫 페이지로 이동
            return redirect('/')
        
# 비동기 통신으로 데이터를 받는 url 생성 
@app.route('/game_result')
def game_result():
    # data : { 'user' : xxxxx }
    user_select = int(request.args['user'])
    print(f"[get_ajax] /game_result : {user_select}")
    # 1 : 가위, 2 : 바위, 3: 보
    # 서버가 선택을 할 리스트 생성
    _list = [1, 2, 3]
    server_select = random.choice(_list)
    # 유저가 선택한 값과 서버가 선택한 값을 가지고 조건
    if user_select == server_select:
        result = '무승부'
    else:
        if user_select == 1:
            # 유저가 가위를 선택한 경우
            if server_select == 2:
                result = '패배'
            else:
                result = '승리'
        elif user_select == 2:
            if server_select == 1:
                result = '승리'
            else:
                result = '패배'
        else:
            if server_select == 1:
                result = '패배'
            else:
                result = '승리'
    # ajax에서 받는 데이터의 타입을 json을 지정했기 때문에
    return_data = {
        'user' : user_select, 
        'server' : server_select, 
        'result' : result
    }
    print(f"[get_ajax] /game_result : GAME_DATA {return_data}")
    return return_data

# 회원가입 페이지를 보여주는 url 생성
@app.route("/signup")
def signup():
    return render_template('signup.html')

# 아이디 사용 가능 유무를 판단하는 url 생성
@app.route('/check_id', methods=['post'])
def signup2():
    # 비동기 통신으로 들어오는 데이터의 형태{ user_id : xxxxx }
    # post 방식으로 들어오는 데이터는 request.form
    user_id = request.form['user_id']
    print(f"[post] /check_id : {user_id}")
    # DB에 해당하는 아이디가 존재하는가?
    select_query = """
        SELECT * FROM `user_list`
        WHERE `id` = %s
    """
    res_sql = web_db.execute_query(select_query, user_id)
    print(f"[post] /check_id : DBResult {len(res_sql)}")
    # res_sql의 데이터 타입? DataFrame
    # 길이가 0이면 사용 가능  아니면 사용 불가
    if len(res_sql) == 0:
        result = True
    else:
        result = False
    return_data = {
        'check_id' : result
    }
    print(f"[post] /check_id : returndata {return_data}")
    return return_data

# 회원의 정보를 받아와서 DB에 insert하는 url
@app.route('/signup2', methods=['post'])
def signup3():
    # 회원 가입 페이지에서 유저가 입력한 데이터들을 모두 변수에 저장 
    # id, pass1, pass2, name 4개의 부분에서 입력 
    # id, pass1, name 입력 공간에는 name 속성이 존재
    # pass2는 name 속성이 존재하지 않는다(해당하는 데이터는 받을수 없다)
    print(f"[post] /signup2 : {request.form}")
    # request.form -> { 'user_id' : xxxx, 
    #                   'user_pass' : xxxxx, 
    #                   'user_name': xxxx }
    user_id = request.form['user_id']
    user_pass = request.form['user_pass']
    user_name = request.form['user_name']

    # 에러가 발생하는 경우 ( try ... except ...)
    # DB 서버에 insert 작업 
    # insert후 DB 에 commit까지 바로
    # insert 가 정상적으로 작동을 했다면 -> 로그인 페이지('/')로 이동 redirect()
    try: 
        insert_query = """
            INSERT INTO 
            `user_list`
            VALUES (%s, %s, %s)
        """
        web_db.execute_query(insert_query, 
                            user_id, 
                            user_pass, 
                            user_name, 
                            inplace=True)
        return redirect('/')
    # 정상적으로 작동하지 않으면 -> 회원 가입 페이지('/signup')로 이동 
    except Exception as e:
        print(f"[post] /signup2 : ERROR {e}")
        return redirect('/signup')


# 웹 서버 시작
app.run(debug=True)