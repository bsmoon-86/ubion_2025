import pandas as pd 
import numpy as np
import os 
from glob import glob

# 월별 수익율을 계산하기 위해 데이터의 정제하는 함수 
def create_1m_rtn(_df, 
                  _ticker,
                  _start = '2010-01-01', 
                  _col = 'Adj Close'):
    # 복사본을 생성
    result = _df.copy()
    # 'Date' 컬럼을 인덱스로 변환
    if 'Date' in result.columns:
        result.set_index('Date', inplace=True)
    # 인덱스를 시계열로 변경 
    result.index = pd.to_datetime(result.index)
    # 시작 시간과 기준이 되는 컬럼을 데이터를 필터링 
    result = result.loc[_start: , [_col]]
    # 기준년월 컬럼을 생성 
    result['STD-YM'] = result.index.strftime('%Y-%m')
    # 월별 수익율 컬럼을 생성
    result['1m_rtn'] = 0
    # CODE 컬럼을 생성 _ticker대입
    result['CODE'] = _ticker
    # 기준년월의 중복데이터를 제거하고 리스트형태로 생성
    ym_list = result['STD-YM'].unique()
    return result, ym_list

# 데이터를 로드하고 월별 수익율 계산하여 데이터프레임을 결합하는 함수
def data_load(_path = "./data", 
              _end = 'csv', 
              _start = '2010-01-01', 
              _col = 'Adj Close'):
    # _path 경로 안에 있는 모든 csv 파일의 목록을 생성
    files = glob(f"{_path}/*.{_end}")
    # 로드가 되는 파일들을 결합할 빈 데이터프레임 생성
    stock_df = pd.DataFrame()
    # 월말의 데이터를 결합한 데이터프레임 생성
    month_last_df = pd.DataFrame()

    # files 목록에서 모든 데이터를 로드
    for file in files:
        # file -> ./data/AAPL.csv
        folder , name = os.path.split(file)
        head, tail = os.path.splitext(name)

        # 데이터 파일을 로드 
        read_df = pd.read_csv(file)

        # read_df를 create_1m_rtn에 대입 
        price_df, ym_list = create_1m_rtn(read_df, head, _start, _col)

        # price_df를 stock_df에 단순한 행 결합 
        stock_df = pd.concat( [stock_df, price_df] )

        # ym_list를 이용해서 1개월간의 수익율 계산
        for ym in ym_list:
            # 조건식 생성 
            # ym은 기준년월의 유니크 값
            flag = price_df['STD-YM'] == ym
            # 월초의 기준이 되는 컬럼의 값 구매가
            buy = price_df.loc[flag].iloc[0, 0]
            # 월말의 기준이되는 컬럼의 값 판매가
            sell = price_df.loc[flag].iloc[-1, 0]
            # 수익율 계산산
            m_rtn = sell / buy
            # price_df flag 조건에 맞는 1m_rtn에 대입 
            price_df.loc[flag, '1m_rtn'] = m_rtn
            # 월말의 데이터을 추출하여 month_last_df에 결합
            data = price_df.loc[flag, ['CODE', '1m_rtn']].tail(1)
            month_last_df = pd.concat( [month_last_df, data] )
    return stock_df, month_last_df

# 월별 수익율을 기준으로 랭크를 설정하는 함수 
def create_position(_df, _pct = 0.15):
    # _df를 인덱스를 초기화해서 다른 변수에 저장 
    result = _df.reset_index()
    # _pct의 값이 1보다 크거나 같은 경우 
    if _pct >= 1:
        _pct = _pct / 100
    # 데이터프레임으 재구조화
    result = result.pivot_table(
        index = 'Date', 
        columns = 'CODE', 
        values = '1m_rtn'
    )
    # rank 함수를 이용하여 순위를 퍼센트로 잡는다다
    result = result.rank(
        axis=1, 
        ascending = False, 
        method = 'max', 
        pct = True
    )
    # print(result)
    # _pct를 기준으로 해당하는 값보다 큰 퍼센트는 0으로 대체
    result = result.where(result < _pct, 0)
    # value가 0이 아니라면 1로 변경
    result[result != 0] = 1

    # 거래 신호를 딕셔너리로 생성하기 위한 빈 딕셔너리 생성 
    sig_dict = dict()

    # 반복문을 이용해서 sig_dict에 데이터를 대입
    for date in result.index:
        # 구매 신호의 종목 리스트
        ticker_list = list(
            result.loc[date, result.loc[date] == 1].index
        )
        sig_dict[date] = ticker_list
        # { 2010-01-28 : [AAPL, BND] }

    # 종목들의 리스트
    stock_code = list(result.columns)
    return sig_dict, stock_code

# 거래 내역컬럼을 생성하는 함수 
def create_trade_book(_df, _codes, _signal):
    # 준비를 넣어주는 함수 
    book = _df.reset_index()
    book = book.pivot_table(
        index = 'Date', 
        columns = 'CODE', 
        values = book.columns[1]
    )
    book['STD-YM'] = book.index.strftime('%Y-%m')
    # code별로 컬럼을 생성 
    for code in _codes:
        book[f"p_{code}"] = ""
        book[f"r_{code}"] = ""
    # 구매 포지션을 대입 
    for date, values in _signal.items():
        # values는 리스트형태의 데이터
        for value in values:
            book.loc[date, f"p_{value}"] = f"ready_{value}"
    return book

# 거래 내역 추가하는 함수
def create_trading(_df, _codes):
    book = _df.copy()
    # 기준년월 변수 생성 
    std_ym = ""
    # 구매 신호
    buy_phase = False

    # 종목 별로 반복
    for code in _codes:
        # book를 반복 실행
        for idx in book.index:
            col = f"p_{code}"
            # ready_code 포지션을 잡는다. 
            # 전날의 col의 값이 ready이고 오늘의 col의 값이 ""
            if (book.loc[idx, col] == "") & \
                (book.shift(1).loc[idx, col] == f"ready_{code}"):
                # std_ym에 기준년월을 대입 
                std_ym = book.loc[idx, 'STD-YM']
                # 구매 신호를 True 변경
                buy_phase = True
            # 구매 내역을 대입 
            # col의 값이 ""
            # book['STD-YM']과 std_ym이 같은 경우
            # 구매 신호가 True인 경우
            if (book.loc[idx, col] == "") & \
                (book.loc[idx, 'STD-YM'] == std_ym) & \
                (buy_phase):
                book.loc[idx, col] = f"buy_{code}"
            # std_ym과 buy_phase를 초기화
            if book.loc[idx, col] == '':
                std_ym = ""
                buy_phase = False
    return book


# 수익율 계산하는 함수 
def multi_returns(_df, _codes):
    book = _df.copy()
    rtn = 1
    buy_dict = dict()
    sell_dict = dict()

    # 반복문 생성 (인덱스 기준)
    for idx in book.index:
        # _codes 기준 반복문
        for code in _codes:
            # 매수 : 2일전에 "" 1일전에 "ready" 오늘이 'buy'
            col = f"p_{code}"
            if (book.shift(2).loc[idx, col] == '') & \
                (book.shift(1).loc[idx, col] == f'ready_{code}') & \
                    (book.loc[idx, col] == f'buy_{code}'):
                # buy_dict에 키: 벨류 추가 
                buy_dict[code] = book.loc[idx, code]
                print(f"매수일 : {idx}, 매수종목 : {code}, 매수가 : {buy_dict[code]}")
            # 매도 : 1일전에 'buy' 오늘이 ''
            elif (book.shift(1).loc[idx, col] == f"buy_{code}") & \
                (book.loc[idx, col] == ''):
                sell_dict[code] = book.loc[idx, code]
                # 수익율 계산
                rtn = sell_dict[code] / buy_dict[code]
                # 수익율 r_code 컬럼에 대입 
                book.loc[idx, f"r_{code}"] = rtn
                print(f"매도일 : {idx}, 매도 종목 : {code}, 매도가 : {sell_dict[code]}, 수익율 : {rtn}")
            # dict 초기화
            if book.loc[idx, col] == '':
                buy_dict[code] = ''
                sell_dict[code] = ''
    return book

# 누적 수익율을 계산하는 함수
def multi_acc_returns(_df, _codes):
    book = _df.copy()
    # 누적 수익율 변수 생성
    acc_rtn = 1

    # 데이터프레임을 반복
    for idx in book.index:
        count = 0
        rtn = 0
        for code in _codes:
            col = f"r_{code}"
            # 수익이 존재하는가?
            if book.loc[idx, col]:
                count += 1
                rtn += book.loc[idx, col]
        if (rtn != 0) & (count != 0):
            acc_rtn *= (rtn / count)
            print(f"누적 매도일 : {idx}, 매도 종목수 : {count}, 수익율 : {round(acc_rtn, 2)}")
        book.loc[idx, 'acc_rtn'] = acc_rtn
    return book, acc_rtn    