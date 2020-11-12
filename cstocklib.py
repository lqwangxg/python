#-*- coding:utf-8 -*-
import os.path 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
from talib import MACD, RSI, OBV, AD, ADOSC, WCLPRICE, WILLR ,ROC, DX,\
                  BETA, LINEARREG,LINEARREG_ANGLE,LINEARREG_INTERCEPT,LINEARREG_SLOPE,\
                  STDDEV,TSF,VAR,STOCH, WMA                 
MAX_DAYS= 80
MAX_J = 95
MAX_FEE=30
MAX_HL=50

def refresh(df, days = MAX_DAYS):
    df = df[-(days + 1): -1]
    open =  df.open.astype("f8").values
    high =  df.high.astype("f8").values
    low =  df.low.astype("f8").values
    df["h2"] =0
    df["l2"] =0
    close = df.close.astype("f8").values
    volume = df.volume.astype("f8").values

    #df["wma"] = WMA(close)
    #df["price"] = WCLPRICE(high, low, close) #Weighted Close Price
    #df["obv"] = OBV(close,volume)
    #df["ad"] = AD(high, low, close, volume)
    #df["macd"],df["signal"],df["histogram"] = MACD(close)
    df["rsi"] =RSI(close) #relative strong index
    #df["willr"] = WILLR(high, low, close) + 100 #will index
    df["roc"] = ROC(close)
    k, d = STOCH(high, low, close) 
    df["K"] = k
    df["D"] = d 
    df["J"] = k * 3 - d * 2    
    
    #統計
    #df["beta"] = BETA(high,low)
    #df["linearR"] = LINEARREG(close)#線形回帰　
    #df["linearA"] = LINEARREG_ANGLE(close)##線形回帰　角度
    #df["linearI"] = LINEARREG_INTERCEPT(close)#線形回帰　JIEJU
    #df["linearS"] = LINEARREG_SLOPE(close)#線形回帰　坂
    #df["stddev"] = STDDEV(close)#標準偏差
    #df["tsf"] = TSF(close)#Time Series Forecast
    #df["var"] = VAR(close) #方差
    df["saleprice"] = 0
    df["buyprice"] = 0
    df["balance1"] = 0
    df["balance2"] = 0
    df["balance3"] = 0
    return df

def refresh2(code, df, days = MAX_DAYS):
    c10 = int(len(df) / 10)
    isSaled = False
    isBuyed = False
    salePrice = 0
    buyPrice = 0
    strpath = "csv/{}_r1.csv".format(code)
    if os.path.exists(strpath):
        os.remove(strpath) 
    # for i in range(c10):
    #     df2 = df[i*10:(i+1)*10]
    #     desc = (df2.high - df2.low ).describe() 
    #     std = desc["std"]
    #     minv = desc["min"]
    df2 = df
    df2["h2"] = df.high + MAX_HL
    df2["l2"] = df.low - MAX_HL
    for x in range(1,len(df2)):
        dy = df2.iloc[x-1] #data of yesteday.
        data = df2.iloc[x]   #data of today.  
        if dy.J > MAX_J:
            if data.high > dy.h2:
                isSaled = True
                df2.saleprice[x]  = dy.h2
            if isSaled and data.low < dy.h2 - MAX_FEE:
                isSaled = False
                df2.buyprice[x] = dy.h2 - MAX_FEE
                df2.balance1[x] = MAX_FEE
        elif dy.J< 100-MAX_J:
            if data.low < dy.l2:
                isBuyed = True
                df2.buyprice[x]  = dy.l2
            if isBuyed and data.low < dy.l2 + MAX_FEE:
                isBuyed = False
                df2.saleprice[x] = dy.l2 + MAX_FEE
                df2.balance2[x] = MAX_FEE
    df2.balance3 = df2.balance1 + df2.balance2
    if os.path.exists(strpath):
        df2.to_csv(strpath, header =False, mode='a')
    else:
        df2.to_csv(strpath, mode='w')

def show(df):
    
    ax = plt.subplot(311)
    df.close.plot()
    ax.set_title("Raw data")
    
    ax = plt.subplot(312)
    df.macd.plot(color = 'green')
    df.signal.plot(color = 'red')
    #df.histogram.bar(color = 'blue')
    left = np.array(range(len(df)))
    plt.bar(left, df.histogram)
    ax.set_title("MACD")
    
    ax = plt.subplot(313)   
    df.K.plot(color="green")
    df.D.plot(color="blue")
    df.J.plot(color="red")
    ax.set_title("KDJ")
    
    plt.show()
    pass
def showKDJ(df):
    columns = ['K','D','J']
    df2 = df[columns]
    df2.plot() 
    plt.show()
    pass

def showMACD(df):
    columns = ['macd','signal','histogram']
    df2 = df[columns]
    #df2.plot()
    df.macd.plot()
    df.signal.plot()
    #plt.figure()
    df2.histogram.plot(kind='bar')
    #df2.histogram.plot.bar()
    plt.show()
    pass

if __name__ == "__main__":
    code = 2127
    df = pd.read_csv("csv/{}.csv".format(code), index_col="date")
    df = refresh(df)    
    df = df.dropna()
    #df.to_csv("csv/{}_r1.csv".format(code))
    #showMACD(df)
    refresh2(code, df)
