# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 00:17:57 2020

@author: angad
"""

import yfinance as yf
import numpy as np
import pandas as pd

#Stock Universe consists of 2014 ET 500 companies of 2014

ET500 = ["IOC.NS","RELIANCE.NS","BPCL.NS","HINDPETRO.NS","TATAMOTORS.NS","SBIN.NS","ONGC.NS",
         "TATASTEEL.NS","HINDALCO.NS","BHARTIARTL.NS","LT.NS","TCS.NS","NTPC.NS","ICICIBANK.NS",
         "COALINDIA.NS","M&M.NS","VEDL.NS","GAIL.NS","ADANIENT.NS","INFY.NS","JSWSTEEL.NS",
         "HDFCBANK.NS","PNB.NS"] 

tickers = ["MMM","AXP","T","BA","CAT","CVX","CSCO","KO", "XOM","GE","GS","HD",
           "IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","NKE","PFE","PG","TRV",
           "UNH","VZ","V","WMT","DIS"]

selected=ET500

benchmark = ["^NSEI"]

start="2014-07-30"
end="2020-07-01"
total_periods=72

stock_data = {}

for i in range(len(selected)):
    stock_data[selected[i]] = yf.download(selected[i],start=start,end=end,interval="1mo")
    stock_data[selected[i]].dropna(inplace=True)
    
benchmark_data = {}

for i in range(len(benchmark)):
    benchmark_data[benchmark[i]] = yf.download(benchmark[i],start=start,end=end,interval="1mo")
    
n_top_performers = 6

#calculate monthly returns 
for i in range(len(selected)):
     stock_data[selected[i]]["monthly_return"] = stock_data[selected[i]]["Adj Close"].pct_change()
     stock_data[selected[i]]["monthly_return"]
     
for i in range(len(benchmark)):
     benchmark_data[benchmark[i]]["monthly_return"] = benchmark_data[benchmark[i]]["Adj Close"].pct_change()     
     
#backtesting
pfolio = ["IOC.NS","RELIANCE.NS","BPCL.NS","HINDPETRO.NS","TATAMOTORS.NS","SBIN.NS"]
mean_return = [np.nan]

for i in range(1,total_periods):
    temp=0
    for stock in pfolio:
        temp = temp + stock_data[stock].iloc[i]["monthly_return"]
    mean_return.append(temp/len(pfolio))
    
    return_of_stocks={}
    
    for stock in selected:
        return_of_stocks[stock] = stock_data[stock].iloc[i]["monthly_return"]
    sorted_tuple = sorted(return_of_stocks.items(), key=lambda x:x[1],reverse=True)    
    
    for i in range(n_top_performers):
        pfolio[i] = sorted_tuple[i][0]

#calculating KPIs
n=72/12
perfomance = pd.DataFrame(mean_return,columns=["monthly_return"])
perfomance["cum_return"] = (1+perfomance["monthly_return"]).cumprod()
CAGR_pfolio = perfomance.iloc[-1]["cum_return"]**1/n - 1
vol_pfolio = perfomance["monthly_return"].std()*np.sqrt(12)
Sharpe_pfolio = (CAGR_pfolio - 0.0597)/vol_pfolio

#for i in range(len(benchmark_data)):
  #  n=72/12
   # benchmark_data[benchmark[i]]["CS"] = (1 + benchmark_data[benchmark[i]]["monthly_return"]).cumprod()
   # vol = benchmark_data[benchmark[i]]["monthly_return"].std()*np.sqrt(12)
   # CAGR_index = benchmark_data[benchmark[i]]["CS"][-1]**(1/n) - 1
   # Sharpe = (CAGR_index - 0.0597)/vol
    

