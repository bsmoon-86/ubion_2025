import pandas as pd
import numpy as np
from datetime import datetime

def create_ym(
        _df, 
        _col = 'Adj Close'
):
    # 복사본 생성 
    result = _df.copy()
    # Date 컬럼이 존재하는가?
    if 'Date' in result.columns:
        # Date를 인덱스로 변경
        result.set_index('Date', inplace=True)
    # index를 시계열로 변경
    result.index = pd.to_datetime(result.index, utc=True)
    try:
        result.index = result.index.tz_localize(None)
    except Exception as e:
        print(e)
    # 결측치 무한대 값들은 제외
    flag = result.isin( [np.nan, np.inf, -np.inf] ).any(axis=1)
    result = result.loc[~flag, [_col] ]
    # 파생변수를 생성 
    result['STD-YM'] = result.index.strftime('%Y-%m')
    return result

def create_month(
        _df, 
        _start = '2010-01-01', 
        _end = datetime.now(), 
        _momentum = 12, 
        _select = 1
):
    # _select가 1과 같다면
    if _select == 1:
        # 월말 데이터의 조건식을 생성
        flag = _df['STD-YM'] != _df.shift(-1)['STD-YM']
        # result = _df.loc[flag]
    elif _select == 0:
        # 월초 데이터의 조건식 생성
        flag = _df['STD-YM'] != _df.shift(1)['STD-YM']
        # result = _df.loc[flag]
    else:
        return "_select의 값은 0 아니면 1 입니다."
    result = _df.loc[flag]
    # 기준이 되는 컬럼의 이름을 변수에 저장 
    col = result.columns[0]
    # BF1컬럼을 생성
    # 전월의 데이터를 대입
    result['BF1'] = result.shift(1)[col]
    # _momentum 값의 과거의 개월수 데이터 대입 
    result['BF2'] = result.shift(_momentum)[col]
    try:
        result.index = result.index.tz_localize(None)
    except Exception as e:
        print(e)
    # 시작 시간과 종료시간을 기준으로 데이터 필터링 
    result = result.loc[_start : _end]
    return result
    
def create_trade(
        _df1, 
        _df2, 
        _score = 1
):
    # 복사본 생성
    result = _df1.copy()
    # trade 컬럼을 추가 
    result['trade'] = ''

    # 반복문 생성 -> _df2를 기준으로 반복
    for idx in _df2.index:
        signal = ''
        # 모멘텀 인덱스를 계산
        momentum_index = _df2.loc[idx, 'BF1'] / \
              _df2.loc[idx,'BF2'] - _score
        # 모멘텀 인덱스를 이용하여 구매 신호 생성
        flag = (momentum_index > 0) & (momentum_index != np.inf)
        if flag :
            signal = 'buy'
        # 출력 
        print(f"날짜 : {idx}, 모멘텀 인덱스 : {momentum_index}, signal : {signal}")
        # 구매 신호를 result에 대입 
        result.loc[idx:, 'trade'] = signal
    
    return result
