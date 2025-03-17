import pandas as pd 
import numpy as np
from datetime import datetime

def create_YM(
        _df, 
        _col = 'Adj Close'
):
    df = _df.copy()
    # Date가 컬럼에 포함되어있는가?
    if 'Date' in df.columns:
        # 포함되어있다면 Date를 인덱스로 변환 
        df.set_index('Date', inplace=True)
    # 인덱스를 시계열데이터로 변경
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    # 결측치, 무한대 데이터를 제거 기준이되는 컬럼만 두고 나머지 모두 제거 
    flag = df.isin([np.nan, np.inf, -np.inf]).any(axis=1)
    df = df.loc[~flag, [_col]]
    # 파생변수 STD-YM 생성
    df['STD-YM'] = df.index.strftime('%Y-%m')

    return df

def create_month(
        _df, 
        _start = "2010-01-01", 
        _end = datetime.now(), 
        _momentum = 12, 
        _select = 1
):
    if _select == 1:
        # 월말의 데이터들을 새로운 데이터프레임으로 생성 
        # 현재 행의 년-월과 다음 행의 년-월이 다른 경우 
        flag = _df['STD-YM'] != _df.shift(-1)['STD-YM']
        # df = _df.loc[flag,]
    elif _select == 0:
        flag = _df['STD-YM'] != _df.shift()['STD-YM']
        # df = _df.loc[flag,]
    else :
        return "_select 인자는 0과 1이 가능하다"
    col = _df.columns[0]
    df = _df.loc[flag,]
    df['BF1'] = df.shift()[col].fillna(0)
    df['BF2'] = df.shift(_momentum)[col].fillna(0)
    # 시작시간과 종료 시간은 시계열로 변경 
    try:
            if type(_start) == 'str':
                start = datetime.strptime(_start, '%Y-%m-%d')
            else:
                start = _start
            if type(_end) == "str":
                    end = datetime.strptime(_end, '%Y-%m-%d')
            else:
                    end = _end
    except:
            return "인자값의 타입이 잘못되었습니다.(예 : YYYY-mm-dd)"
    df = df.loc[start:end,]
    return df

def create_rtn(_df1, _df2, _score = 1):
    # _df1에 파생변수 2개 생성 
    _df1['trade'] = ""
    _df1['rtn'] = 1

    # _df2 데이터를 이용하여 momentum_index를 계산하고 거래 내역 추가 
    for i in _df2.index:
        signal = ""

        # 절대 모멘텀 계산
        momentum_index = _df2.loc[i, 'BF1'] / _df2.loc[i, 'BF2'] - _score

        # 모멘텀 인덱스가 무한대가 아니고 0보다 큰 경우 
        flag = (momentum_index > 0) & (momentum_index != np.inf)

        if flag:
            signal = 'buy'
        
        _df1.loc[i:, 'trade'] = signal
        # print(f"날짜 : {i}, 모멘텀 인덱스 : {momentum_index}, flag : {flag}, signal : {signal}")
    # 수익율 계산
    col = _df1.columns[0]

    for i in _df1.index:
        # 구매한 날의 조건식 (전날의 trade가 "" 오늘의 trade가 "buy")
        if (_df1.shift().loc[i, 'trade'] == "") & (_df1.loc[i, 'trade'] == "buy"):
            buy = _df1.loc[i, col]
            print(f"매수일 : {i}, 매수가 : {buy}")
        # 판매한 날의 조건식 (전날의 trade가 "buy" 오늘의 trade가 "")
        elif (_df1.shift().loc[i, 'trade'] == "buy") & (_df1.loc[i, 'trade'] == ""):
            sell = _df1.loc[i, col]
            rtn = sell / buy
            _df1.loc[i, 'rtn'] = rtn
            # print(f"매도일 : {i}, 매도가 : {sell}, 수익율 : {rtn}")
    # 누적수익율 계산
    _df1['acc_rtn'] = _df1['rtn'].cumprod()

    # 총 누적수익율 변수에 대입 
    acc_rtn = _df1.iloc[-1, ]['acc_rtn']

    return _df1, acc_rtn