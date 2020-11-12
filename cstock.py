#-*- coding:utf-8 -*-

import time
import datetime
import numpy as np
import pandas as pd
import talib as ta
from talib import MACD, RSI, OBV, AD, ADOSC, WCLPRICE, WILLR ,ROC, DX,\
                  BETA, LINEARREG,LINEARREG_ANGLE,LINEARREG_INTERCEPT,LINEARREG_SLOPE,\
                  STDDEV,TSF,VAR,STOCH, WMA                 
import os.path

MAX_RSI = 75

class cstock(object):
    def __init__(self, id = 0, count = 1, amount=0):
        self.price = 0
        self.id = id

        self.count = count
        self.amount = amount
        self.cbuy = False
        self.csale = False 
        self.cbuyprice = 0
        self.csaleprice = 0
        
        self.wramount = amount

    def _issalechance(self, data):
        if self.csale:
            return False

        if  data.rsi > MAX_RSI  \
        and data.macd > 0 and data.signal > 20 and data.histogram < 0:
            return True
        else:
            return False

    def _isendsalechance(self, data):
        if self.csale == False:
            return False

        #if  abs(data.histogram) < 5 \
        if  data.price < self.csaleprice  \
        and data.rsi < MAX_RSI :
            return True
        else:
            return False

    def _isbuychance(self, data):
        if self.cbuy:
            return False
        
        if data.rsi < (100-MAX_RSI)   \
        and data.macd < 0 and data.signal < -20 and data.histogram > 0:
            return True
        else:
            return False

    def _isendbuychance(self, data):
        if self.cbuy == False:
            return False

        if  data.price > self.csaleprice  \
        and data.macd > 0 and data.signal > 0 and data.histogram < 0:
            return True
        else:
            return False

    def _onsalestart(self, data):
        '''
        WILLR >90、仮売なしの場合.
        High価格で仮売注文
        '''
        if(self._issalechance(data)):
            self.csale = True
            self.csaleprice = data.high
            self.willr = data.willr
            self.rsi = data.rsi     
            self.histogram = data.histogram       
            data.memo = 1
            
    def _onbuystart(self, data):
        '''
        WILLR <10、買なしの場合.
        low価格で買注文
        '''
        if(self._isbuychance(data)):
            self.cbuy = True
            self.cbuyprice = data.low
            self.willr = data.willr
            self.rsi = data.rsi
            self.histogram = data.histogram
            data.memo = -1

    def _onclosedeal(self, data):
        '''
        仮売有の場合、平均価格で買還注文。
        '''
        if(self._isendsalechance(data) ): #sale on time.
            self.wramount += self.count * (self.csaleprice - data.price)
            self.csale = False
            data.memo = 2
            
        '''
        買有の場合、平均価格で売注文。
        '''
        if(self._isendbuychance(data)):
            self.wramount += self.count * (data.price - self.cbuyprice)
            self.cbuy = False
            data.memo = -2

    def ondeal(self, df):
        '''
        ondeal(self, df,  dealcount = 1)
        loop all data, check deal chance, and deal on chance coming. 
        '''
        for i in range(1, len(df)):
            dyes = df.iloc[i-1] #data of yesteday.
            data = df.iloc[i]   #data of today.

            # check yesteday data. come in or not. 
            self._onbuystart(dyes)
            #self._onsalestart(dyes)
            if(dyes.memo > 0):
                df.memo[i-1] = dyes.memo

            # check today data if come in already. 
            # get out if it's a good time.          
            self._onclosedeal(data)
            if(data.memo > 0):
                df.memo[i] = data.memo

            #refresh amount.
            df.wramount[i] = self.wramount
            df.amount[i] = self.wramount - df.wramount[i-1]

    def doall(self, scode):
        print('starting by id:{}, scode :{}'.format(self.id, scode))
        strPath = "csv/{}.csv".format(scode)
        df = pd.read_csv(strPath, index_col="date")
        self.refresh(df)
        df = df.dropna()
        self.ondeal(df)
        df.to_csv("csv/{}_r1.csv".format(scode))

if __name__ == "__main__":
    code = 2127
    df = pd.read_csv("csv/{}.csv".format(code), index_col="date")
    df  = cstock.refresh(df)
    df = df.dropna()
    df.to_csv("csv/{}_r1.csv".format(code))
