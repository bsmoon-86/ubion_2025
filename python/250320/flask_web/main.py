# flask web server start
# 프레임워크 호출 
from flask import Flask, render_template, session, request, redirect

# 클래스 생성
app = Flask(__name__)

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
# 웹 서버 시작
app.run(debug=True)