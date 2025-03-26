import pandas as pd
from datetime import datetime

def buyandhold(
        _df, 
        _start, 
        _end, 
        _col
):
    # DataFrame을 복사 copy()
    result = _df.copy()
    # 인덱스가 0부터 시작하는 인덱스 // Date 인덱스 경우 

    
    # 시작시간과 종료시간을 기준으로 데이터를 필터링 -> 특정 컬럼만 필터링
    result = result.loc[_start : _end, [_col]]
    print(_start)
    print(_end)
    print(_col)
    print("바이앤홀드 df : ", len(result))
    # 일별 수익율 컬럼을 생성 
    result['daily_rtn'] = (result[_col].pct_change() + 1).fillna(1)
    # 누적 수익율 컬럼을 생성
    result['acc_rtn'] = result['daily_rtn'].cumprod()
    print(f"""{_start.strftime('%Y-%m-%d')}부터 
          {_end.strftime('%Y-%m-%d')}까지 
          buyandhold의 수익율은 {result.iloc[-1, 2]}입니다""")
    # return데이터에 데이터프레임, 총 수익율 
    acc_rtn = result.iloc[-1, 2]
    return result, acc_rtn
