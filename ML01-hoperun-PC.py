# -*- coding: utf-8 -*-
import datetime
import numpy as np
import pandas as pd
import talib as ta
from talib import MACD, STOCH, SMA, BBANDS,RSI, OBV, AD, ADOSC, \
                AVGPRICE, WCLPRICE, MEDPRICE, \
                ATR,NATR,TRANGE ,\
                CDL2CROWS,CDL3BLACKCROWS ,CDL3INSIDE ,CDL3LINESTRIKE ,CDL3OUTSIDE,\
                HT_DCPERIOD,HT_DCPHASE,HT_PHASOR ,HT_SINE ,HT_TRENDMODE ,\
                BETA ,CORREL ,LINEARREG ,LINEARREG_ANGLE ,LINEARREG_INTERCEPT ,\
                LINEARREG_SLOPE ,STDDEV ,TSF,VAR ,\
                ACOS,ASIN,ATAN,CEIL,COS,COSH,EXP,FLOOR,LN,LOG10,SIN,SINH,SQRT,TAN,TANH,\
                ADD,DIV,MAX,MAXINDEX,MIN,MININDEX,MINMAX,MINMAXINDEX,SUB,SUM
                
'''
                CDL3STARSINSOUTH ,CDL3WHITESOLDIERS ,CDLABANDONEDBABY ,\
                CDLADVANCEBLOCK ,CDLBELTHOLD ,CDLBREAKAWAY ,CDLCLOSINGMARUBOZU ,\
                CDLCONCEALBABYSWALL ,CDLCOUNTERATTACK ,CDLDARKCLOUDCOVER ,\
                CDLDOJI ,CDLDOJISTAR ,CDLDRAGONFLYDOJI ,CDLENGULFING ,\
                CDLEVENINGDOJISTAR ,CDLEVENINGSTAR ,CDLGAPSIDESIDEWHITE ,\
                CDLGRAVESTONEDOJI ,CDLHAMMER ,CDLHANGINGMAN ,CDLHARAMI ,\
                CDLHARAMICROSS ,CDLHIGHWAVE ,CDLHIKKAKE ,CDLHIKKAKEMOD ,\
                CDLHOMINGPIGEON ,CDLIDENTICAL3CROWS ,CDLINNECK ,\
                CDLINVERTEDHAMMER ,CDLKICKING ,CDLKICKINGBYLENGTH ,
                CDLLADDERBOTTOM ,CDLLONGLEGGEDDOJI ,CDLLONGLINE ,CDLMARUBOZU 
'''
def setvolume(open, high, low, close, volume):
   #volume
    df["obv"] = OBV(close, volume)
    #df["ad"] = AD(high, low, close, volume)
    df["ad"] = ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)

def price_transform(open, high, low, close, volume):
    #price_transform
    df["ap"] = AVGPRICE(open, high, low, close) #Average Price
    df["wcp"] = WCLPRICE(high, low, close) #Weighted Close Price
    df["mp"] = MEDPRICE(high, low) #Median Price

def Volatility_Indicator(open, high, low, close, volume):
    #Volatility Indicator Functions
    df["atr"] = ATR(high, low, close, timeperiod=14)#Average True Range
    df["natr"] = NATR(high, low, close, timeperiod=14) #Normalized Average True Range
    df["tr"]  = TRANGE(high, low, close)

def Pattern_Recognition(open, high, low, close, volume):
    #Pattern Recognition
    df["pt2crow"] = CDL2CROWS(open, high, low, close)
    df["pt3crow"] = CDL3BLACKCROWS(open, high, low, close)

def Cycle_Indicator(open, high, low, close, volume):
    #Cycle Indicator Functions
    df["htdcp"]  = HT_DCPERIOD(close)

def Statistic(open, high, low, close, volume):
    #Statistic Functions
    df["beta"]  = BETA(high, low, timeperiod=5)
    df["tsf"] = TSF(close, timeperiod=14)
    df["var"]  = VAR(close, timeperiod=5, nbdev=1)

#Math Transform Functions
#Math Operator Functions

if __name__ == "__main__":
    #READ data.
    df = pd.read_csv("6641.csv", index_col=["date"], parse_dates=True)
    open = df.open.values.astype("f8")
    close = df.close.values.astype("f8")
    high = df.high.values.astype("f8")
    low = df.low.values.astype("f8")
    volume = df.volume.values.astype("f8")
    
    #refresh data.
    df["rsi"] = RSI(close)    
    df["macd"], df["signal"], df["histogram"] = MACD(close)
    df["min"],df["max"] = MINMAX(close)
    df = df.dropna()

    balance = 1000000
    deal(df,balance)

    df.to_csv("result_6641_1.csv", index=True)


def deal(df, balance):
    dealflag = False
    dealtype = 0
    priceSale = 0

    df["balance"] = 0
    df["dealtype"] = 0 
    
    MAX_RSI = 70
    MIN_RSI = 38
    ST_COUNT = 100
    
    #日付昇順で、loop処理を行う
    for i in range(len(df)):
        price = df.close[i] 
        if dealtype in [-1,0,1]:
            if df.rsi[i] > MAX_RSI: #売
                dealflag = True   #取引開始
                dealtype = 2      #信用借売
                priceSale = price
            elif df.rsi[i] < MIN_RSI: #買
                dealflag = True   #取引開始
                dealtype = -2      #信用売
                priceSale = price    
        else:            
            if df.rsi[i] < MIN_RSI and dealtype == 2 : #買
                dealflag = False   #取引完了
                dealtype = 1      #信用借返
                balance = balance + ST_COUNT * (priceSale - price)
            elif df.rsi[i] > MAX_RSI and dealtype == -2 : #売
                dealflag = False   #取引完了
                dealtype = -1      #信用売
                balance = balance + ST_COUNT * (price - priceSale)
            else:
                pass
        
        df['balance'][i] = balance
        df['dealtype'][i] = dealtype
