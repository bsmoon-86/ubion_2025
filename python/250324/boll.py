from datetime import datetime
import pandas as pd
import numpy as np 


def create_band(
        _df, 
        _col = 'Adj Close', 
        _start = '2010-01-01', 
        _end = datetime.now(), 
        _cnt = 20
):
    # 복사본을 생성 
    result = _df.copy()
    # 컬럼 중 Date 컬럼이 존재하는가?
    if 'Date' in result.columns:
        # Date를 인덱스로 변환
        result.set_index('Date', inplace = True)
    # index를 시계열 데이터로 변경 
    result.index = pd.to_datetime(result.index, format='%Y-%m-%d')
    # 결측치, 무한대를 제외시킨다. 
    flag = result.isin( [np.nan, np.inf, -np.inf] ).any(axis=1)
    result = result.loc[~flag, [_col]]
    # 이동평균선, 상단 밴드, 하단 밴드 생성 
    result['center'] = result[_col].rolling(_cnt).mean()
    result['up'] = \
        result['center'] + (2 * result[_col].rolling(_cnt).std())
    result['down'] = \
        result['center'] - (2 * result[_col].rolling(_cnt).std())
    # 시작 시간과 종료 시간을 시계열 데이터로 변경 
    try :
        start = datetime.strptime(_start, '%Y-%m-%d')
        # print(type(start))
        if type(_end) == 'str':
            end = datetime.strptime(_end, '%Y-%m-%d')
        else:
            end = _end
        # print(type(end))
        start = pd.Timestamp(start, tz='UTC')
        end = pd.Timestamp(end, tz='UTC')
    except:
        print('시작 시간과 종료 시간의 포멧은 YYYY-mm-dd 입니다.')
        return ''
    # 시작 시간과 종료 시간을 기준으로 데이터를 필터링 
    result = result.loc[start : end]
    return result

def create_trade(_df):
    result = _df.copy()
    # 첫번째 컬럼의 이름을 변수에 저장 
    col = result.columns[0]

    # 보유 내역 컬럼을 생성 '' 대입
    result['trade'] = ''

    # 내역 추가 
    for idx in result.index:
        # 상단 밴드보다 기준이 되는 컬럼의 값이 크거나 같은 경우
        if result.loc[idx, col] >= result.loc[idx, 'up']:
            # 매수중인 경우 매도 // 보유중 아니면 유지
            # trade = ''
            result.loc[idx, 'trade'] = ''
        # 하단 밴드보다 기준이 되는 컬럼의 값이 작거나 같은 경우 
        elif result.loc[idx, 'down'] >= result.loc[idx, col]:
            # 보유중이 아니면 매수 // 보유중이면 유지 
            # trade = 'buy'
            result.loc[idx, 'trade'] = 'buy'
        # 밴드 중간에 기준이 되는 컬럼의 값이 존재한다면
        else:
            # 보유중이라면 보유 유지
            if result.shift().loc[idx, 'trade'] == 'buy':
                result.loc[idx, 'trade'] = 'buy'
            # 보유중이 아니라면 유지
            else:
                result.loc[idx, 'trade'] = ''
    return result


def create_rtn(_df):
    # 복사본 생성 
    result = _df.copy()
    # 컬럼의 첫번째 이름을 변수에 저장 
    col = result.columns[0]
    # 수익율 컬럼을 생성 1대입
    result['rtn'] = 1

    # 수익율 생성 
    for idx in result.index:
        # 매수 
        if (result.shift().loc[idx, 'trade'] == '') & \
            (result.loc[idx, 'trade'] == 'buy'):
            buy = result.loc[idx, col]
            print(f"매수일 : {idx}, 매수가 : {buy}")
        # 매도
        elif (result.shift().loc[idx, 'trade'] == 'buy') & \
            (result.loc[idx, 'trade'] == ''):
            sell = result.loc[idx, col]
            print(f"매도일 : {idx}, 매도가 : {sell}")
            # 수익율 계산 
            rtn = sell / buy
            # 컬럼에 대입 
            result.loc[idx, 'rtn'] = rtn
            print(f"수익율 : {rtn}")
    # 누적 수익율 계산
    result['acc_rtn'] = result['rtn'].cumprod()
    # 최종 누적 수익율 변수 저장
    acc_rtn = result.iloc[-1, -1]
    return result, acc_rtn