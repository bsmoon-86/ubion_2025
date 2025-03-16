# flask 프레임워크 로드 
from flask import Flask, render_template, request
import pandas as pd

# class 생성
# Flask class는 파일의 이름을 인자값으로 대입
# 현재 파일의 이름은 __name__
app = Flask(__name__)

# api 생성
# base_url -> localhost // 127.0.0.1
# port : 8080
# 웹서버 접속시 -> localhost:8080

# 누군가가 내 웹 서버에 요청을 보낸다. 
# localhost:8080
@app.route('/')
def index():
    # index()함수는 localhost:8080/ 요청이 왔을때 호출
    # 문자열 되돌려줄 때
    # return "<h1>Hello</h1>"
    # html 문서를 되돌려줄 때
    # render_template()함수는 기본 경로가 현재 작업 공간에서 
    # 하위 폴더인 templates로 구성
    return render_template('index.html')

# /second 주소로 요청이 들어왔을때
# second.html을 되돌려준다. 
# second 페이지에서는 메인 화면으로 돌아가는 
# 하이퍼링크 하나 생성


# 127.0.0.1:5000/second 주소로 요청을 보냈을때
@app.route('/second')
def second():
    # return "<i>second Page</i>"
    return render_template('second.html')

# index page에서 보낸 데이터를 받는 주소
# get방식으로 데이터를 받는 주소
@app.route('/login')
def get_login():
    # request 메시지 확인 -> flask에 request 로드 
    # request 안에 key가 args 되어있는 value을 확인 
    print(request.args)
    # 로그인 성공하는 조건?
    # 유저가 입력한 아이디의 값이 'test'
    # 유저가 입력한 패스워드의 값이 'asdf1234'
    # 모두 만족을 할 때 로그인이 성공
    # 둘 중 하나라도 만족을 못하면 로그인이 실패
    # request는 데이터의 타입이? dict -> {'input_id':'test', 'input_pass' :'asdf1234'}
    if request.args['input_id'] == 'test' and\
          request.args['input_pass'] == 'asdf1234':
        return "로그인 성공"
    else:
        return "로그인 실패"
    # return 'login test'

# post 방식으로 데이터를 보내는 주소를 생성 
# /login_post -> [post]
@app.route('/login_post', methods=['post'])
def login_post():
    # post 방식으로 보낸 데이터는 request 안에 form에 존재
    print(f" POST 방식의 데이터 : {request.form} ")
    # 유저가 보낸 아이디와 패스워드를 user_info.csv 파일에서 
    # 해당하는 데이터가 존재하는가?
    # user_info.csv 파일을 로드
    post_id = request.form['post_id']
    post_pass = request.form['post_pass'] 
    user = pd.read_csv('user_info.csv')
    # loc를 이용하여 인덱스의 조건식
    # 조건식 -> user['id'] == post_id
    #           user['pass'] == post_pass
    # 두 개의 조건식을 모두 만족하는 데이터프레임의 길이
    flag = user['id'] == post_id
    flag2 = user['pass'] == int(post_pass)
    print(f" user 데이터프레임 결과 : {user.loc[flag & flag2]}")
    if len(user.loc[flag & flag2]):
        # user 데이터프레임에서 id, pass가 모두 일치하는 name 값을 변수에 저장
        user_name = user.loc[flag & flag2, 'name'].iloc[0]
        print(f" 유저의 이름은 {user_name}")
        # return "로그인 성공"
        return render_template('main.html', user = user_name)
    else:
        return "로그인 실패"
    # login_check = False
    # for i in range(len(user)):
    #     # i는 0, 1, 2, 3, .... 위치 값
    #     if list(user.iloc[i].values ) == [post_id, int(post_pass)]:
    #         # 특정 변수의 데이터를 True
    #         login_check = True
    # if login_check:

    #     return "로그인 성공"
    # else:
    #     return "로그인 실패"
    # return "test"


# 웹 서버 오픈 
# host 매개변수 : 접속할 수 있는 아이피의 목록 
# port 매개변수 : 해당하는 주소의 포트 번호
# debug 매개변수 : 디버그 오픈 여부(기본값이 False)
app.run(debug=True)



# 유저와 서버간의 데이터의 이동 
# 유저가 서버에게 데이터를 보내는 경우 
    # html문서 안에 유저가 입력할 수 있는 공간은 생성
        # input 태그를 이용
    # 데이터를 보내는 방법 
        # form 태그를 이용
            # 어느 주소로 보낼것인가? (action) 
            # 어떤 방법으로 보낼것인가? (method)
                # get
                    # url 뒤에 ?를 붙이고 key = value 형태로 데이터를 전송
                    # 데이터 노출로 인한 보상은 문제가 발생할 수 있음
                    # url는 최대 255자 까지만 제한
                    # 보안적으로 노출이 되면 안되는 데이터나 굉장히 긴 데이터는 전송이 불가능
                    # request 메시지 안에 args 키 값에 데이터가 dict형태로 존재
                # post
                    # request 데이터에서 body 부분에 데이터를 담아서 보낸다. 
                    # 데이터 노출이 없고 길이의 제한이 존재하지 않는다. 
                    # get 방식에 비해 상대적으로 느리다
                    # request 메시지 안에 form 키 값에 데이터가 dict 형태로 존재

# 서버가 유저에게 데이터를 보내는 경우 
    # html 문서를 제외한 다른 특정 데이터를 보낸다. 
    # html과 특정 데이터를 묶여서 하나의 html로 만든다. 
    # render_template(파일의 이름, html에서 사용할 변수명 = 데이터)
        # html문서를 불러온다. (한줄씩 확인)
        # 한줄 씩 체크하는 중 {% %} 부분을 확인
        # {% python code %} python code로 변환
        # 변수는 그냥 변수의 값으로 되돌려준다. 
        # if나 for의 경우에는 들여쓰기가 html은 인식 불가 
        # 끝나는 부분은 작성 {%endif%} {%endfor%}
        # 전체 데이터를 문자열로 변경하여 유저에게 되돌려주는 형태