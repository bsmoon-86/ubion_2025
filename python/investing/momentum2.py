import pandas as pd 
from datetime import datetime
import numpy as np
import os 
import glob


# 월별 수익율을 계산하는 함수 생성 
def create_1M_rtn(_df, _ticker, _start = "2010-01-01", _col = 'Adj Close'):
    # 복사본 생성 
    result = _df.copy()
    # 컬럼에 Date가 포함되어있는지 확인 
    if 'Date' in result.columns:
        result = result.loc[result['Date'] >= _start, ['Date', _col]]
        # Date 컬럼의 데이터를 시계열로 변경
        result['Date'] = pd.to_datetime(result['Date'], format='%Y-%m-%d')
    else:
        result.index = pd.to_datetime(result.index, inplace=True)
        result = result.loc[_start:, [_col]]
        result.reset_index(inplace=True)
    # 기준 년월 컬럼을 생성
    result['STD-YM'] = result['Date'].dt.strftime('%Y-%m')
    result['1m_rtn'] = 0
    result['CODE'] = _ticker
    # 기준 년월의 중복데이터를 제거하고 고유한 값들을 리스트로 생성
    ym_list = result['STD-YM'].unique()
    return result, ym_list

# 함수 생성 (경로 지정 매개변수)
def data_load(_path = "./data/"):
    files = glob.glob(f"{_path}/*.csv")
    # 새로운 데이터프레임을 생성 
    # 종목별 데이터프레임 
    stock_df = pd.DataFrame()
    # 월말 데이터프레임 
    month_last_df = pd.DataFrame()

    for file in files:
        folder, name = os.path.split(file)
        # print(folder, name)
        head, tail = os.path.splitext(name)
        # print(head, tail)
        # head는 create_1M_rtn 함수에 ticker 인자값으로 사용

        # 데이터 파일을 로드 
        read_df = pd.read_csv(file)

        # create_1M_rtn 함수를 호출 
        price_df, ym_list = create_1M_rtn(read_df, head)

        # 유니언 결합 (단순한 행 결합 함수)
        stock_df = pd.concat([stock_df, price_df], axis=0)

        # 월별 상태 모멘텀을 계산하기 위해 1개월간의 수익율 계산
        for ym in ym_list:
            flag = price_df['STD-YM'] == ym
            m_rtn = price_df.loc[flag,].iloc[-1, 1] / price_df.loc[flag,].iloc[0, 1]
            price_df.loc[flag, '1m_rtn'] = m_rtn
            data = price_df.loc[flag, ['Date','CODE', '1m_rtn']].tail(1)
            month_last_df = pd.concat([month_last_df, data], axis=0) 

    return stock_df, month_last_df

## 월별 수익율을 기준으로 하여 랭크를 설정하는 함수 
def create_position(_df, _pct = 0.15):

    df = _df.copy()
    rank_df = df.pivot_table(
        index = 'Date', 
        columns= 'CODE', 
        values= '1m_rtn'
    )
    rank_df = rank_df.rank(
        axis=1, 
        ascending=False, 
        method='max', 
        pct=True
    )
    rank_df =  rank_df.where(rank_df < _pct, 0)

    rank_df[rank_df != 0] = 1

    sig_dict = dict()

    for date in rank_df.index:
        # print(date)
        ticker_list = list(
            rank_df.loc[date, rank_df.loc[date] >= 1].index)
        # print(ticker_list)
        sig_dict[date] = ticker_list

    stock_code = list(rank_df.columns)

    return sig_dict, stock_code

# 거래 내역컬럼을 생성하는 데이터프레임 생성하는 함수 
def create_trade_book(_df, _code, _sig_dict):
    book = _df.pivot_table(
        index='Date', 
        columns = 'CODE', 
        values= _df.columns[1]
    )
    book['STD-YM'] = book.index.strftime('%Y-%m')
    for c in _code:
        book['p'+c] = ""
        book['r'+c] = ""

        # 포지션을 생성 
    for date, values in _sig_dict.items():
        # print(date, values)
        for stock in values:
            book.loc[date, 'p'+stock] = 'ready'+stock
    return book


# 거래 내역 추가 
def trading(_book, s_code):
    book = _book.copy()
    std_ym = ""
    buy_phase = False


    # 종목별로 순회
    for code in s_code:
        for i in book.index:
            # 해당 종목코드의 포지션을 잡는다.
            if (book.loc[i, 'p'+code] == "") & \
                (book.shift().loc[i, 'p'+code] == "ready"+code):
                std_ym = book.loc[i, 'STD-YM']
                buy_phase = True
            # 해당 종목코드에서 신호가 잡혀있다면 매수 상태 유지 
            if (book.loc[i, 'p'+code] == "") & \
                (book.loc[i, 'STD-YM'] == std_ym) & \
                (buy_phase):
                book.loc[i, 'p'+code] = 'buy'+code
            
            # std_ym, buy_phase 초기화
            if book.loc[i, 'p'+code] == "":
                std_ym = ""
                buy_phase = False
    return book

# 수익율 계산 함수 
def multi_returns(_book, s_code):
    book = _book.copy()
    rtn = 1
    buy_dict = dict()
    sell_dict = dict()

    for i in book.index:
        for code in s_code:
            # 매수 (p+code 2일전에 "" 1일전에 ready 오늘이 buy)
            if (book.shift(2).loc[i, "p"+code] == "") & \
                (_book.shift(1).loc[i, 'p'+code] == "ready"+code) & \
                (book.loc[i, 'p'+code] == "buy"+code):
                buy_dict[code] = book.loc[i, code]
                print(f"매수일 : {i}, 종목코드 : {code}, 매수가 : {buy_dict[code]}")
            # 매도 (1일 전의 pcode가 buy 오늘의 pcode가 "")
            elif (book.shift(1).loc[i, "p"+code] == "buy"+code) & \
                (book.loc[i, 'p'+code] == ""):
                sell_dict[code] = book.loc[i, code]
                # 수익율 계산 
                rtn = sell_dict[code] / buy_dict[code]
                book.loc[i, 'r'+code] = rtn
                print(f"매도일 : {i}, 종목코드 : {code}, 매도가 : {sell_dict[code]}, 수익율 : {rtn}")
            # buy_dict, sell_dict 데이터를 초기화
            if book.loc[i, 'p'+code] == "":
                buy_dict[code] = 0
                sell_dict[code] = 0
    return book


# 누적 수익율 계산 함수 
def multi_acc_returns(_book, s_code):
    book = _book.copy()
    # 누적 수익율 변수 생성
    acc_rtn = 1
    for i in book.index:
        count = 0
        rtn = 0
        for code in s_code:
            # 수익율 데이터가 존재하는 경우
            if book.loc[i, 'r'+code]:
                count += 1
                rtn += book.loc[i, "r"+code]
        if (rtn != 0) & (count != 0):
            acc_rtn *= (rtn / count)
            print(f"누적 매도일 : {i}, 매도 종목수 : {count}, 수익율 : {round(rtn/count, 2)}")
        book.loc[i, 'acc_rtn'] = acc_rtn
    
    return book, acc_rtn


                