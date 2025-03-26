# 라이브러리/모듈 로드 
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf

import invest.quant.bollinger as boll
import invest.quant.buyandhold as bnh
import invest.quant.momentum as mmt

# 샘플 데이터 생성

# yfinance 데이터를 로드 함수 
def load_data(ticker, start = '2010-01-01', end = datetime.now()):
    Ticker = yf.Ticker(ticker)
    result = Ticker.history(start = start, end = end)
    return result

# class Invest 선언
class Invest:
    # 생성자 함수 생성 : 
        # 어떠한 데이터를 기준으로 할것인가? (주식 데이터)
        # 기준이 되는 컬럼의 이름
        # 투자의 시작 시간
        # 투자의 종료 시간
    def __init__(
            self, 
            _df, 
            _col = 'Adj Close',
            _start = '2010-01-01', 
            _end = datetime.now()
    ):
        # _df에서 Date 컬럼이 존재하면 index로 변환
        if 'Date' in _df.columns:
            _df.set_index('Date', inplace=True)
        # index를 시계열로 변환
        _df.index = pd.to_datetime(_df.index, utc=True)
        # tz 삭제
        try:
            _df.index = _df.index.tz_localize(None)
        except Exception as e:
            print(e)
        # 결측치, 무제한 값 제거 
        flag = _df.isin( [np.nan, np.inf, -np.inf] ).any(axis=1)
        self.df = _df.loc[~flag, [_col]]
        # _start, _end는 시계열로 변경 
        try:
            self.start = datetime.strptime(_start, '%Y-%m-%d')
            if type(_end) == 'str':
                self.end = datetime.strptime(_end, '%Y-%m-%d')
            else:
                self.end = _end
        except Exception as e:
            print(e)
            print('시작 시간 종료시간 타입이 맞지 않습니다 포멧은 YYYY-mm-dd')
            
        self.col=_col

        
    # 수익율을 계산하는 함수 
    def create_rtn(self, _df):
        # 복사본 생성 
        result = _df.copy()

        # rtn 컬럼을 생성 1을 대입 
        result['rtn'] = 1

        for idx in result.index:
            # 매수 
            if (result.shift().loc[idx, 'trade'] == '') &\
                (result.loc[idx, 'trade'] == 'buy'):
                buy = result.loc[idx, self.col]
                print(f"매수일 : {idx}, 매수가 : {buy}")
            # 매도
            elif (result.shift().loc[idx, 'trade'] == 'buy') &\
                (result.loc[idx, 'trade'] == ''):
                sell = result.loc[idx, self.col]
                print(f"매도일 : {idx}, 매도가 : {sell}")
                # 수익율 계산
                rtn = sell / buy
                # 수익율을 데이터프레임에 대입 
                result.loc[idx, 'rtn'] = rtn
                print(f"수익율 : {rtn}")
        # 누적수익율 계산하고 대입 
        result['acc_rtn'] = result['rtn'].cumprod()
        # 총 누적수익율을 변수에 저장 
        acc_rtn = result.iloc[-1, -1]
        return result, acc_rtn
    
    # buyandhold 방식 함수를 생성 
    def buyandhold(self):
        # 모듈 안에 있는 buyandhold 함수를 호출
        result, acc_rtn = bnh.buyandhold(self.df, 
                                         _start=self.start, 
                                         _end = self.end, 
                                         _col = self.col)
        print(f"투자기간 : {self.start} ~ {self.end}, 총 수익율 : {acc_rtn}")
        return result
    
    # bolliner 방식 함수를 생성
    def bollinger(self, _cnt = 20):
        # 밴드 생성 함수 
        band_df = boll.create_band(self.df, 
                                   _start = self.start, 
                                   _end = self.end, 
                                   _col = self.col, 
                                   _cnt = _cnt)
        # 거래 내역 함수
        trade_df = boll.create_trade(band_df)
        # 수익율 함수를 호출 
        result, acc_rtn = self.create_rtn(trade_df)

        print(f"투자기간 : {self.start} ~ {self.end}, 총 수익율 : {acc_rtn}")
        return result
    # momentum 방식 함수를 생성 
    def momentum(self, 
                 _momentum = 12, 
                 _score = 1, 
                 _select = 1
    ):
        # 기준연월 컬럼을 생성하는 함수
        ym_df = mmt.create_ym(self.df, _col = self.col)
        # 월말/월초 전월/전년도 데이터를 생성하는 함수
        month_df = mmt.create_month(ym_df, 
                                    _start = self.start, 
                                    _end = self.end, 
                                    _momentum = _momentum, 
                                    _select = _select)
        # 거래내역을 추가하는 함수 
        trade_df = mmt.create_trade(ym_df, 
                                    month_df, 
                                    _score = _score)
        # 수익율을 계산하는 함수 
        result, acc_rtn = self.create_rtn(trade_df)
        print(f"투자기간 : {self.start} ~ {self.end}, 총 수익율 : {acc_rtn}")
        return result