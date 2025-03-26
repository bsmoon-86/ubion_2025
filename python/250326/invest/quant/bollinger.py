from datetime import datetime
import pandas as pd
import numpy as np 


def create_band(
        _df, 
        _col, 
        _start, 
        _end, 
        _cnt = 20
):
    # 복사본을 생성 
    result = _df.copy()
    # 이동평균선, 상단 밴드, 하단 밴드 생성 
    result['center'] = result[_col].rolling(_cnt).mean()
    result['up'] = \
        result['center'] + (2 * result[_col].rolling(_cnt).std())
    result['down'] = \
        result['center'] - (2 * result[_col].rolling(_cnt).std())

    # 시작 시간과 종료 시간을 기준으로 데이터를 필터링 
    result = result.loc[_start : _end]
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

