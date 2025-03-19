import pymysql
import pandas as pd

class MyDB:
    # 독립적으로 저장이 되는 변수를 생성 
    # class가 생성되는 과정에서 바로 호출이 되는 함수 : 생성자 함수 
    # 변수 : 서버의 주소, 포트번호, 유저명, 비밀번호, 데이터베이스명
    # 변수들의 기본값을 설정 ( 로컬 피씨씨 ) 
    def __init__(self, 
                 host = "127.0.0.1", 
                 port = 3306, 
                 user = 'root', 
                 pwd = '1234', 
                 db = 'ubion'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
    
    # 서버와 연결하고 커서를 생성하는 함수 
    def connect_sql(self):
        # 서버와 연결 
        self.server = pymysql.connect(
            host = self.host, 
            port = self.port, 
            user = self.user, 
            password = self.pwd, 
            db = self.db
        )
        # 커서를 생성 (독립적)
        self.cursor = self.server.cursor(pymysql.cursors.DictCursor)
    # 서버와 연결을 종료하는 함수 
    def close_sql(self):
        self.server.close()

    # 쿼리문을 실행하는 함수 
    def execute_query(self, sql_query, *values, inplace = False):
        # 서버와 연결
        self.connect_sql()
        # 커서에 sql_query를 보낸다. 
        self.cursor.execute(sql_query, values)
        # sql_query가 select문이라면?
        # if sql_query.upper().lstrip().startswith('SELECT'):
        if sql_query.upper().split()[0] == 'SELECT':
            # 커서에서 데이터를 가져온다. 
            sql_data = self.cursor.fetchall()
            # 데이터프레임으로 변환
            result = pd.DataFrame(sql_data)
        else:
            # insert, update, delete인 경우
            # inplace True인 경우
            if inplace:
                self.server.commit()
            result = "Query OK"
        
        # 서버와의 연결을 종료
        self.close_sql()
        
        return result