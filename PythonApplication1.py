#-*- coding:utf-8 -*-

import datetime
import numpy as np
import pandas as pd
#import jsm
import YahooFinanceSpider as y
c = y.Crawler()


# 株価のデータ取得（銘柄コード, 開始日, 終了日）
def get_stock(code, start_date, end_date):
    # 期間設定
    year, month, day = start_date.split("-")
    start = datetime.date(int(year), int(month), int(day))
    
    year, month, day = end_date.split("-") 
    end = datetime.date(int(year), int(month), int(day))
    print(start) 
    # 株価データ取得
    #q = jsm.Quotes()
    target = c.get_price(code, start, end, y.DAILY) 
    #target = q.get_historical_prices(code, jsm.DAILY, start_date = start, end_date = end)
    
    # 項目ごとにリストに格納して返す
    date = [data.date for data in target]
    open = [data.open for data in target]
    close = [data.close for data in target]
    high = [data.high for data in target]
    low = [data.low for data in target]

    return target, [date, open, close, high, low]

def main():
    code=6641 #日新電機
    fromDate ='2017-9-23'
    toDate = '2017-9-27'

    # 株価の取得(銘柄コード, 開始日, 終了日)
    target, data = get_stock(code, fromDate, toDate)
    csvfile="{0}_{1}_{2}.csv".format(code,fromDate, toDate)
    target.to_csv(csvfile)
    

    ## 取得したデータの表示
    #print("日付\t始値\t終値\t高値\t安値")
    #for date, open, close, high, low in list(zip(*data)):
    #    print(date.strftime("%m/%d"), "\t", open, "\t", close, "\t", high, "\t", low)
    
if __name__ == "__main__":
    main()