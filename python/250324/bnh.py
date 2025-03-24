import pandas as pd
from datetime import datetime

def buyandhold(
        _df, 
        _start = "2010-01-01", 
        _end = datetime.now(), 
        _col = 'Adj Close'
):
    # DataFrame을 복사 copy()
    result = _df.copy()
    # 인덱스가 0부터 시작하는 인덱스 // Date 인덱스 경우 
    # 데이터프레임에서 컬럼 중 Date라는 컬럼이 존재하는가?
    if "Date" in result.columns:
        # Date 컬럼을 인덱스로 변경 
        result.set_index('Date', inplace=True)
    # index를 시계열데이터로 변경
    result.index = pd.to_datetime(result.index)

    # _start, _end 값을 시계열 데이터로 변경 
    try : 
        start = datetime.strptime(_start, "%Y-%m-%d")
        # _end은 기본값은 시계열인 경우는 아무 행동도 하지 않는다. 
        # 문자열인 경우는 시계열로 데이터를 변경 
        if type(_end) == 'str':
            end = datetime.strptime(_end, '%Y-%m-%d')
        else:
            end = _end
    except:
        print(f"시작시간과 종료시간의 포멧은 YYYY-mm-dd 형식입니다")
        return ""
    
    # 시작시간과 종료시간을 기준으로 데이터를 필터링 -> 특정 컬럼만 필터링
    result = result.loc[start : end, [_col]]
    # 일별 수익율 컬럼을 생성 
    result['daily_rtn'] = (result[_col].pct_change() + 1).fillna(1)
    # 누적 수익율 컬럼을 생성
    result['acc_rtn'] = result['daily_rtn'].cumprod()
    print(f"""{start.strftime('%Y-%m-%d')}부터 
          {end.strftime('%Y-%m-%d')}까지 
          buyandhold의 수익율은 {result.iloc[-1, 2]}입니다""")
    # return데이터에 데이터프레임, 총 수익율 
    acc_rtn = result.iloc[-1, 2]
    return result, acc_rtn
