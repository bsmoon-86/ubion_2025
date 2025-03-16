# 4개의 투자전략 모듈을 로드 
from invest.quant import bnh
from invest.quant import bollinger as boll
from invest.quant import halloween as hw
from invest.quant import momentum as mmt
from datetime import datetime
import pandas as pd
import numpy as np
import yfinance as yf

import importlib
importlib.reload(bnh)
importlib.reload(boll)
importlib.reload(hw)
importlib.reload(mmt)

AAPL = pd.read_csv(
    r"C:\Users\moons\Documents\GitHub\ubion-10\python\invest\data\AAPL.csv", 
    index_col='Date')
AMZN = pd.read_csv(
    r"C:\Users\moons\Documents\GitHub\ubion-10\python\invest\data\AMZN.csv", 
    index_col='Date')
BND = pd.read_csv(
    r"C:\Users\moons\Documents\GitHub\ubion-10\python\invest\data\BND.csv", 
    index_col='Date')

def load_data(ticker, _start = "2010-01-01"):
    result = yf.download(ticker, start=_start)
    return result

class Invest:
    # 생성자 함수 : class를 생성할때 최초로 한번 실행이 되는 함수
    def __init__(
            self, 
            _df, 
            _col = 'Adj Close', 
            _start = "2010-01-01",
            _end = datetime.now()
    ):
        # Date가 컬럼에 포함되어있다면 인덱스로 변경 
        if 'Date' in _df.columns:
            _df.set_index('Date', inplace=True)
        # 인덱스를 시계열 데이터로 변경 
        _df.index = pd.to_datetime(_df.index, format='%Y-%m-%d')
        # _df의 결측치와 무한대 제거하고 기준이 되는 컬럼만 두고 나머지 삭제
        flag = _df.isin([np.nan, np.inf, -np.inf]).any(axis=1)
        self.df = _df.loc[~flag, [_col]]
        # _start, _end는 시계열 데이터로 변경해서 객체 변수에 대입 
        try:
            self.start = datetime.strptime(_start, "%Y-%m-%d")
            if type(_end) == 'str':
                self.end = datetime.strptime(_end, '%Y-%m-%d')
            else:
                self.end = _end
        except:
            print('투자기간 인자값의 포멧이 잘못되었습니다. (YYYY-mm-dd)')
        self.col = _col
    
    def buyandhold(self):
        result , acc_rtn = bnh.buyandhold(
            self.df, self.col ,self.start, self.end)
        print(acc_rtn)
        return result, acc_rtn
    
    def bollinger(self, _cnt = 20):
        # 밴드를 생성하는 함수 호출 
        band_df = boll.create_band(
            self.df, self.col, self.start, self.end, _cnt)
        # 거래 내역을 추가하는 함수 호출 
        trade_df = boll.create_trade(band_df)
        # 수익율 계산하는 함수 호출 
        result , acc_rtn = boll.create_rtn(trade_df)

        return result, acc_rtn
    
    def halloween(self, _month=11):
        # 시작 년도 
        h_start = self.start.year
        # 종료 년도
        h_end = self.end.year
        result, acc_rtn = hw.six_month(self.df, self.col, h_start, h_end, _month)
        return result, acc_rtn
    
    def momentum(self, _momentum = 12, _score = 1, _select = 1):
        ym_df = mmt.create_YM(self.df, self.col)
        month_df = mmt.create_month(
            ym_df, self.start, self.end, _momentum, _select)
        result, acc_rtn = mmt.create_rtn(ym_df, month_df, _score)
        return result, acc_rtn

